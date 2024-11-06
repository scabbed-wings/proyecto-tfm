import torch
import torch.utils
import torch.utils.data
from deep_learning.datasets.dataset import visualize_images
from deep_learning.datasets.utils.transformations import collate_function_detector
from torchmetrics.detection import MeanAveragePrecision
from PIL import Image
import os
from tqdm import tqdm
from pathlib import Path
# from models.detector_utils.detector_inference import get_logits_and_probabilities
from deep_learning.models.utils import (get_cuda_device, Averager, nms_on_output_dictionary, flatten_list,
                                        nms_filter_boxes, evaluate_predictions, test_transform)


def checkpoint(model, filedir, experiment_name, epoch, best):
    file_parent = Path(os.path.join(filedir, experiment_name))
    file_parent.mkdir(parents=True, exist_ok=True)
    file_name = f"best_model_{epoch}.pth" if best else f"model_{epoch}.pth"
    file_name = os.path.join(file_parent, file_name)
    torch.save(model.state_dict(), file_name)


def eval_checkpoint(model, validation_dataloader, device):
    mAP = MeanAveragePrecision(box_format="xyxy", iou_type="bbox", class_metrics=True)
    model.eval()
    with torch.no_grad():
        for images, valid_targets in tqdm(validation_dataloader):
            print("Validation images: ", len(images))
            images = list(image.to(device) for image in images)
            valid_targets = [{k: v.to(torch.device("cuda")) for k, v in t.items()} for t in valid_targets]
            output = model(images)
            output = [{k: v.to(torch.device("cuda")) for k, v in t.items()} for t in output]
            filtered_output = nms_on_output_dictionary(output, iou_threshold=0.15)
            mAP.update(preds=filtered_output, target=valid_targets)
    metrics = mAP.compute()
    print(metrics)
    return metrics


def train_model(train_data_loader, valid_data_loader,
                model, experiment_name,
                save_checkpoint="AI_PROJECT/output/detector_models/",
                epochs=30,
                lr=0.001,
                performance_parameter='map'):
    device = get_cuda_device()
    print("Training on: ", device)
    model.to(device)
    params = [p for p in model.parameters() if p.requires_grad]
    # optimizer = torch.optim.SGD(params, lr=0.001, momentum=0.9, weight_decay=0.01)
    optimizer = torch.optim.Adam(params, lr=lr)
    lr_scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=1, gamma=0.5)
    num_epochs = epochs
    best_metric_value = 0
    loss_hist = Averager()
    itr = 1

    for epoch in range(num_epochs):
        loss_hist.reset()
        train_dataloader = torch.utils.data.DataLoader(train_data_loader, 128, collate_fn=collate_function_detector,
                                                       pin_memory=True, num_workers=4)
        model.train()
        print("Training epoch ", epoch)
        for images, targets in tqdm(train_dataloader):

            images = list(image.to(device) for image in images)
            targets = [{k: v.to(device) for k, v in t.items()} for t in targets]

            loss_dict = model(images, targets)   # Return the loss
            losses = sum(loss for loss in loss_dict.values())
            loss_value = losses.item()

            loss_hist.send(loss_value)  # Average out the loss

            optimizer.zero_grad()
            losses.backward()
            optimizer.step()

            if itr % 50 == 0:
                print(f"Iteration #{itr} loss: {loss_value}")

            itr += 1

        print("Evaluating epoch ", epoch)
        metrics = eval_checkpoint(model, valid_data_loader, device)

        # update the learning rate
        if lr_scheduler is not None:
            lr_scheduler.step()

        if metrics[performance_parameter] > best_metric_value:
            best_metric_value = metrics[performance_parameter]
            checkpoint(model, save_checkpoint, experiment_name, epoch=epoch+1, best=True)
        elif (epoch + 1) % 5 == 0:
            checkpoint(model, save_checkpoint, experiment_name, epoch=epoch+1, best=False)

        print(f"Epoch #{epoch} loss: {loss_hist.value}")


def inference_test(weights_file, model, test_dataloader, iou_threshold):
    model.load_state_dict(torch.load(weights_file))
    device = get_cuda_device()
    model.to(device)
    model.eval()
    with torch.no_grad():
        for images, _ in test_dataloader:
            images = list(image.to(device) for image in images)
            output = model(images)
            for ind, image in enumerate(images):
                boxes = output[ind]['boxes'].data.cpu()
                labels = output[ind]['labels'].data.cpu()
                scores = output[ind]['scores'].data.cpu()
                filtered_boxes, filtered_labels, _ = nms_filter_boxes(boxes, scores, labels, iou_threshold)
                new_image = image.data.cpu()
                visualize_images(new_image, filtered_boxes, filtered_labels, inference=True)


def get_inference_and_metrics(weights_file, model, data_loader, num_classes, iou_threshold=0.15):
    model.load_state_dict(torch.load(weights_file))
    device = get_cuda_device()
    model.to(device)
    model.eval()
    y_true = {i: [] for i in range(1, num_classes+1)}
    y_scores = {i: [] for i in range(1, num_classes+1)}

    with torch.no_grad():
        for images, targets in data_loader:
            images = [image.to(device) for image in images]
            outputs = model(images)

            for i, output in enumerate(outputs):
                gt_boxes = targets[i]['boxes'].cpu().numpy()
                gt_labels = targets[i]['labels'].cpu().numpy()
                pred_boxes = output['boxes'].data.cpu()
                pred_scores = output['scores'].data.cpu()
                pred_labels = output['labels'].data.cpu()
                filtered_boxes, filtered_labels, filtered_scores = nms_filter_boxes(pred_boxes,
                                                                                    pred_scores,
                                                                                    pred_labels,
                                                                                    iou_threshold)
                filtered_boxes = filtered_boxes.numpy()
                filtered_labels = filtered_labels.numpy()
                filtered_scores = filtered_scores.numpy()
                tp, fp, fn = evaluate_predictions(gt_boxes, gt_labels, filtered_boxes, filtered_labels, iou_threshold)
                for class_id in range(1, num_classes+1):
                    y_true[class_id].extend([1] * tp[class_id] + [0] * fp[class_id])
                    y_scores[class_id].extend(filtered_scores[filtered_labels == class_id])

    return y_true, y_scores


def metrics_with_torchmetrics(weights_file, model, dataloader, iou_threshold=0.5):
    model.load_state_dict(torch.load(weights_file))
    mAP = MeanAveragePrecision(box_format="xyxy", iou_type="bbox", class_metrics=True)
    device = get_cuda_device()
    model.to(device)
    model.eval()

    gt_labels = []
    pred_scores = []
    with torch.no_grad():
        for images, test_targets in dataloader:
            # result = get_logits_and_probabilities(model, images)
            images = list(image.to(device) for image in images)
            test_targets = [{k: v.to(torch.device("cuda")) for k, v in t.items()} for t in test_targets]
            output = model(images)
            # print("Output: ", output)
            gt_labels += [torch.flatten(target['labels']).cpu().tolist() for target in test_targets]
            output = [{k: v.to(torch.device("cuda")) for k, v in t.items()} for t in output]
            filtered_output = nms_on_output_dictionary(output, iou_threshold=iou_threshold)
            pred_scores += [prediction["scores"] for prediction in filtered_output]
            mAP.update(preds=filtered_output, target=test_targets)
    gt_labels = flatten_list(gt_labels)
    pred_scores = flatten_list(pred_scores)
    metrics = mAP.compute()
    print(metrics)


def resize_bounding_boxes(image: Image, bounding_boxes, dims):
    original_size_tensor = torch.tensor([image.width, image.height, image.width, image.height])
    resized_tensor = torch.tensor([dims[0], dims[1], dims[0], dims[1]])
    prop_pred_boxes = bounding_boxes / resized_tensor
    original_size_pred_boxes = prop_pred_boxes * original_size_tensor
    return original_size_pred_boxes


def unitary_inference(model, weights_file, image, dims=(320, 320)):
    print("Loading model")
    model.load_state_dict(torch.load(weights_file))
    device = get_cuda_device()
    transform = test_transform(dims)
    print("Processing image")
    processed_image = transform(image)
    processed_image = processed_image.unsqueeze(0)
    model.to(device)
    model.eval()
    with torch.no_grad():
        processed_image.to(device)
        print("Inference on image")
        output = model(processed_image)[0]
        boxes = output['boxes'].data.cpu()
        labels = output['labels'].data.cpu()
        scores = output['scores'].data.cpu()
        filtered_boxes, filtered_labels, _ = nms_filter_boxes(boxes, scores, labels, 0.15)
        new_image = processed_image.data.cpu()
        new_image = new_image.squeeze(0)
        return filtered_boxes, filtered_labels


def loaded_unitary_inference(model, device, image, dims=(320, 320)):
    transform = test_transform(dims)
    processed_image = transform(image)
    processed_image = processed_image.unsqueeze(0)
    with torch.no_grad():
        processed_image = processed_image.to(device)
        output = model(processed_image)[0]
        boxes = output['boxes'].data.cpu()
        labels = output['labels'].data.cpu()
        scores = output['scores'].data.cpu()
        filtered_boxes, filtered_labels, _ = nms_filter_boxes(boxes, scores, labels, 0.15)
        new_image = processed_image.data.cpu()
        new_image = new_image.squeeze(0)
    return filtered_boxes, filtered_labels
