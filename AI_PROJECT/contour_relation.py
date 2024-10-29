from models.detector_functions import unitary_inference
from models.detector_definition import model_defintion
from datasets.dataset import visualize_images
from torchvision.transforms.functional import pil_to_tensor
import numpy as np
from detect_and_relate import resize_bounding_boxes
from relator.follow_line_algorithm import follow_lines
from PIL import Image
import cv2


if __name__ == "__main__":
    model_detector = model_defintion()
    detector_weights_path = r"AI_PROJECT\output\model_15.pth"
    test_image = r"data_generator\test\img392.png"
    dims = (320, 320)
    image = Image.open(test_image)
    pred_boxes, pred_labels = unitary_inference(model_detector, detector_weights_path, image, dims)
    original_size_pred_boxes = resize_bounding_boxes(image, pred_boxes, dims)
    image = image.convert('L')
    image_array = np.asarray(image)
    ret, thresholded_image = cv2.threshold(image_array, 127, 255, cv2.THRESH_BINARY_INV)
    kernel = np.ones((3, 3))
    dilate_threholded_image = cv2.dilate(thresholded_image, kernel, iterations=1)
    relations_found = follow_lines(dilate_threholded_image, original_size_pred_boxes, pred_labels)
    print("Found relations: ", relations_found)
    image_tensor = pil_to_tensor(image)
    visualize_images(image_tensor, original_size_pred_boxes, pred_labels, inference=True, box_index=True)
