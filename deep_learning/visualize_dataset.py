from os.path import isdir, isfile
from glob import glob
from pathlib import Path
from deep_learning.datasets.dataset import color_selector
import pandas as pd
import numpy as np
import cv2


def show_image(image_name: str, bboxes: np.ndarray, labels: np.ndarray, ids: np.ndarray, related_objects: np.ndarray):
    image = cv2.imread(image_name)
    for i in range(bboxes.shape[0]):
        color = color_selector(labels[i])
        cv2.rectangle(image, (bboxes[i, 0], bboxes[i, 1]),
                      (bboxes[i, 2], bboxes[i, 3]), color, 2)
        centroid = (int(bboxes[i, 0]), int(bboxes[i, 1]))
        cv2.putText(image, f"id {ids[i]}-{related_objects[i]}",
                    centroid, cv2.FONT_HERSHEY_COMPLEX, 0.7, (20, 117, 255), 2)
    cv2.imshow("Annotations", image)
    cv2.waitKey(0)


def visualize_dataset(dataset_path: str):
    if isdir(dataset_path):
        image_list = glob(dataset_path + "/*.png") + glob(dataset_path + "/*.jpg")
        for image_name in image_list:
            img_path = Path(image_name)
            csv_path = img_path.with_suffix(".csv")
            if not isfile(csv_path):
                raise IsADirectoryError(f'''{csv_path} is a directory and not a CSV file''')
            annotations = pd.read_csv(csv_path, sep=";", index_col=0)
            bboxes = annotations[["x_min", "y_min", "x_max", "y_max"]].values
            labels = annotations["class"].values
            element_ids = annotations["id"].values
            related_objects = annotations["related_objects"].values
            show_image(image_name, bboxes, labels, element_ids, related_objects)
    else:
        raise NotADirectoryError(f'{dataset_path} is not a directory')


if __name__ == "__main__":
    visualize_dataset(r'data_generator\real_sample_images')
