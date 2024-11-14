from deep_learning.datasets.utils.transformations import collate_function_classificator
from deep_learning.datasets.dataset import process_data_classificator, balance_dataset
from deep_learning.datasets.utils.custom_dataset import PairedImageDataset
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader
from torchvision import transforms
import json


def transform_image_test(dims):
    transform = transforms.Compose([
            transforms.Grayscale(),
            transforms.Resize(dims),
            transforms.ToTensor(),
        ])
    return transform


def transform_image_train(dims):
    transform = transforms.Compose([
            transforms.Grayscale(),
            transforms.RandomVerticalFlip(),
            transforms.RandomHorizontalFlip(),
            transforms.Resize(dims),
            transforms.ToTensor(),
        ])
    return transform


def create_classificator_dataset(train_annotation_file: str, train_images_folder: str,
                                 test_annotation_file: str, test_images_folder: str,
                                 validation_proportion: float = 0.1, dims=(320, 320)):
    # Load train annotations
    f_train = open(train_annotation_file, 'r')
    train_annotation_data = json.load(f_train)
    f_train.close()
    # Load test annotations
    f_test = open(test_annotation_file, 'r')
    test_annotation_data = json.load(f_test)
    f_test.close()
    # Create and balance train and validation dataframe
    print("PROCESSING TRAIN DATA")
    df_train = process_data_classificator(train_annotation_data, train_images_folder)
    print("BALANCING TRAIN AND VALIDATION DATA")
    balanced_df_train = balance_dataset(df_train)
    train_set, valid_set = train_test_split(balanced_df_train, test_size=validation_proportion,
                                            stratify=balanced_df_train['label'])
    # Create test dataframe
    print("PROCESSING TEST DATA")
    df_test = process_data_classificator(test_annotation_data, test_images_folder)
    train_transform = transform_image_train(dims)
    test_transform = transform_image_test(dims)

    train_obj = PairedImageDataset(train_set, dims, train_transform)
    valid_obj = PairedImageDataset(valid_set, dims, test_transform)
    test_obj = PairedImageDataset(df_test, dims, test_transform)
    print("CREATING DATALOADERS")
    train_dataloader = DataLoader(train_obj, batch_size=128, shuffle=True,
                                  collate_fn=collate_function_classificator)
    validation_dataloader = DataLoader(valid_obj, batch_size=32, shuffle=True,
                                       collate_fn=collate_function_classificator)
    test_dataloader = DataLoader(test_obj, batch_size=32, shuffle=True,
                                 collate_fn=collate_function_classificator)

    return train_dataloader, validation_dataloader, test_dataloader
