import torch
from torchvision.ops import box_iou

def get_cuda_device():
    return torch.device('cuda' if torch.cuda.is_available() else "cpu")
    #return torch.device("cpu")


class Averager:      ##Return the average loss 
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


def calculate_metrics(predictions, groundtruth, iou_threshold: float=0.5):
    iou_matrix = box_iou(predictions["boxes"], groundtruth["boxes"])
    for num_row, row in enumerate(iou_matrix):
        greater_iou = row >= iou_threshold
        indexes= greater_iou.nonzero()
        if indexes.nelement() == 1:
            for index in indexes:
                print("Number of box: ", num_row, " IOU with GT BOX: ", index.item())
                pred_label = predictions["labels"][num_row]
                gt_label = groundtruth["labels"][index.item()]
                if pred_label.item() - gt_label.item() != 0:
                    print("PRED_SCORE: ", predictions["scores"][num_row], " PRED_LABEL: ", predictions["labels"][num_row])
                    print("GROUNDTRUTH_LABEL: ", groundtruth["labels"][index.item()])