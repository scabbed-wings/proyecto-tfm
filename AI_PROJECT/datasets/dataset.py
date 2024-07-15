from pathlib import Path
from glob import glob
import torch
import pandas as pd
import numpy as np
import cv2
import os
from sklearn.model_selection import train_test_split
from datasets.utils.transformations import get_transforms, get_mean_std
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt

OG_WIDTH, OG_HEIGHT = 1181, 1545


def color_selector(class_id):
    if class_id == 0:
        return (255, 0, 0)
    elif class_id == 1:
        return (0, 255, 0)
    else:
        return (0, 0, 255)


def visualize_new_annotations(image_list, bboxes, classes,
                              new_width: int, new_height: int):
    for id, image_name in enumerate(image_list):
        path = Path(image_name).with_suffix(".png")
        image = cv2.imread(fr"{str(path)}")
        image = cv2.resize(image, (new_width, new_height))
        for i in range(bboxes[id].shape[0]):
            print(bboxes[id][i])
            color = color_selector(classes[id][i])
            cv2.rectangle(image, (bboxes[id][i, 0], bboxes[id][i, 1]),
                          (bboxes[id][i, 2], bboxes[id][i, 3]), color, 2)
        cv2.imshow("Annotations", image)
        cv2.waitKey(0)


def visualize_images(image, bboxes, labels, inference: bool = False, box_index=False):
    array = image.numpy()
    array = np.transpose(array, (1,2,0))
    array = cv2.cvtColor(array, cv2.COLOR_GRAY2RGB)
    bboxes = bboxes.numpy()
    labels =labels.numpy()
    for i in range(bboxes.shape[0]):
            new_bboxes = 300 * bboxes[i] if not inference else bboxes[i]
            # print(new_bboxes)
            color = color_selector(int(labels[i])) if not inference else color_selector(int(labels[i]-1))
            cv2.rectangle(array, (int(new_bboxes[0]), int(new_bboxes[1])),
                          (int(new_bboxes[2]), int(new_bboxes[3])), color, 2)
            if box_index:
                centroid = (int(new_bboxes[0]), int(new_bboxes[1]))
                cv2.putText(array, f"id {i}", centroid, cv2.FONT_HERSHEY_COMPLEX, 0.7, (20, 117, 255), 2)
    plt.imshow(array)
    plt.show()


def process_data_box_unit(dataset_folder: str, 
                 new_width: int = 640, new_height: int = 640):
    image_list = glob(dataset_folder + "/*.png")
    output_list = []
    for file in image_list:
        img_path = Path(file)
        csv_path = img_path.with_suffix(".csv")
        abs_path = img_path.resolve()
        annotations = pd.read_csv(csv_path, sep=";", index_col=0)
        annotations["image_path"] = str(abs_path)
        annotations[["x_min", "x_max"]] = (annotations[["x_min", "x_max"]] / OG_WIDTH) * new_width
        annotations[["y_min", "y_max"]] = (annotations[["y_min", "y_max"]] / OG_HEIGHT) * new_height
        output_list += annotations.values.tolist()
    return pd.DataFrame(output_list, columns=["x_min", "y_min", "x_max",
                                              "y_max", "class", "image_path"])


def process_data_bboxes(dataset_folder: str, not_background: bool = True):
    image_list = glob(dataset_folder + "/*.png")
    output_list = []
    for file in image_list:
        img_path = Path(file)
        csv_path = img_path.with_suffix(".csv")
        abs_path = img_path.resolve()
        annotations = pd.read_csv(csv_path, sep=";", index_col=0)
        bboxes = annotations[["x_min", "y_min", "x_max", "y_max"]].values
        labels = annotations["class"].values + 1 if not_background else annotations["class"].values
        output_list.append([abs_path, bboxes, labels])
    return pd.DataFrame(output_list, columns=["img_path", "bboxes", "labels"])


def process_data_classificator(annotation_data: list, images_folder: str):
    dataframe_list = []
    for annotation in annotation_data:
        crop_path = Path(os.path.join(images_folder, annotation['image_crop']))
        image_path = Path(os.path.join(images_folder, annotation['image_source']))
        dataframe_list.append([image_path, crop_path, annotation['label'], annotation['bbox1'], 
                               annotation['bbox2']])
    return pd.DataFrame(dataframe_list, columns=['image_source', 'image_crop', 'label', 'bbox1', 'bbox2'])


def balance_dataset(df: pd.DataFrame, target_column: str = 'label'):
    min_class_size = df[target_column].value_counts().min()
    # Separar las clases mayoritaria y minoritaria
    df_minority = df[df[target_column] == df[target_column].value_counts().idxmin()]
    df_majority = df[df[target_column] == df[target_column].value_counts().idxmax()]

    df_majority_downsampled = df_majority.sample(n=min_class_size)

    df_resampled = pd.concat([df_minority, df_majority_downsampled])

    return df_resampled
