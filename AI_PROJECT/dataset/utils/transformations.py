from torchvision import transforms
import cv2
from glob import glob
import numpy as np

def get_transforms(img_height, img_width, mean, std):

    train_transform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((img_height, img_width)),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize(mean, std)
    ])

    test_transform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((img_height, img_width)),
        transforms.ToTensor(),
        transforms.Normalize(mean, std)
    ])

    return train_transform, test_transform

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
    return mean, std