import torch
import torchvision.models as models

class PairedImageClassifier(torch.nn.Module):
    def __init__(self):
        super(PairedImageClassifier, self).__init__()
        self.resnet = models.resnet18(pretrained=True)

        # Eliminar la última capa fc de ResNet
        self.resnet = torch.nn.Sequential(*list(self.resnet.children())[:-1])

        # Nueva capa fully connected para la clasificación binaria
        self.fc = torch.nn.Linear(512 * 2, 1)

    def forward(self, img1, img2):
        x1 = self.resnet(img1)
        x2 = self.resnet(img2)

        x1 = x1.view(x1.size(0), -1)
        x2 = x2.view(x2.size(0), -1)

        x = torch.cat((x1, x2), dim=1)
        x = self.fc(x)

        return x