import pickle
from relator.read_bboxes import read_box
from relator.follow_line_algorithm import follow_lines
from torchvision.transforms.functional import pil_to_tensor
from datasets.dataset import visualize_images
from PIL import Image
import numpy as np
import cv2

if __name__ == "__main__":
    test_image = r"data_generator\test\img362.png"
    image = Image.open(test_image)
    image = image.convert('L')
    image_array = np.asarray(image)
    ret, thresholded_image = cv2.threshold(image_array,127,255,cv2.THRESH_BINARY_INV)
    kernel = np.ones((3,3))
    dilate_thresholded_image = cv2.dilate(thresholded_image, kernel, iterations=1)
    bboxes= []
    labels = []
    with open('pred_boxes.pkl', 'rb') as file_boxes:
        bboxes = pickle.load(file_boxes)
    with open('pred_labels.pkl', 'rb') as file_labels:
        labels = pickle.load(file_labels)
    follow_lines(image, dilate_thresholded_image, bboxes, labels)
    image_tensor = pil_to_tensor(image)
    visualize_images(image_tensor, bboxes, labels, inference=True, box_index=True)