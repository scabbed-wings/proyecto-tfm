from torch.utils.data import Dataset, DataLoader
from PIL import Image
import pandas as pd
import torchvision.transforms as T
import torch

class BoundingBoxDataset(Dataset):
    def __init__(self, dataframe, transform=None):
        self.data = dataframe
        self.transform = transform

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        img_path = self.data.iloc[idx, 0]
        image = Image.open(img_path).convert("RGB")

        boxes = []
        labels = []
        for i in range(len(self.data)):
            if self.data.iloc[idx, 0] == img_path:
                xmin = self.data.iloc[idx, 1]
                ymin = self.data.iloc[idx, 2]
                xmax = self.data.iloc[idx, 3]
                ymax = self.data.iloc[idx, 4]
                boxes.append([xmin, ymin, xmax, ymax])
                labels.append(self.data.iloc[idx, 5])

        boxes = torch.as_tensor(boxes, dtype=torch.float32)
        labels = torch.as_tensor(labels)

        target = {
            'boxes': boxes,
            'labels': labels
        }

        if self.transform:
            image, target = self.transform(image, target)

        return image, target



transform = T.Compose([
    T.Resize((300, 300)),
    T.ToTensor(),
])

dataset = BoundingBoxDataset('tu_archivo.csv', transform=transform)
dataloader = DataLoader(dataset, batch_size=2, shuffle=True)

for images, targets in dataloader:
    # Ahora puedes usar images y targets en tu modelo de PyTorch
    print(images.shape)
    print(targets['boxes'])
    print(targets['labels'])