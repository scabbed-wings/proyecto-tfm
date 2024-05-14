import torch.nn as nn


class ObjectDetection(nn.Module): 
    def __init__(self, in_channels=3, out_channels_cnn=3, bboxes=4):
        super().__init__()
        hidden_channel1 = 32
        hidden_channel2 = 64
        hidden_channel3 = 128
        kernel_size = 3
        stride = 1
        padding = 1
        self.conv1 = nn.Conv2d(in_channels=in_channels,
                               out_channels=hidden_channel1,
                               kernel_size=kernel_size,
                               stride=stride,
                               padding=padding)
        self.conv2 = nn.Conv2d(in_channels=hidden_channel1,
                               out_channels=hidden_channel2,
                               kernel_size=kernel_size,
                               stride=stride,
                               padding=padding)
        self.conv3 = nn.Conv2d(in_channels=hidden_channel2,
                               out_channels=hidden_channel2,
                               kernel_size=kernel_size,
                               stride=stride,
                               padding=padding)
        self.conv4 = nn.Conv2d(in_channels=hidden_channel2,
                               out_channels=hidden_channel3,
                               kernel_size=kernel_size,
                               stride=stride,
                               padding=padding)
        self.conv5 = nn.Conv2d(in_channels=hidden_channel3,
                               out_channels=hidden_channel3,
                               kernel_size=kernel_size,
                               stride=stride,
                               padding=padding)
        
        self.batchnorm1 = nn.BatchNorm2d(hidden_channel1)
        self.batchnorm2 = nn.BatchNorm2d(hidden_channel2)
        self.batchnorm3 = nn.BatchNorm2d(hidden_channel3)
        self.maxpool = nn.MaxPool2d(kernel_size=2)
        self.relu = nn.ReLU()
        self.fc = nn.Flatten()
        self.cnn_layer = nn.Linear(7*7*128, out_channels_cnn)
        self.regressor = nn.Linear(7*7*128, bboxes)

    def cnn_layers(self, x):
        x = self.relu(x)
        x = self.maxpool(x)
        return x
    
    def feature_extractor(self, x):
        x = self.conv1(x)
        x = self.batchnorm1(x)
        x = self.cnn_layers(x)
#         print(x.shape)
        
        x = self.conv2(x)
        x = self.batchnorm2(x)
        x = self.cnn_layers(x)
#         print(x.shape)      
        x = self.conv3(x)
        x = self.batchnorm2(x)
        x = self.cnn_layers(x)
#         print(x.shape)
        x = self.conv4(x)
        x = self.batchnorm3(x)
        x = self.cnn_layers(x)
#         print(x.shape)
        x = self.conv5(x)
        x = self.batchnorm3(x)
        x = self.cnn_layers(x)
#         print(x.shape)
        x = self.fc(x)
#         print(x.shape)
        return x
    
    def forward(self, x):
        x = self.feature_extractor(x)
        classifier_op = self.cnn_layer(x)
        regressor_op = self.regressor(x)
        return (regressor_op, classifier_op)
#         out = torch.concat([classifier_op, regressor_op])
#         return out
