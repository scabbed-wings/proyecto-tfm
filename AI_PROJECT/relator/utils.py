from models.relational_classification_model import PairedImageClassifier
import torch
from models.detector_definition import model_defintion
from collections import Counter


def max_min_coordinates(bbox1, bbox2):
    bbox1 = bbox1.int()
    bbox2 = bbox2.int()
    xmin = min(bbox1[0], bbox2[0])
    ymin = min(bbox1[1], bbox2[1])
    xmax = max(bbox1[2], bbox2[2])
    ymax = max(bbox1[3], bbox2[3])
    return xmin, ymin, xmax, ymax


def load_model(weights_path, device, model_type):
    if model_type == "detector":
        model = model_defintion()
    elif model_type == "classification":
        model = PairedImageClassifier()
    model.load_state_dict(torch.load(weights_path))
    model.to(device)
    model.eval()
    return model


def already_detected(target, source, found_relations):
    search_list = [target, source]
    for elem in found_relations:
        if Counter(elem) == Counter(search_list):
            return True
    return False
