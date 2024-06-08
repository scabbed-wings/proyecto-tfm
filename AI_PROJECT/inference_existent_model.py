import torch
import torchvision
from dataset.load_dataset import get_torch_dataloader
from model.existent_model import model_test_metrics
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision.models.detection.rpn import AnchorGenerator
from torchvision.models.detection import FasterRCNN_MobileNet_V3_Large_FPN_Weights

if __name__ == "__main__":

    train_data_loader, valid_data_loader, test_data_loader = get_torch_dataloader(dataset_path="data_generator/img_fractional", 
                                                                                  dims=(500,500))
    model = torchvision.models.detection.fasterrcnn_mobilenet_v3_large_fpn(
        weights=FasterRCNN_MobileNet_V3_Large_FPN_Weights.DEFAULT)
        # get number of input features for the classifier
    model.rpn.score_thresh = 0.2
    model.rpn.nms_thresh = 0.8
    model.roi_heads.detections_per_img = 60
    model.roi_heads.nms_thresh = 0.8
    model.roi_heads.score_thresh = 0.1
    #model.rpn._post_nms_top_n["testing"] = 1500
    #model.rpn._post_nms_top_n["training"] = 2000
    #model.transform.image_mean = [0.9844960020963516, 0.9844960020963516, 0.9844960020963516]
    #model.transform.image_std = [0.11468420904814396, 0.11468420904814396, 0.11468420904814396]
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    print(in_features)
    num_classes = 4
    # replace the pre-trained head with a new one
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes,)
    model_test_metrics("AI_PROJECT\output\model_10.pth",model, test_data_loader)