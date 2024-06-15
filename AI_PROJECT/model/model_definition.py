from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
from torchvision.models.detection.rpn import AnchorGenerator
from torchvision.models.detection import FasterRCNN_MobileNet_V3_Large_FPN_Weights
import torchvision


def model_defintion():
    model = torchvision.models.detection.fasterrcnn_mobilenet_v3_large_fpn(
            weights=FasterRCNN_MobileNet_V3_Large_FPN_Weights.DEFAULT)
    model.rpn.score_thresh = 0.2
    model.rpn.nms_thresh = 0.6
    model.roi_heads.detections_per_img = 150
    model.roi_heads.nms_thresh = 0.6
    model.roi_heads.score_thresh = 0.1
    # model.rpn._post_nms_top_n["testing"] = 1500
    # model.rpn._post_nms_top_n["training"] = 2000
    # model.transform.image_mean = [0.9844960020963516, 0.9844960020963516, 0.9844960020963516]
    # model.transform.image_std = [0.11468420904814396, 0.11468420904814396, 0.11468420904814396]
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    num_classes = 4
    # replace the pre-trained head with a new one
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)
    return model
