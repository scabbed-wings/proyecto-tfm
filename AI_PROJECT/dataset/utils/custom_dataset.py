import torch.utils
from torch.utils.data import Dataset, DataLoader
import cv2
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
        image = cv2.imread(self.tensors[0][idx])
        image = torch.tensor(image, dtype=torch.float32).permute(2, 0, 1)

        boxes = self.tensors[1][idx]
        labels = self.tensors[2][idx]

        if self.transform:
            image, boxes = self.transform(image, boxes)

        return (image, boxes, labels)


def get_mean(img_list):
    mean = np.array([0.,0., 0.])
    numSamples = len(img_list)
    for img_file in img_list:
        img = cv2.imread(img_file)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = img.astype(float) / 255.
        mean += np.mean(img)
        for j in range(3):
            mean[j] += np.mean(img[:,:,j])
    return (mean / numSamples)


def get_mean_std(dataset_folder):
    img_list = glob(dataset_folder + "/*.png")
    stdTemp = np.array([0.,0.,0.])
    std = np.array([0.,0., 0.])
    mean = get_mean(img_list)
    numSamples = len(img_list)
    for img_file in img_list:
        im = cv2.imread(img_file)
        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        im = im.astype(float) / 255.
        for j in range(3):
            stdTemp[j] += ((im[:,:,j] - mean[j])**2).sum()/(im.shape[0]*im.shape[1])
        
    std = np.sqrt(stdTemp / numSamples)

    return torch.from_numpy(mean), torch.from_numpy(std)


if __name__ == "__main__":
    transform = transforms.Compose([
        transforms.Resize((640, 640)),
        transforms.ToTensor(),
    ])

    dataset = BoundingBoxDataset('tu_archivo.csv', transform=transform)
    dataloader = DataLoader(dataset, batch_size=2, shuffle=True)

    for images, targets in dataloader:
        # Ahora puedes usar images y targets en tu modelo de PyTorch
        print(images.shape)
        print(targets['boxes'])
        print(targets['labels'])