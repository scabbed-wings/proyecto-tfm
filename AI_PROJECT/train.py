from model.model import ObjectDetection
from model.utils import get_cuda_device
from dataset.dataset import get_torch_dataloader
import torch
import tqdm


def setup_stage():


def train(epochs, LR=0.001):
    device = get_cuda_device()
    model = ObjectDetection(in_channels=3, out_channels_cnn=3, bboxes=4)
    model.to(device)

    classification_loss = torch.nn.CrossEntropyLoss()
    bbox_loss = torch.nn.MSELoss()
    opt = torch.optim.Adam(model.parameters(), lr=LR)

    train_loss = []
    train_accuracy = []
    test_loss = []
    test_accuracy = []

    for epoch in tqdm(range(epochs)):
        correct = 0
        iter = 0
        iter_loss = 0
        model.train()


if __name__ == "__main__":
    train(10)
