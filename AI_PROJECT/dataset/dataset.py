from pathlib import Path
from glob import glob
import torch
import pandas as pd
import cv2
from sklearn.model_selection import train_test_split
from utils.custom_dataset import get_mean_std, BoundingBoxDataset
from utils.transformations import get_transforms
from torch.utils.data import DataLoader

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
        image = cv2.imread(str(path))
        image = cv2.resize(image, (new_width, new_height))
        for i in range(bboxes[id].shape[0]):
            print(bboxes[id][i])
            color = color_selector(classes[id][i])
            cv2.rectangle(image, (bboxes[id][i, 0], bboxes[id][i, 1]),
                          (bboxes[id][i, 2], bboxes[id][i, 3]), color, 2)
        cv2.imshow("Annotations", image)
        cv2.waitKey(0)


def process_data(dataset_folder: str, 
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


def get_torch_dataloader(batch_size=32, img_width=640, img_height=640,
                         dataset="data_generator/img"):
    print("Processing data")
    df = process_data(dataset)
    print("Splitting data")
    train_set, test_set = train_test_split(df, test_size=0.1,
                                           shuffle=True, stratify=df["class"])
    print("Creating tensors")
    train_images = train_set["image_path"].values
    test_images = test_set["image_path"].values

    train_labels = torch.from_numpy(train_set['class'].values)
    test_labels = torch.from_numpy(test_set['class'].values)

    train_bbox = torch.from_numpy(train_set[['x_min', 'x_max',
                                             'y_min', 'y_max']].values)
    test_bbox = torch.from_numpy(test_set[['x_min', 'x_max',
                                           'y_min', 'y_max']].values)
    print("Getting normalized vectors")
    mean, std = get_mean_std(dataset)
    train_transform, test_transform = get_transforms(img_height=img_height,
                                                     img_width=img_width,
                                                     mean=mean, std=std)
    print("Creating train and test sets")
    trainset = BoundingBoxDataset((train_images, train_labels, train_bbox),
                                  transforms=train_transform)
    testset = BoundingBoxDataset((test_images, test_labels, test_bbox),
                                 transforms=test_transform)
    print("Creating dataloader objects")
    train_data_loader = DataLoader(trainset, batch_size, shuffle=True)
    test_data_loader = DataLoader(testset, batch_size, shuffle=True)
    
    return train_data_loader, test_data_loader
