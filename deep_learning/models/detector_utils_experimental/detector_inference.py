from torchvision.models.detection.image_list import ImageList
import torch
from torchvision.ops import boxes as box_ops
import torch.nn.functional as F
from torch import Tensor
from typing import List, Tuple, Dict
from models.detector_utils.utils import BoxCoder


def postprocess_detections(
        class_logits,  # type: Tensor
        box_regression,  # type: Tensor
        proposals,  # type: List[Tensor]
        image_shapes,  # type: List[Tuple[int, int]]
        score_thresh,
        nms_thresh,
        detections_per_img,
    ):
        # type: (...) -> Tuple[List[Tensor], List[Tensor], List[Tensor]]
        device = class_logits.device
        num_classes = class_logits.shape[-1]
        boxes_per_image = [boxes_in_image.shape[0] for boxes_in_image in proposals]
        box_coder = BoxCoder((10.0, 10.0, 5.0, 5.0))
        pred_boxes = box_coder.decode(box_regression, proposals)
        pred_scores = F.softmax(class_logits, -1)
        pred_boxes_list = pred_boxes.split(boxes_per_image, 0)
        pred_scores_list = pred_scores.split(boxes_per_image, 0)

        all_boxes = []
        all_scores = []
        all_labels = []
        for boxes, scores, image_shape in zip(pred_boxes_list, pred_scores_list, image_shapes):
            boxes = box_ops.clip_boxes_to_image(boxes, image_shape)

            # create labels for each prediction
            labels = torch.arange(num_classes, device=device)
            labels = labels.view(1, -1).expand_as(scores)

            # remove predictions with the background label
            boxes = boxes[:, 1:]
            scores = scores[:, 1:]
            labels = labels[:, 1:]



            # batch everything, by making every class prediction be a separate instance
            boxes = boxes.reshape(-1, 4)
            scores = scores.reshape(-1)
            labels = labels.reshape(-1)

            # remove low scoring boxes
            inds = torch.where(scores > score_thresh)[0]
            boxes, scores, labels = boxes[inds], scores[inds], labels[inds]

            # print("Boxes: ", boxes)
            # print("Scores: ", scores)
            # print("Labels: ", labels)

            # remove empty boxes
            keep = box_ops.remove_small_boxes(boxes, min_size=1e-2)
            boxes, scores, labels = boxes[keep], scores[keep], labels[keep]

            # non-maximum suppression, independently done per class
            keep = box_ops.batched_nms(boxes, scores, labels, nms_thresh)
            # keep only topk scoring predictions
            keep = keep[: detections_per_img]
            boxes, scores, labels = boxes[keep], scores[keep], labels[keep]

            all_boxes.append(boxes)
            all_scores.append(scores)
            all_labels.append(labels)

        return all_boxes, all_scores, all_labels


def get_logits_and_probabilities(model, images):

    # Transformar imágenes
    images_transformed = model.transform(images)  
    transformed_tensors = images_transformed[0].tensors  

    # Obtener características
    features = model.backbone(transformed_tensors)

    # Obtener propuestas
    proposals, _ = model.rpn(images_transformed[0], features)  

    # Pasar las características y propuestas a la cabeza del ROI
    image_shapes =  [(img.shape[1], img.shape[2]) for img in images]
    box_features = model.roi_heads.box_roi_pool(features, proposals, image_shapes)
    box_features = model.roi_heads.box_head(box_features)

    # Aplanar box_features para pasar al predictor
    box_features_flat = box_features.flatten(start_dim=1)  # Cambiar aquí si es necesario
    print("Score thresh: ", model.roi_heads.score_thresh)

    # Obtener logits de la cabeza del ROI
    box_logits, box_deltas = model.roi_heads.box_predictor(box_features_flat)
    boxes, scores, labels = postprocess_detections(box_logits, box_deltas, proposals, image_shapes,
                                                   model.roi_heads.score_thresh,
                                                   model.roi_heads.nms_thresh,
                                                   model.roi_heads.detections_per_img)
    print("Boxes: ", boxes, " Scores: ", scores, " Labels: ", labels)
    num_images = len(boxes)
    result: List[Dict[str, torch.Tensor]] = []
    for i in range(num_images):
        result.append(
            {
                "boxes": boxes[i],
                "labels": labels[i],
                "scores": scores[i],
            }
        )
    
    return result