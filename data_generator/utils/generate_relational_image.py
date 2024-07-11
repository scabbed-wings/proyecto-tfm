import matplotlib.pyplot as plt
import numpy as np


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


def crop_relations(image, bbox_origin, valid_objects):
    for index in range(len(valid_objects)):
        row = valid_objects.iloc[index]
        bbox_target = np.array([row['x_min'], row['y_min'], row['x_max'], row['y_max']], dtype=np.int32)
        copy_binary_image = image.copy()
        xmin, ymin, xmax, ymax = max_min_coordinates(bbox_origin, bbox_target)
        bbox_source, bbox_target = resize_boxes_2_crop(xmin, ymin, bbox_origin, 
                                                    bbox_target)
        copy_binary_image = copy_binary_image[ymin:ymax, xmin:xmax]
        plt.imshow(copy_binary_image, 'gray')
        plt.show()
    #return copy_binary_image, bbox_source, bbox_target
        

def crop_relational_image(image, labels_df):
    for index in range(len(labels_df)):
        row = labels_df.iloc[index]
        bbox_source = np.array([row['x_min'], row['y_min'], row['x_max'], row['y_max']], dtype=np.int32)
        related_objects = row.related_objects.strip('][').split(',')
        valid_objects = labels_df.loc[labels_df['class'] != row['class']]
        crop_relations(image, bbox_source, valid_objects)
        