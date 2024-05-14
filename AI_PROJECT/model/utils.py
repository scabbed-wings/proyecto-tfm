import torch


def get_cuda_device():
    return torch.device('cuda' if torch.cuda.is_available() else "cpu")
