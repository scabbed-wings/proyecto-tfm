from models.detector_functions import unitary_inference
from models.detector_definition import model_defintion
from models.relational_classification_model import PairedImageClassifier
from models.relational_classification_functions import unitary_inference_classificator
import numpy as np
from detect_and_relate import resize_bounding_boxes
from relator.follow_line_algorithm import follow_lines
from PIL import Image
import pickle
import cv2

if __name__ == "__main__":
    model_detector = model_defintion()
    detector_weights_path = "AI_PROJECT\output\model_15.pth"
    classifier_weights_path = r"AI_PROJECT\output\classification_output\best_model_21.pth"
    test_image = r"AI_PROJECT\prueba.png"
    dims = (320, 320)
    image = Image.open(test_image)
    pred_boxes, pred_labels = unitary_inference(model_detector, detector_weights_path, image, dims)
    original_size_pred_boxes = resize_bounding_boxes(image, pred_boxes, dims)
    print(pred_boxes)
    image = image.convert('L')
    image_array = np.asarray(image)
    ret, thresholded_image = cv2.threshold(image_array,127,255,cv2.THRESH_BINARY_INV)
    kernel = np.ones((3,3))
    dilate_threholded_image = cv2.dilate(thresholded_image, kernel, iterations=1)
    follow_lines(image, dilate_threholded_image, original_size_pred_boxes, pred_labels)