import torch
import torch.utils
import torch.utils.data
from datasets.dataset import visualize_images
from datasets.utils.transformations import collate_function
from torchmetrics.detection import MeanAveragePrecision
import os
from models.utils import (get_cuda_device, Averager, nms_on_output_dictionary,
                         nms_filter_boxes, evaluate_predictions, test_transform)


def checkpoint(model, filedir, epoch):
    filename = os.path.join(filedir, f"model_{epoch}.pth")
    torch.save(model.state_dict(), filename)


def train_model(train_data_loader, valid_data_loader,
                model,
                save_checkpoint="AI_PROJECT/output/"):
    device = get_cuda_device()
    print("Training on: ", device)
    model.to(device)
    params = [p for p in model.parameters() if p.requires_grad]
    # optimizer = torch.optim.SGD(params, lr=0.001, momentum=0.9, weight_decay=0.01)
    optimizer = torch.optim.Adam(params, lr=0.001)
    lr_scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=1, gamma=0.5)
    mAP = MeanAveragePrecision(box_format="xyxy", iou_type="bbox", class_metrics=True)
    num_epochs = 30

    loss_hist = Averager()
    itr = 1

    for epoch in range(num_epochs):
        loss_hist.reset()
        train_dataloader = torch.utils.data.DataLoader(train_data_loader, 128, collate_fn=collate_function,
                                                       pin_memory=True, num_workers=4)
        model.train()
        for images, targets in train_dataloader:

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

        model.eval()
        with torch.no_grad():
            for images, valid_targets in valid_data_loader:
                print("Validation images: ", len(images))
                images = list(image.to(device) for image in images)
                valid_targets = [{k: v.to(torch.device("cuda")) for k, v in t.items()} for t in valid_targets]
                output = model(images)
                output = [{k: v.to(torch.device("cuda")) for k, v in t.items()} for t in output]
                filtered_output = nms_on_output_dictionary(output, iou_threshold=0.15)
                mAP.update(preds=filtered_output, target=valid_targets)
                metrics = mAP.compute()
                print(metrics)
            # update the learning rate
            if lr_scheduler is not None:
                lr_scheduler.step()
            if (epoch + 1) % 5 == 0:
                checkpoint(model, save_checkpoint, epoch=epoch+1)

            print(f"Epoch #{epoch} loss: {loss_hist.value}")


def inference_test(weights_file, model, test_dataloader):
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
                filtered_boxes, filtered_labels, _ = nms_filter_boxes(boxes, scores, labels, 0.15)
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
                pred_boxes = output['boxes'].cpu().numpy()
                pred_scores = output['scores'].cpu().numpy()
                pred_labels = output['labels'].cpu().numpy()

                tp, fp = evaluate_predictions(gt_boxes, gt_labels, pred_boxes, pred_labels, iou_threshold)
                #tp, fp, fn = evaluate_predictions(gt_boxes, gt_labels, pred_boxes, pred_labels, iou_threshold)
                for class_id in range(1, num_classes+1):
                    y_true[class_id].extend([1] * tp[class_id] + [0] * fp[class_id])
                    y_scores[class_id].extend(pred_scores[pred_labels == class_id])

    return y_true, y_scores


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
