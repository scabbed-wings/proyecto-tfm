import cv2
import matplotlib.pyplot as plt
from visual_relation_detector.src.utils import max_min_coordinates, already_detected


def relation_is_valid(label_source, label_target):
    if label_source == 1 and (label_target in [2, 3]):
        return True
    elif label_source == 2 and (label_target in [1, 3]):
        return True
    elif label_source == 3 and (label_target in [1, 2]):
        return True
    else:
        return False


def border_boxes_points(bbox_coords):
    border_points = []
    # Todos los puntos a lo ancho del rectangulo por arriba y abajo
    for i in range(bbox_coords[0], bbox_coords[2] + 1):
        border_points.append((i, bbox_coords[1]))
        border_points.append((i, bbox_coords[3]))
    # Todos los puntos a lo alto del rectangulo por izquierda y derecha
    for j in range(bbox_coords[1], bbox_coords[3] + 1):
        border_points.append((bbox_coords[0], j))
        border_points.append((bbox_coords[2], j))
    return border_points


def resize_boxes_2_crop(xmin, ymin, bbox1, bbox2):
    bbox1 = bbox1.int().numpy()
    bbox2 = bbox2.int().numpy()
    # Modificar el tamaño
    bbox1 = [int(bbox1[0] - xmin), int(bbox1[1] - ymin), int(bbox1[2] - xmin), int(bbox1[3] - ymin)]
    bbox2 = [int(bbox2[0] - xmin), int(bbox2[1] - ymin), int(bbox2[2] - xmin), int(bbox2[3] - ymin)]
    # Proporcionar los puntos de los bordes
    # bbox1 = border_boxes_points(bbox1)
    # bbox2 = border_boxes_points(bbox2)
    # Proporcionar las esquinas
    bbox1 = [(bbox1[0], bbox1[1]), (bbox1[0], bbox1[3]), (bbox1[2], bbox1[1]), (bbox1[2], bbox1[3])]
    bbox2 = [(bbox2[0], bbox2[1]), (bbox2[0], bbox2[3]), (bbox2[2], bbox2[1]), (bbox2[2], bbox2[3])]
    return bbox1, bbox2


def check_points_in_contour(contours, bbox1, bbox2):
    combinations = [(p1, p2) for p1 in bbox1 for p2 in bbox2 if p1 != p2]
    not_contained = False
    for combination in combinations:
        for contour in contours:
            p1_in = cv2.pointPolygonTest(contour, combination[0], False)
            p2_in = cv2.pointPolygonTest(contour, combination[1], False)
            if p1_in >= 0 and p2_in >= 0:
                not_contained = True
                break
        if not_contained:
            break
    return not_contained


def crop_outsider_elements(bboxes, binary_image, index_source, index_target):
    copy_binary_image = binary_image.copy()
    for ind, bbox in enumerate(bboxes):
        if ind != index_source and ind != index_target:
            bbox_to_crop = bbox.int()
            copy_binary_image[bbox_to_crop[1]:bbox_to_crop[3],
                              bbox_to_crop[0]:bbox_to_crop[2]] = 0
        elif ind == index_source or ind == index_target:
            bbox_to_fill = bbox.int()
            copy_binary_image[bbox_to_fill[1]:bbox_to_fill[3],
                              bbox_to_fill[0]:bbox_to_fill[2]] = 255
    xmin, ymin, xmax, ymax = max_min_coordinates(bboxes[index_source], bboxes[index_target])
    bbox_source, bbox_target = resize_boxes_2_crop(xmin, ymin, bboxes[index_source],
                                                   bboxes[index_target])
    copy_binary_image = copy_binary_image[ymin:ymax, xmin:xmax]
    # plt.imshow(copy_binary_image, 'gray')
    # plt.show()
    return copy_binary_image, bbox_source, bbox_target


def follow_lines(binary_image, bboxes, labels):
    found_relations = []
    for index_source, _ in enumerate(bboxes):
        bbox_source_label = labels[index_source]
        for index_target, _ in enumerate(bboxes):
            bbox_target_label = labels[index_target]
            if relation_is_valid(bbox_source_label, bbox_target_label) and not already_detected(index_target,
                                                                                                index_source,
                                                                                                found_relations):
                cropped_binary, bbox_source, bbox_target = crop_outsider_elements(bboxes, binary_image,
                                                                                  index_source, index_target)
                contours = cv2.findContours(cropped_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
                contours = contours[0] if len(contours) == 2 else contours[1]
                if check_points_in_contour(contours, bbox_source, bbox_target):
                    found_relations.append([index_source, index_target])
    return found_relations
