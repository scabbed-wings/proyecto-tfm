import matplotlib.pyplot as plt
import numpy as np
import cv2


def process_related_objects(related_objects_string: str):
    new_list = related_objects_string.strip('][').split(',')
    return [int(x) for x in new_list]


def process_bounding_box(xmin, ymin, xmax, ymax):
    return np.array([xmin, ymin, xmax, ymax], dtype=np.int32)


def relation_is_processed(relation: list, processed_relations: list):
    for proc_relation in processed_relations:
        reversed_relation = proc_relation.copy()
        reversed_relation.reverse()
        if relation == proc_relation or relation == reversed_relation:
            return True
    return False


def max_min_coordinates(bbox1, bbox2):
    xmin = min(bbox1[0], bbox2[0])
    ymin = min(bbox1[1], bbox2[1])
    xmax = max(bbox1[2], bbox2[2])
    ymax = max(bbox1[3], bbox2[3])
    return xmin, ymin, xmax, ymax


def resize_boxes_2_crop(xmin, ymin, bbox1, bbox2):
    # Modificar el tamaño
    bbox1 = [int(bbox1[0] - xmin), int(bbox1[1] - ymin), int(bbox1[2] - xmin), int(bbox1[3] - ymin)]
    bbox2 = [int(bbox2[0] - xmin), int(bbox2[1] - ymin), int(bbox2[2] - xmin), int(bbox2[3] - ymin)]
    return bbox1, bbox2


def crop_relations(image, bbox_origin, valid_objects, 
                   origin_id, processed_relations, output_path):
    for index in range(len(valid_objects)):
        row = valid_objects.iloc[index]
        relation = [row['id'], origin_id]
        if not relation_is_processed(relation, processed_relations):
            processed_relations.append(relation)
            crop_path = f"{output_path.parent}/{output_path.stem}_{len(processed_relations)}.png"
            print("Crop path: ", crop_path)
            bbox_target = process_bounding_box(row['x_min'], row['y_min'], row['x_max'], row['y_max'])
            target_relations = process_related_objects(row['related_objects'])
            label = 1 if origin_id in target_relations else 0
            copy_binary_image = image.copy()
            xmin, ymin, xmax, ymax = max_min_coordinates(bbox_origin, bbox_target)
            bbox_source, bbox_target = resize_boxes_2_crop(xmin, ymin, bbox_origin,
                                                        bbox_target)
            copy_binary_image = copy_binary_image[ymin:ymax, xmin:xmax]
            # cv2.imwrite(crop_path, copy_binary_image)
            # plt.imshow(copy_binary_image, 'gray')
            # plt.show()
    #return copy_binary_image, bbox_source, bbox_target
        

def crop_relational_image(image, output_path, labels_df):
    processed_relations = []
    for index in range(len(labels_df)):
        row = labels_df.iloc[index]
        bbox_source = process_bounding_box(row['x_min'], row['y_min'], row['x_max'], row['y_max'])
        valid_objects = labels_df.loc[labels_df['class'] != row['class']]
        crop_relations(image, bbox_source, valid_objects, row['id'], 
                       processed_relations, output_path)
        