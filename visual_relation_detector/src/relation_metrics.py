from pathlib import Path
from glob import glob
from deep_learning.datasets.dataset import process_relational_data
from deep_learning.models.detector_functions import loaded_unitary_inference, resize_bounding_boxes
from deep_learning.models.relational_classification_functions import unitary_inference_classificator
from PIL import Image
from torchvision.ops import box_iou
from visual_relation_detector.src.metric_calculator import MetricCalculator
from visual_relation_detector.src.follow_line_algorithm import follow_lines
from tqdm import tqdm
from visual_relation_detector.src.utils import already_detected, max_min_coordinates
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import cv2
from time import time


def box_correspondence(pred_boxes, gt_boxes, threshold: float = 0.5):
    correspondence_boxes = []
    iou = box_iou(pred_boxes, gt_boxes)
    for i in range(len(pred_boxes)):
        max_iou = iou[i, :].argmax()
        max_iou_value = iou[i, max_iou]
        if max_iou_value >= threshold:
            correspondence_boxes.append({
                "pred_box_index": i,
                "gt_box_index": int(max_iou)
            })
    return correspondence_boxes


def get_gt_index_from_correspondence(pred_index: int, correspondences: list):
    for elem in correspondences:
        if pred_index == elem['pred_box_index']:
            return elem['gt_box_index']
    return -1


def transform_predicted_relations_to_gt(predicted_relations: list, correspondences: list, ids):
    transformed_relations = []
    for relation in predicted_relations:
        gt_index1 = get_gt_index_from_correspondence(relation[0], correspondences)
        gt_index2 = get_gt_index_from_correspondence(relation[1], correspondences)
        id_value1 = ids[gt_index1] if gt_index1 >= 0 else gt_index1
        id_value2 = ids[gt_index2] if gt_index2 >= 0 else gt_index2
        transformed_relations.append([id_value1, id_value2])
    return transformed_relations


def gt_relations_to_list(gt_ids, gt_relations):
    relations_list = []
    for id_index, id in enumerate(gt_ids):
        for related_id in gt_relations[id_index]:
            if not already_detected(id, related_id, relations_list):
                relations_list.append([id, related_id])
    return relations_list


def loaded_crop_detections_and_relate(image, pred_boxes, model, classifier_thresh=0.9474):
    found_relations = []
    for index_source, box_source in enumerate(pred_boxes):
        for index_target, box_target in enumerate(pred_boxes):
            if index_target != index_source and not already_detected(index_target, index_source, found_relations):
                xmin, ymin, xmax, ymax = max_min_coordinates(box_source, box_target)
                crop_image = image.crop((int(xmin), int(ymin), int(xmax), int(ymax)))
                prediction = unitary_inference_classificator(model, image, crop_image)
                if prediction >= classifier_thresh:
                    found_relations.append([index_source, index_target])
    return found_relations


def count_tp_fp_fn(pred_relations_list: list, gt_relations: list, metric_counter: MetricCalculator):
    pred_counter = Counter(tuple(sorted(relation)) for relation in pred_relations_list)
    gt_counter = Counter(tuple(sorted(relation)) for relation in gt_relations)

    for par, pred_count in pred_counter.items():
        gt_count = gt_counter.get(par, 0)
        if gt_count > 0:
            metric_counter.increment_tp()
            metric_counter.increment_fp(max(pred_count - gt_count, 0))
        else:
            metric_counter.increment_fp(pred_count)

    for par, gt_count in gt_counter.items():
        if par not in pred_counter:
            metric_counter.increment_fn(gt_count)

    return metric_counter


def get_relation_metrics(dataset: str, detector_model, classification_model, device, dims,
                         method: str = "classifier"):
    image_list = glob(dataset + "/*.png") + glob(dataset + "/*.jpg")
    times = []
    metric_calculator = MetricCalculator()
    for image in tqdm(image_list):
        image_path = Path(image)
        image_data = Image.open(image_path)
        csv_path = image_path.with_suffix(".csv")
        gt_bboxes, gt_labels, gt_ids, gt_relations = process_relational_data(csv_path)
        gt_relations_list = gt_relations_to_list(gt_ids, gt_relations)
        pred_boxes, pred_labels = loaded_unitary_inference(detector_model, device, image_data)
        original_size_pred_boxes = resize_bounding_boxes(image_data, pred_boxes, dims)
        correspondences = box_correspondence(original_size_pred_boxes, gt_bboxes)
        if method == "classifier":
            start_time = time()
            found_relations = loaded_crop_detections_and_relate(image_data, original_size_pred_boxes,
                                                                classification_model)
            final_time = time() - start_time
            times.append(final_time)
        elif method == "contours":
            start_time = time()
            image_data = image_data.convert('L')
            image_array = np.asarray(image_data)
            plt.imshow(image_array, cmap='gray')
            plt.show()
            ret, thresholded_image = cv2.threshold(image_array, 127, 255, cv2.THRESH_BINARY_INV)
            kernel = np.ones((3, 3))
            dilate_threholded_image = cv2.dilate(thresholded_image, kernel, iterations=1)
            plt.imshow(dilate_threholded_image, 'gray')
            plt.show()
            found_relations = follow_lines(dilate_threholded_image, original_size_pred_boxes, pred_labels)
            final_time = time() - start_time
            times.append(final_time)
        pred_gt_relations = transform_predicted_relations_to_gt(found_relations, correspondences, gt_ids)
        count_tp_fp_fn(pred_gt_relations, gt_relations_list, metric_calculator)

    print(f"Time mean: {sum(times) / len(times)}s")
    return metric_calculator.calculate_metrics()
