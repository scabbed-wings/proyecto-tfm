import torch
from torchvision.ops import box_iou, nms
import torchvision.transforms as TT
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import precision_recall_curve
from sklearn.preprocessing import label_binarize


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


def get_cuda_device():
    # return torch.device('cuda' if torch.cuda.is_available() else "cpu")
    return torch.device("cpu")


def flatten_list(labels):
    new_list = []
    for list in labels:
        new_list += list
    return new_list


def create_PRC_2(gt_labels, pred_scores, num_classes=3):
    classes = [i for i in range(1, num_classes + 1)]
    label_binarizer = label_binarize(gt_labels ,classes=classes)


def nms_filter_boxes(result_boxes, result_scores, result_labels, iou_threshold):
    nms_ids = nms(result_boxes, result_scores, iou_threshold)
    filtered_boxes = result_boxes.index_select(0, nms_ids)
    filtered_labels = result_labels.index_select(0, nms_ids)
    filtered_scores = result_scores.index_select(0, nms_ids)
    return filtered_boxes, filtered_labels, filtered_scores


def nms_on_output_dictionary(output, iou_threshold=0.5):
    filtered_dictionary = []
    for item in output:
        filtered_result = nms_filter_boxes(item['boxes'], item['scores'], item['labels'], iou_threshold)
        item['boxes'] = filtered_result[0]
        item['labels'] = filtered_result[1]
        item['scores'] = filtered_result[2]
        filtered_dictionary.append(item)
    return filtered_dictionary


def evaluate_predictions(gt_boxes, gt_labels, pred_boxes, pred_labels, iou_threshold=0.5, num_classes=3):
    tp = {i: 0 for i in range(1, num_classes+1)}
    fp = {i: 0 for i in range(1, num_classes+1)}
    fn = {i: 0 for i in range(1, num_classes+1)}

    for class_id in range(1, num_classes+1):
        gt_mask = gt_labels == class_id
        pred_mask = pred_labels == class_id

        if gt_mask.sum() == 0:
            continue

        ious = box_iou(torch.tensor(pred_boxes[pred_mask]), torch.tensor(gt_boxes[gt_mask])).numpy()

        for i in range(len(gt_boxes[gt_mask])):
            max_iou = ious[:, i].max() if ious.shape[1] > i else 0
            if max_iou >= iou_threshold:
                tp[class_id] += 1
            else:
                fn[class_id] += 1

        fp[class_id] += len(pred_boxes[pred_mask]) - tp[class_id]

    return tp, fp, fn


def create_PRC(y_true, y_scores, num_classes):
    styles = ["-r", "-g", "-b"]
    class_name = ["Entity", "Attribute", "Relation"]
    fig, axis = plt.subplots(num_classes)
    
    for class_id in range(1, num_classes+1):
        precision, recall, thresholds = precision_recall_curve(y_true[class_id], y_scores[class_id])
        
        axis[class_id - 1].plot(recall, precision, styles[class_id - 1], label=f'Class {class_name[class_id - 1]}')
        axis[class_id - 1].set_title(class_name[class_id - 1])
        axis[class_id - 1].set_xlabel('Recall')
        axis[class_id - 1].set_ylabel('Precision')
        
    fig.suptitle('Precision-Recall Curve for Each Class')
    fig.savefig('metrics_model.png')
    plt.show()


def test_transform(dims):
    return TT.Compose([
        TT.Grayscale(),
        TT.Resize(dims),
        TT.ToTensor(),
    ])