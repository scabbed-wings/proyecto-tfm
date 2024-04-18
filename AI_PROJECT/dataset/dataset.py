import shutil
from pathlib import Path
from glob import glob
from random import shuffle
from os.path import split, join
from os import makedirs
import pandas as pd

def save_subset(files:list, output_folder:str, subset_type:str):
    output_path = join(Path(output_folder, subset_type))
    makedirs(output_path, exist_ok=True)
    for file in files:
        file_path = Path(file)
        parent = split(file_path)[0]
        file_name = split(file_path)[1][:-4]
        annotations = join(Path(parent), file_name + "_labels.csv")
        shutil.copy2(file_path, output_path)
        shutil.copy2(annotations, output_path)


def create_dataset(dataset_folder:str,
                   output_folder:str, 
                   test_split:float, 
                   val_split:float):
    
    image_list = glob(dataset_folder +"/*.png")
    shuffle(image_list)
    test_subset = image_list[-int(len(image_list) * test_split):]
    train_val = image_list[:-int(len(image_list) * test_split)]
    val_subset = train_val[-int(len(train_val) * val_split):]
    train_subset = train_val[:-int(len(train_val) * val_split)]

    save_subset(test_subset, output_folder, "test")
    save_subset(val_subset, output_folder, "val")
    save_subset(train_subset, output_folder, "train")

def get_vectors(ann_list: list):
    bbox, classes = [], []

    for elem in ann_list:
        data = pd.read_csv(elem, sep=";")
        bbox.append(data[["x_min", "y_min", "x_max", "y_max"]].to_numpy())
        classes.append(data["class"].to_numpy())
    
    print(bbox, classes)

def process_data(folder:str, width:int = 640, height:int = 640):
    
    train_ann = glob(folder + "/train/*.csv")
    val_ann = glob(folder + "/val/*.csv")
    test_ann = glob(folder + "/test/*.csv")

    get_vectors(test_ann)





    

if __name__ == "__main__":
    dataset = "data_generator/img"
    output = "AI_PROJECT/output"
    #create_dataset(dataset, output, 0.1, 0.2)
    process_data(output)