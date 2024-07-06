from PIL import Image
import numpy as np
import cv2
import matplotlib.pyplot as plt
import pickle


def relation_is_valid(label_source, label_target):
    if label_source == 1 and (label_target in [2,3]):
        return True
    elif label_source == 2 and (label_target in [1,3]):
        return True
    elif label_source == 3 and (label_target in [1,2]):
        return True
    else:
        return False
    

def max_min_coordinates(bbox1, bbox2):
    bbox1 = bbox1.int()
    bbox2 = bbox2.int()
    xmin = min(bbox1[0], bbox2[0])
    ymin = min(bbox1[1], bbox2[1])
    xmax = max(bbox1[2], bbox2[2])
    ymax = max(bbox1[3], bbox2[3])
    return xmin, ymin, xmax, ymax


def resize_boxes_2_crop(xmin, ymin, bbox1, bbox2):
    bbox1 = bbox1.int()
    bbox2 = bbox2.int()
    bbox1 = [bbox1[0] - xmin, bbox1[1] - ymin, bbox1[2] - xmin, bbox1[3] - ymin]
    bbox2 = [bbox2[0] - xmin, bbox2[1] - ymin, bbox2[2] - xmin, bbox2[3] - ymin]
    return bbox1, bbox2


def crop_outsider_elements(bboxes, binary_image, index_source, index_target):
    copy_binary_image = binary_image.copy()
    for ind, bbox in enumerate(bboxes):
        if ind != index_source and ind != index_target:
            bbox_to_crop = bbox.int()
            copy_binary_image[bbox_to_crop[1]:bbox_to_crop[3],
                              bbox_to_crop[0]:bbox_to_crop[2]] = 0
    xmin, ymin, xmax, ymax = max_min_coordinates(bboxes[index_source], bboxes[index_target])
    bbox_source, bbox_target = resize_boxes_2_crop(xmin, ymin, bboxes[index_source], 
                                                   bboxes[index_target])
    print("BBOX_SOURCE: ", bbox_source, "\nBBOX_TARGET: ", bbox_target)
    copy_binary_image = copy_binary_image[ymin:ymax, xmin:xmax]
    plt.imshow(copy_binary_image)
    plt.show()
    return copy_binary_image


def follow_lines(binary_image, bboxes, labels):
    for ind_source, bbox_source in enumerate(bboxes):
        bbox_source_label = labels[ind_source]
        for ind_target, bbox_target in enumerate(bboxes):
            bbox_target_label = labels[ind_target]
            if relation_is_valid(bbox_source_label, bbox_target_label):
                cropped_binary = crop_outsider_elements(bboxes, binary_image, ind_source, ind_target)
                contours = cv2.findContours(cropped_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
                contours = contours[0] if len(contours) == 2 else contours[1]
                print(len(contours))


if __name__ == "__main__":
    test_image = r"data_generator\test\img398.png"
    image = Image.open(test_image)
    image = image.convert('L')
    image_array = np.asarray(image)
    ret, thresholded_image = cv2.threshold(image_array,127,255,cv2.THRESH_BINARY_INV)
    kernel = np.ones((3,3))
    dilate_threholded_image = cv2.dilate(thresholded_image, kernel, iterations=1)
    bboxes= []
    labels = []
    with open('pred_boxes.pkl', 'rb') as file_boxes:
        bboxes = pickle.load(file_boxes)
    with open('pred_labels.pkl', 'rb') as file_labels:
        labels = pickle.load(file_labels)
    follow_lines(dilate_threholded_image, bboxes, labels)