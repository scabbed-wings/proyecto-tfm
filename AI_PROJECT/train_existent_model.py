import torch
from dataset.load_dataset import get_torch_dataloader
from model.existent_model import train_model, inference_test

  
if __name__ == "__main__":
    train_data_loader, valid_data_loader, test_data_loader = get_torch_dataloader()
    train_model(train_data_loader)
    inference_test("AI_PROJECT\output\model\model.pth", test_data_loader)
    # model = torchvision.models.detection.fasterrcnn_resnet50_fpn(weights=None, weights_backbone=None)
