import torch
import torchvision.models as models
from torchvision.models.mobilenetv3 import MobileNet_V3_Small_Weights


class PairedImageClassifier(torch.nn.Module):
    def __init__(self):
        super(PairedImageClassifier, self).__init__()
        self.mobilenet = models.mobilenet_v3_small(weights=MobileNet_V3_Small_Weights.DEFAULT)
        self.mobilenet.features[0][0] = torch.nn.Conv2d(1, 16, kernel_size=(3, 3),
                                                        stride=(2, 2),
                                                        padding=(1, 1), bias=False)
        self.features = self.mobilenet.features
        self.avgpool = torch.nn.AdaptiveAvgPool2d((1, 1))

        self.fc = torch.nn.Linear(576 * 2, 1)

    def forward(self, img1, img2):
        x1 = self.features(img1)
        x1 = self.avgpool(x1)
        x1 = x1.view(x1.size(0), -1)

        x2 = self.features(img2)
        x2 = self.avgpool(x2)
        x2 = x2.view(x2.size(0), -1)

        # print(f"x1 shape: {x1.shape}, x2 shape: {x2.shape}")
        x = torch.cat((x1, x2), dim=1)
        x = self.fc(x)

        return x
