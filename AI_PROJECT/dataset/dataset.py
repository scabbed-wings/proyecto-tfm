import shutil
from pathlib import Path
from glob import glob
from random import shuffle
from os.path import split, join
import torch
from os import makedirs
import pandas as pd
import numpy as np
import cv2

OG_WIDTH, OG_HEIGHT = 1181, 1545


def color_selector(class_id):
    if class_id == 0:
        return (255, 0, 0)
    elif class_id == 1:
        return (0, 255, 0)
    else:
        return (0, 0, 255)


def visualize_new_annotations(image_list, bboxes, classes, new_width, new_height):
    for id, image_name in enumerate(image_list):
        path = Path(image_name).with_suffix(".png")
        image = cv2.imread(str(path))
        image = cv2.resize(image, (new_width, new_height))
        for i in range(bboxes[id].shape[0]):
            print(bboxes[id][i])
            color = color_selector(classes[id][i])
            cv2.rectangle(image, (bboxes[id][i, 0], bboxes[id][i, 1]), (bboxes[id][i, 2], bboxes[id][i, 3]), color, 2)
        
        cv2.imshow("Annotations", image)
        cv2.waitKey(0)


def process_data(dataset_folder: str, output: str):
    image_list = glob(dataset_folder +"/*.png")
    output_list = []
    for file in image_list:
        img_path = Path(file)
        csv_path = img_path.with_suffix(".csv")
        abs_path = img_path.resolve()
        annotations = pd.read_csv(csv_path, sep=";", index_col=0)
        annotations["image_path"] = str(abs_path)
        output_list += annotations.values.tolist()
    
    return pd.DataFrame(output_list, columns=["x_min", "y_min", "x_max", "y_max", "class", "image_path"])


if __name__ == "__main__":
    dataset = "data_generator/img"
    output = "AI_PROJECT/output"
    df = process_data(dataset, output)
    print(df)