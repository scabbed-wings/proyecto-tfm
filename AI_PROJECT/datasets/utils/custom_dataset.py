import torch.utils
from torch.utils.data import Dataset
from PIL import Image
import torch.utils.data
import torch
import numpy as np
from datasets.utils.transform.transform import transform
from models.utils import get_cuda_device

class CustomBBoxDataset(Dataset):
    def __init__(self, tensors, split, size=(300,300)):
        self.tensors = tensors
        self.split = split.upper()
        self.device = get_cuda_device()
        self.dims = size

        assert self.split in {'TRAIN', 'TEST'}

    
    def __len__(self):
        return self.tensors.shape[0]
    
    def __getitem__(self, idx):
        image = Image.open(self.tensors.iloc[idx, 0]).convert('L')
        boxes = torch.FloatTensor(self.tensors.iloc[idx, 1])
        labels = torch.IntTensor(self.tensors.iloc[idx, 2]).to(torch.int64)

        image, boxes, labels = transform(image, boxes, labels, split=self.split, dims=self.dims)
        targets = dict()
        targets['boxes'] = boxes
        targets['labels'] = labels

        return image, targets


class PairedImageDataset(Dataset):
    def __init__(self, image_dir1, image_dir2, labels, transform=None):
        self.image_dir1 = image_dir1
        self.image_dir2 = image_dir2
        self.labels = labels
        self.transform = transform
        self.image_names1 = os.listdir(image_dir1)
        self.image_names2 = os.listdir(image_dir2)

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        img1_path = os.path.join(self.image_dir1, self.image_names1[idx])
        img2_path = os.path.join(self.image_dir2, self.image_names2[idx])
        img1 = Image.open(img1_path).convert('RGB')
        img2 = Image.open(img2_path).convert('RGB')

        if self.transform:
            img1 = self.transform(img1)
            img2 = self.transform(img2)

        label = self.labels[idx]

        return img1, img2, label