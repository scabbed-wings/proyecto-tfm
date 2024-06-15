import torch
import torch.utils
import torch.utils.data
import torchvision
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from model.utils import get_cuda_device, Averager, calculate_metrics, create_precision_recall_curve
from dataset.dataset import visualize_images
from dataset.utils.transformations import collate_function
from torchmetrics.detection import MeanAveragePrecision
import os
import numpy as np


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
    num_epochs = 20

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
                # new_valid_targets = valid_targets.copy()
                # for item in new_valid_targets: print(item['labels'].shape)
                # for item in new_valid_targets: item['scores'] = torch.ones(size=item['labels'].shape)
                output = model(images)
                output = [{k: v.to(torch.device("cuda")) for k, v in t.items()} for t in output]
                mAP.update(preds=output, target=valid_targets)
                metrics = mAP.compute()
                print(metrics)
            # update the learning rate
            if lr_scheduler is not None:
                lr_scheduler.step()
            if (epoch + 1) % 10 == 0:
                checkpoint(model, save_checkpoint, epoch=epoch+1)

            print(f"Epoch #{epoch} loss: {loss_hist.value}")


def inference_test(weights_file, model, test_dataloader):
    model.load_state_dict(torch.load(weights_file))
    device = get_cuda_device()
    model.to(device)
    model.eval()
    for images, targets in test_dataloader:
        images = list(image.to(device) for image in images)
        output = model(images)
        for ind, image in enumerate(images):
            boxes = output[ind]['boxes'].data.cpu()
            labels = output[ind]['labels'].data.cpu()
            # scores = output[ind]['scores'].data.cpu()
            new_image = image.data.cpu()
            visualize_images(new_image, boxes, labels, inference=True)


def model_test_metrics(weights_file, model, test_dataloader):
    metric_counter = 0
    class_thresholds = np.arange(start=0.0, step=0.05, stop=1.05)
    num_samples = 0
    model.load_state_dict(torch.load(weights_file))
    device = get_cuda_device()
    model.to(device)
    model.eval()
    for images, targets in test_dataloader:
        images = list(image.to(device) for image in images)
        num_samples += len(images)
        output = model(images)
        for ind, image in enumerate(images):
            predictions = dict()
            predictions["boxes"] = output[ind]['boxes'].data.cpu()
            predictions["labels"] = output[ind]['labels'].data.cpu()
            predictions["scores"] = output[ind]['scores'].data.cpu()
            if metric_counter == 0:
                metric_counter = calculate_metrics(predictions, targets[ind], class_thresholds)
            else:
                new_values = calculate_metrics(predictions, targets[ind], class_thresholds)
                for key in new_values.keys():
                    metric_counter[key] += new_values[key]

    create_precision_recall_curve(class_thresholds, metric_counter)
