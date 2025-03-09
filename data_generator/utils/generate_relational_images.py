import numpy as np
import cv2
from pathlib import Path
from data_generator.utils.balanced_counter import Balanced_Counter


def crop_labels(image_name, crop_name, label, bbox_source, bbox_target):
    return {
        "image_source": str(image_name),
        "image_crop": str(crop_name.name),
        "label": label,
        "bbox1": bbox_source,
        "bbox2": bbox_target
    }


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
    xmin = 0 if xmin < 0 else xmin
    ymin = 0 if ymin < 0 else ymin
    xmax = max(bbox1[2], bbox2[2])
    ymax = max(bbox1[3], bbox2[3])
    return xmin, ymin, xmax, ymax


def resize_boxes_2_crop(xmin, ymin, bbox1, bbox2):
    # Modificar el tamaño
    bbox1 = [int(bbox1[0] - xmin), int(bbox1[1] - ymin), int(bbox1[2] - xmin), int(bbox1[3] - ymin)]
    bbox2 = [int(bbox2[0] - xmin), int(bbox2[1] - ymin), int(bbox2[2] - xmin), int(bbox2[3] - ymin)]
    return bbox1, bbox2


def count_entity_relation_relations(df):
    count = 0
    for index in range(len(df)):
        related_objects = process_related_objects(df.iloc[index]['related_objects'])
        count += len(related_objects)
    return count


def get_equal_number_of_relation_types(labels_df):
    atributes_df = labels_df[labels_df['class'] == 1]
    relations_df = labels_df[labels_df['class'] == 2]
    num_entity_relation = count_entity_relation_relations(relations_df)
    return min(len(atributes_df), num_entity_relation)


def type_of_relation(source_class_id, target_class_id):
    relation_list = [source_class_id, target_class_id]
    atribute_relation = [0, 1]
    atribute_relation_relation = [1, 2]
    entity_relation_relation = [0, 2]
    reversed_relation = relation_list.copy()
    reversed_relation.reverse()
    if (relation_list == atribute_relation or reversed_relation == atribute_relation) or \
       (relation_list == atribute_relation_relation or reversed_relation == atribute_relation_relation):
        return 0
    elif relation_list == entity_relation_relation or reversed_relation == entity_relation_relation:
        return 1


def addition_check_on_type_relation(relation_type: int, balanced_counter: Balanced_Counter):
    if relation_type == 0 and balanced_counter.count_atribute_is_finished():
        return True
    elif relation_type == 1 and balanced_counter.count_entity_relation_is_finished():
        return True
    return False


def addition_on_type_relation(relation_type: int, balanced_counter: Balanced_Counter):
    if relation_type == 0:
        balanced_counter.add_count_atribute()
    elif relation_type == 1:
        balanced_counter.add_count_entity_relation()


def crop_relations(image, bbox_origin, valid_objects, origin_id, class_id_source, processed_relations,
                   output_path, balanced_counter: Balanced_Counter):
    labels = []
    for index in range(len(valid_objects)):
        row = valid_objects.iloc[index]
        relation = [row['id'], origin_id]
        relation_type = type_of_relation(class_id_source, row['class'])

        if not relation_is_processed(relation, processed_relations) and \
           not addition_check_on_type_relation(relation_type, balanced_counter):
            processed_relations.append(relation)
            crop_path = f"{output_path.parent}/{output_path.stem}_{len(processed_relations)}.png"
            bbox_target = process_bounding_box(row['x_min'], row['y_min'], row['x_max'], row['y_max'])
            target_relations = process_related_objects(row['related_objects'])
            label = 1 if origin_id in target_relations else 0
            copy_binary_image = image.copy()
            xmin, ymin, xmax, ymax = max_min_coordinates(bbox_origin, bbox_target)
            bbox_source, bbox_target = resize_boxes_2_crop(xmin, ymin, bbox_origin,
                                                           bbox_target)
            copy_binary_image = copy_binary_image[ymin:ymax, xmin:xmax]
            crop_label = crop_labels(output_path.name, Path(crop_path), label, bbox_source, bbox_target)
            labels.append(crop_label)
            cv2.imwrite(crop_path, copy_binary_image)
            if balanced_counter.count_or_not() and label == 1:
                addition_on_type_relation(relation_type, balanced_counter)
        if balanced_counter.is_finished():
            break

    return labels


def crop_relational_image(image, output_path, labels_df, balance_relations: bool):
    processed_relations = []
    processed_labels = []
    number_of_relations = get_equal_number_of_relation_types(labels_df) if balance_relations else None
    count_balancer = Balanced_Counter(number_of_relations)

    for index in range(len(labels_df)):
        row = labels_df.iloc[index]
        bbox_source = process_bounding_box(row['x_min'], row['y_min'], row['x_max'], row['y_max'])
        valid_objects = labels_df.loc[labels_df['class'] != row['class']]
        crop_labels = crop_relations(image, bbox_source, valid_objects, row['id'], row['class'],
                                     processed_relations, output_path, count_balancer)
        processed_labels += crop_labels
        if balance_relations and count_balancer.is_finished():
            count_balancer.print_counter()
            break
    return processed_labels
