import torch.utils
from torch.utils.data import Dataset
from PIL import Image
import torch.utils.data
import torch
import numpy as np
from datasets.utils.transform.transform import transform
from models.utils import get_cuda_device


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
        