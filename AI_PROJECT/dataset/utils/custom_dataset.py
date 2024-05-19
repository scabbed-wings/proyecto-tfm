import torch.utils
from torch.utils.data import Dataset
from PIL import Image
import torch.utils.data
import torch
import numpy as np


class BoundingBoxDataset(Dataset):
    def __init__(self, tensors, transforms=None):
        self.tensors = tensors
        self.transform = transforms

    def __len__(self):
        return self.tensors[0].shape[0]
    
    def __getitem__(self, idx):

        image = np.array(Image.open(self.tensors[0][idx]).convert('L'))
        #image = torch.tensor(image, dtype=torch.float32).permute(2, 0, 1)
        image = torch.tensor(image, dtype=torch.float32)
        boxes = self.tensors[1][idx]
        labels = self.tensors[2][idx]

        if self.transform:
            image = self.transform(image)

        return (image, boxes, labels)


class CustomBBoxDataset(Dataset):
    def __init__(self, tensors):
        self.tensors = tensors
    
    def __len__(self):
        return self.tensors[0].shape[0]
    
    def __getitem__(self, idx):
        image = np.array(Image.open(self.tensors[0][idx]).convert('L'))
        image = torch.tensor(image, dtype=torch.float32)
        boxes = torch.FloatTensor(self.tensors[1][idx])
        labels = torch.FloatTensor(self.tensors[2][idx])
        