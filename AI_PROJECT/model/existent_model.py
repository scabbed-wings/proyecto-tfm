import torch
import torch.utils
import torch.utils.data
import torchvision
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from model.utils import get_cuda_device, Averager
from pathlib import Path
from dataset.dataset import visualize_images
from dataset.utils.transformations import collate_function

def checkpoint(model, filename):
    torch.save(model.state_dict(), filename)


def train_model(train_data_loader, num_classes: int = 4, save_checkpoint = "AI_PROJECT/output/model/model.pth" ):
    model = torchvision.models.detection.fasterrcnn_mobilenet_v3_large_fpn(weights=None, weights_backbone=None)
    device = get_cuda_device()
    # get number of input features for the classifier
    in_features = model.roi_heads.box_predictor.cls_score.in_features

    # replace the pre-trained head with a new one
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)

    model.train()
    model.to(device)
    params = [p for p in model.parameters() if p.requires_grad]
    optimizer = torch.optim.SGD(params, lr=0.01, momentum=0.9, weight_decay=0.00001)
    lr_scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=1, gamma=0.5)

    num_epochs = 5

    loss_hist = Averager()
    itr = 1

    for epoch in range(num_epochs):
        loss_hist.reset()
        train_dataloader = torch.utils.data.DataLoader(train_data_loader,8, shuffle=True, 
                                    collate_fn=collate_function, pin_memory=True, num_workers=2)
        for images, targets in train_dataloader:
            
            images = list(image.to(device) for image in images)
            targets = [{k: v.to(device) for k, v in t.items()} for t in targets]

            loss_dict = model(images, targets)   ##Return the loss
            losses = sum(loss for loss in loss_dict.values())
            loss_value = losses.item()

            loss_hist.send(loss_value)  #Average out the loss

            optimizer.zero_grad()
            losses.backward()
            optimizer.step()

            if itr % 50 == 0:
                print(f"Iteration #{itr} loss: {loss_value}")

            itr += 1
        
        # update the learning rate
        if lr_scheduler is not None:
            lr_scheduler.step()

        print(f"Epoch #{epoch} loss: {loss_hist.value}")
    checkpoint(model,save_checkpoint)


def inference_test(weights_file, test_dataloader, num_classes=4):
    model = torchvision.models.detection.fasterrcnn_mobilenet_v3_large_fpn(pretrained=False)
    in_features = model.roi_heads.box_predictor.cls_score.in_features

    # replace the pre-trained head with a new one
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)
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
            scores = output[ind]['scores'].data.cpu()
            new_image = image.data.cpu()
            visualize_images(new_image, boxes, labels, inference=True)


