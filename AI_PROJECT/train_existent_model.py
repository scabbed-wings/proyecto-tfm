import torch
import torchvision
from dataset.load_dataset import get_torch_dataloader
from model.existent_model import train_model, inference_test
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision.models.detection.rpn import AnchorGenerator
from torchvision.models.detection import FasterRCNN_MobileNet_V3_Large_FPN_Weights

  
if __name__ == "__main__":
    train_data_loader, valid_data_loader, test_data_loader = get_torch_dataloader(dims=(720,720))
    model = torchvision.models.detection.fasterrcnn_mobilenet_v3_large_fpn(
        weights=FasterRCNN_MobileNet_V3_Large_FPN_Weights.DEFAULT)
        # get number of input features for the classifier
    model.rpn.score_thresh = 0.3
    #model.rpn._post_nms_top_n["testing"] = 1500
    #model.rpn._post_nms_top_n["training"] = 2000
    #model.transform.image_mean = [0.9844960020963516, 0.9844960020963516, 0.9844960020963516]
    #model.transform.image_std = [0.11468420904814396, 0.11468420904814396, 0.11468420904814396]
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    print(in_features)
    num_classes = 4
    # replace the pre-trained head with a new one
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes,)
    train_model(train_data_loader, valid_data_loader, model)
    inference_test("AI_PROJECT\output\model\model.pth",model, test_data_loader)
    # model = torchvision.models.detection.fasterrcnn_resnet50_fpn(weights=None, weights_backbone=None)
