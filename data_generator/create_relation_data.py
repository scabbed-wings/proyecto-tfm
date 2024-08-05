from glob import glob
from pathlib import Path
import pandas as pd
import numpy as np
from PIL import Image
import os
import json
from utils.generate_relational_images import crop_relational_image
import cv2


def create_relational_data(input_path: str, output_path: str, balance_relations: bool = False):
    output_parent = Path(output_path)
    crops_path = Path(os.path.join(output_parent, 'images'))
    labels_path = Path(os.path.join(output_parent, 'labels.json'))
    output_parent.mkdir(parents=True, exist_ok=True)
    crops_path.mkdir(parents=True, exist_ok=True)
    images_list = glob(input_path + "/*.png")
    dataset_labels = []

    for image_name in images_list:
        print("Processing image: ", image_name)
        image_path = Path(image_name)
        output_path = Path(os.path.join(crops_path), image_path.name)
        csv_path = f"{image_path.parent}/{image_path.stem}.csv"
        image = Image.open(image_path).convert('L')
        image = np.array(image)
        df = pd.read_csv(csv_path, sep=";")
        cv2.imwrite(str(output_path), image)
        image_crops_labels = crop_relational_image(image, output_path, df, balance_relations)
        dataset_labels += image_crops_labels

    with open(labels_path, 'w', encoding='utf-8') as f:
        json.dump(dataset_labels, f, indent=4)


if __name__ == "__main__":
    train_path = "data_generator/img_fractional"
    train_output_parent = "data_generator/train_relational_images"
    test_path = "data_generator/test"
    test_output_parent = "data_generator/test_relational_images"
    create_relational_data(train_path, train_output_parent, balance_relations=True)
    create_relational_data(test_path, test_output_parent)
