from datasets.utils.transformations import collate_function_classificator
from datasets.dataset import process_data_classificator, balance_dataset
from datasets.utils.custom_dataset import PairedImageDataset
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader
from torchvision import transforms
import json


def create_classificator_dataset(annotation_file: str, images_folder: str, 
                                 validation_proportion: float = 0.1, dims=(320,320)):
    
    f = open(annotation_file, 'r')
    annotation_data = json.load(f)
    f.close()
    df = process_data_classificator(annotation_data, images_folder)
    balanced_df = balance_dataset(df)
    train_set, valid_set = train_test_split(balanced_df, test_size=validation_proportion,
                                            stratify=balanced_df['label'])
    transform = transforms.Compose([
        transforms.Grayscale(),
        transforms.Resize(dims),
        transforms.ToTensor(),
    ])
    train_obj = PairedImageDataset(train_set, dims, transform)
    valid_obj = PairedImageDataset(valid_set, dims, transform)
    train_dataloader = DataLoader(train_obj, batch_size=32, shuffle=True, 
                            collate_fn=collate_function_classificator)
    validation_dataloader = DataLoader(valid_obj, batch_size=32, shuffle=True, 
                            collate_fn=collate_function_classificator)
    
    return train_dataloader, validation_dataloader
