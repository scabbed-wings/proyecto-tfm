import torch
from datasets.dataset import process_data_classificator, balance_dataset
from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
import json
import os



transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# Ejemplo de inicialización
# image_dir1 = 'path/to/first/image/directory'
# image_dir2 = 'path/to/second/image/directory'
# labels = [0, 1, 0, 1, ...]  # Ejemplo de etiquetas binarias
# 
# dataset = PairedImageDataset(image_dir1, image_dir2, labels, transform=transform)
# dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

def create_classificator_dataset(annotation_file: str, images_folder: str, 
                                 validation_proportion: float = 0.1):
    
    f = open(annotation_file, 'r')
    annotation_data = json.load(f)
    f.close()
    df = process_data_classificator(annotation_data, images_folder)
    balanced_df = balance_dataset(df)
    train_set, valid_set = train_test_split(balanced_df, test_size=validation_proportion,
                                            stratify=balanced_df['label'])
        