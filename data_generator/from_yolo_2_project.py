from glob import glob
import os
from pathlib import Path
import pandas as pd
from PIL import Image, ImageDraw
from shutil import copy2

COLS = ['x_min', 'y_min', 'x_max', 'y_max', 'class']

def img_has_labels(image_name: str, labels_list: list) -> int:
    for index, label in enumerate(labels_list):
        label_name = Path(label).stem
        if label_name == image_name:
            return index + 1
    return 0


def class_correspondency(class_id: int) -> int:
    if class_id == 0:
        return 1
    elif class_id == 1:
        return 0
    else:
        return class_id


def read_labels(label_path: str) -> pd.DataFrame:
    cols = ["class", "x", "y", "width", "height"]
    df = pd.read_csv(label_path, delim_whitespace=True, header=None, names=cols)
    return df


def color_selector(class_id) -> str:
    if class_id == 0:
        return "#3236a8"
    elif class_id == 1:
        return "#32a852"
    else:
        return "#a83236"


def draw_labels_on_image(image: Image, labels: pd.DataFrame, width: int, height: int):
    image_draw = ImageDraw.Draw(image)
    for index, row in labels.iterrows():
        if row["class"] != 3:
            x_mid = int(row['x'] * width)
            y_mid = int(row['y'] * height)
            label_width = int((row["width"] * width) / 2)
            label_height = int((row["height"] * height) / 2)
            class_id = int(row['class'])
            coords = [(x_mid - label_width, y_mid - label_width), (x_mid + label_width, y_mid + label_height)]
            color = color_selector(class_id)
            image_draw.rectangle(coords, outline=color)
    image.show()
        

def modify_labels_2_project(df: pd.DataFrame, width: int, height: int) -> pd.DataFrame:    
    new_list = []
    for index, row in df.iterrows():
        if row["class"] != 3:
            x_mid = int(row['x'] * width)
            y_mid = int(row['y'] * height)
            label_width = int((row["width"] * width) / 2)
            label_height = int((row["height"] * height) / 2)
            xmin = max(0, x_mid - label_width)
            ymin = max(0, y_mid - label_height)
            xmax = min(width, x_mid + label_width)
            ymax = min(height, y_mid + label_height)
            class_id = class_correspondency(int(row['class']))
            new_list.append([xmin, ymin, xmax, ymax, class_id])
    return pd.DataFrame(new_list, columns=COLS)


def transform_yolo_labels(input_folder: str, output_folder: str):
    image_folder = os.path.join(input_folder, "images/*.jpg")
    labels_folder = os.path.join(input_folder, "labels/*.txt")
    output_path = Path(output_folder)
    output_path.mkdir(parents=True, exist_ok=True)
    images_list = glob(image_folder)
    labels_list = glob(labels_folder)
    for img in images_list:
        img_name = Path(img).stem
        label_index = img_has_labels(img_name, labels_list)
        if label_index:
            label_name = labels_list[label_index - 1]
            df = read_labels(label_name)
            try: 
                image = Image.open(img)
            except:
                continue
            width, height = image.size
            print("Image: ", img, "Width: ", width, " Height: ", height)
            # draw_labels_on_image(image, df, width, height)
            new_labels = modify_labels_2_project(df, width, height)
            copy2(img, output_path)
            output_label_name = os.path.join(output_folder, f"{img_name}.csv")
            new_labels.to_csv(output_label_name, sep=";", columns=COLS, index=None)


if __name__ == "__main__":
    folder = "data_generator/Validation_Detection"
    output_folder = "data_generator/real_images"
    transform_yolo_labels(folder, output_folder)
