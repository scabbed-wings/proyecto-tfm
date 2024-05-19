import torch.utils
from torch.utils.data import Dataset, DataLoader
import cv2
from PIL import Image
import pandas as pd
import torch.utils.data
from torchvision import transforms
import torch
from glob import glob
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


def get_mean(img_list):
    mean = 0
    numSamples = len(img_list)
    for img_file in img_list:
        img = cv2.imread(img_file)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img.astype(float) / 255.
        mean += np.mean(img)
    return (mean / numSamples)


def get_mean_std(dataset_folder):
    img_list = glob(dataset_folder + "/*.png")
    stdTemp = 0
    std = 0
    mean = get_mean(img_list)
    numSamples = len(img_list)
    for img_file in img_list:
        im = cv2.imread(img_file)
        im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        im = im.astype(float) / 255.
        stdTemp += ((im - mean)**2).sum() / (im.shape[0] * im.shape[1])

        
    std = np.sqrt(stdTemp / numSamples)
    print("MEAN: ", (mean, ), " STD: ", (std, ))
    return mean, std