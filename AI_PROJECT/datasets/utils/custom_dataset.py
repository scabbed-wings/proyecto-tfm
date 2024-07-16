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
    def __init__(self, data, size=(300,300), transform=None):
        self.data = data
        self.transform = transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        
        image_source = Image.open(self.data.iloc[idx, 0]).convert('L')
        image_crop = Image.open(self.data.iloc[idx, 1]).convert('L')
        label = torch.tensor(self.data.iloc[idx, 2], dtype=torch.float32)
        bbox1 = torch.IntTensor(self.data.iloc[idx, 3]).to(torch.int64)
        bbox2 = torch.IntTensor(self.data.iloc[idx, 4]).to(torch.int64)

        if self.transform:
            image = self.transform(image_source)
            crop = self.transform(image_crop)


        return image, crop, label