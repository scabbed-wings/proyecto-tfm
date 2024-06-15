import torch
from torchvision.ops import box_iou
import numpy as np
import matplotlib.pyplot as plt


def get_cuda_device():
    # return torch.device('cuda' if torch.cuda.is_available() else "cpu")
    return torch.device("cpu")


class Averager:      # Return the average loss
    def __init__(self):
        self.current_total = 0.0
        self.iterations = 0.0

    def send(self, value):
        self.current_total += value
        self.iterations += 1

    @property
    def value(self):
        if self.iterations == 0:
            return 0
        else:
            return 1.0 * self.current_total / self.iterations

    def reset(self):
        self.current_total = 0.0
        self.iterations = 0.0


def counter_metrics_per_label(num_classes, num_threhsolds):
    '''Dictionary to store TP, FP and FN'''
    counter = dict()
    for i in range(1, num_classes + 1):
        counter[i] = np.zeros(shape=(num_threhsolds, 3))
    return counter


def precision_recall_dict(num_thresholds: int, num_classes: int = 3):
    # 0: Precision, 1: Recall
    pr_vector = dict()
    for i in range(1, num_classes + 1):
        pr_vector[i] = np.zeros(shape=(num_thresholds, 2))
    return pr_vector


def tp_fp_on_different_thresholds(pred_label, pred_score, num_classes, thresholds):
    tp_fp_vector = counter_metrics_per_label(3, thresholds.shape[0])
    for ind, threshold in enumerate(thresholds):
        for id_class in range(1, num_classes + 1):
            if pred_score > threshold and pred_label == id_class:
                tp_fp_vector[id_class][ind, 0] = 1
            else:
                tp_fp_vector[id_class][ind, 1] = 1
    return tp_fp_vector


def get_precision_recall(thresholds_counter: dict, num_thresholds):
    precision_recall_vector = precision_recall_dict(num_thresholds=num_thresholds)
    for key in thresholds_counter.keys():
        for ind, row in enumerate(thresholds_counter[key]):
            precision_recall_vector[key][ind, 0] = row[0] / (row[0] + row[1]) if row[0] + row[1] > 0 else 0
            precision_recall_vector[key][ind, 1] = row[0] / (row[0] + row[2]) if row[0] + row[2] > 0 else 0
    return precision_recall_vector


def create_precision_recall_curve(thresholds, thresholds_counter):
    styles = ["-b", "-g", "-r"]
    precision_recall_vector = get_precision_recall(thresholds_counter, thresholds.shape[0])
    for ind, key in enumerate(precision_recall_vector.keys()):
        precision = precision_recall_vector[key][:, 0]
        recall = precision_recall_vector[key][:, 1]
        plt.plot(precision, recall, styles[ind], label=f"Class {key}")
    plt.xlabel("Precision")
    plt.ylabel("Recall")
    plt.axis((0, 1, 0, 1))
    plt.title("Precision-Recall Curve")
    plt.legend(loc=4)
    plt.show()


def calculate_metrics(predictions, groundtruth, class_thresholds, iou_threshold: float = 0.5):

    thresholds_counter = counter_metrics_per_label(3, class_thresholds.shape[0])
    iou_matrix = box_iou(predictions["boxes"], groundtruth["boxes"])
    gt_found = []
    for num_row, row in enumerate(iou_matrix):
        greater_iou = row >= iou_threshold
        indexes = greater_iou.nonzero()
        if indexes.nelement() > 0:
            if indexes.nelement() > 1:
                print("MOre indexes found")
            for index in indexes:
                # print("Number of box: ", num_row, " IOU with GT BOX: ", index.item())
                pred_label = predictions["labels"][num_row]
                pred_score = predictions["scores"][num_row]
                # gt_label = groundtruth["labels"][index.item()]
                gt_found.append(index.item())
                pred_tp_fp = tp_fp_on_different_thresholds(pred_label, pred_score, 3, class_thresholds)
                for key in thresholds_counter.keys():
                    thresholds_counter[key] += pred_tp_fp[key]
        else:
            for key in thresholds_counter.keys():
                thresholds_counter[key][:, 1] += 1

    gt_found = set(gt_found)
    fn_diff = len(groundtruth["boxes"]) - len(gt_found)
    fn = fn_diff if fn_diff >= 0 else 0
    for key in thresholds_counter.keys():
        thresholds_counter[key][:, 2] += fn

    return thresholds_counter
