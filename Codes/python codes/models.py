import torch
import torch.nn as nn

class AirNet(nn.Module):
    def __init__(self, nchannels=6, nclasses=5, preprocessing=False):
        super(AirNet, self).__init__()
        self.nhidden1 = 64
        self.nhidden2 = 512
        self.preprocessing = preprocessing
        if self.preprocessing:
            nchannels += 2
        self.conv1 = nn.Conv1d(in_channels=nchannels, out_channels=self.nhidden1, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm1d(self.nhidden1)
        self.relu1 = nn.ReLU()

        self.conv2 = nn.Conv1d(in_channels=self.nhidden1, out_channels=self.nhidden1, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm1d(self.nhidden1)
        self.relu2 = nn.ReLU()
        self.pool1 = nn.MaxPool1d(kernel_size=2)

        self.conv3 = nn.Conv1d(in_channels=self.nhidden1, out_channels=self.nhidden1, kernel_size=3, padding=1)
        self.bn3 = nn.BatchNorm1d(self.nhidden1)
        self.relu3 = nn.ReLU()

        self.conv4 = nn.Conv1d(in_channels=self.nhidden1, out_channels=self.nhidden1, kernel_size=3, padding=1)
        self.bn4 = nn.BatchNorm1d(self.nhidden1)
        self.relu4 = nn.ReLU()
        self.pool2 = nn.MaxPool1d(kernel_size=2)

        self.conv5 = nn.Conv1d(in_channels=self.nhidden1, out_channels=self.nhidden1, kernel_size=3, padding=1)
        self.bn5 = nn.BatchNorm1d(self.nhidden1)
        self.relu5 = nn.ReLU()

        self.conv6 = nn.Conv1d(in_channels=self.nhidden1, out_channels=self.nhidden1, kernel_size=3, padding=1)
        self.bn6 = nn.BatchNorm1d(self.nhidden1)
        self.relu6 = nn.ReLU()
        self.pool3 = nn.MaxPool1d(kernel_size=2)

        self.conv7 = nn.Conv1d(in_channels=self.nhidden1, out_channels=self.nhidden1, kernel_size=3, padding=1)
        self.bn7 = nn.BatchNorm1d(self.nhidden1)
        self.relu7 = nn.ReLU()

        self.conv8 = nn.Conv1d(in_channels=self.nhidden1, out_channels=self.nhidden1, kernel_size=3, padding=1)
        self.bn8 = nn.BatchNorm1d(self.nhidden1)
        self.relu8 = nn.ReLU()
        self.pool4 = nn.MaxPool1d(kernel_size=2)

        self.conv9 = nn.Conv1d(in_channels=self.nhidden1, out_channels=self.nhidden1, kernel_size=3, padding=1)
        self.bn9 = nn.BatchNorm1d(self.nhidden1)
        self.relu9 = nn.ReLU()

        self.conv10 = nn.Conv1d(in_channels=self.nhidden1, out_channels=self.nhidden1, kernel_size=3, padding=1)
        self.bn10 = nn.BatchNorm1d(self.nhidden1)
        self.relu10 = nn.ReLU()
        self.pool5 = nn.MaxPool1d(kernel_size=2)

        self.conv11 = nn.Conv1d(in_channels=self.nhidden1, out_channels=self.nhidden1, kernel_size=3, padding=1)
        self.bn11 = nn.BatchNorm1d(self.nhidden1)
        self.relu11 = nn.ReLU()

        self.conv12 = nn.Conv1d(in_channels=self.nhidden1, out_channels=self.nhidden1, kernel_size=3, padding=1)
        self.bn12 = nn.BatchNorm1d(self.nhidden1)
        self.relu12 = nn.ReLU()
        self.pool6 = nn.MaxPool1d(kernel_size=2)

        self.conv13 = nn.Conv1d(in_channels=self.nhidden1, out_channels=self.nhidden1, kernel_size=3, padding=1)
        self.bn13 = nn.BatchNorm1d(self.nhidden1)
        self.relu13 = nn.ReLU()

        self.conv14 = nn.Conv1d(in_channels=self.nhidden1, out_channels=self.nhidden1, kernel_size=3, padding=1)
        self.bn14 = nn.BatchNorm1d(self.nhidden1)
        self.relu14 = nn.ReLU()
        self.pool7 = nn.MaxPool1d(kernel_size=2)

        self.conv15 = nn.Conv1d(in_channels=self.nhidden1, out_channels=self.nhidden1, kernel_size=3, padding=1)
        self.bn15 = nn.BatchNorm1d(self.nhidden1)
        self.relu15 = nn.ReLU()

        self.conv16 = nn.Conv1d(in_channels=self.nhidden1, out_channels=self.nhidden1, kernel_size=3, padding=1)
        self.bn16 = nn.BatchNorm1d(self.nhidden1)
        self.relu16 = nn.ReLU()
        self.pool8 = nn.MaxPool1d(kernel_size=2)

        self.flatten = nn.Flatten()
        self.fc1 = nn.Linear(in_features=self.nhidden2, out_features=self.nhidden2)
        self.relu17 = nn.ReLU()
        self.fc2 = nn.Linear(in_features=self.nhidden2, out_features=nclasses)

    def preprocess(self, x):
        c1 = torch.sqrt(torch.sum(x[:, 0:3, :]**2, dim=1, keepdim=True) / 3)
        c2 = torch.sqrt(torch.sum(x[:, 3:6, :]**2, dim=1, keepdim=True) / 3)
        x = torch.cat([x, c1, c2], dim=1)
        return x
    
    def forward(self, x):
        if self.preprocessing:
            x = self.preprocess(x)
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu1(x)

        x = self.conv2(x)
        x = self.bn2(x)
        x = self.relu2(x)

        x = self.pool1(x)
        x = self.conv3(x)
        x = self.bn3(x)
        x = self.relu3(x)

        x = self.conv4(x)
        x = self.bn4(x)
        x = self.relu4(x)

        x = self.pool2(x)
        x = self.conv5(x)
        x = self.bn5(x)
        x = self.relu5(x)

        x = self.conv6(x)
        x = self.bn6(x)
        x = self.relu6(x)

        x = self.pool3(x)
        x = self.conv7(x)
        x = self.bn7(x)
        x = self.relu7(x)

        x = self.conv8(x)
        x = self.bn8(x)
        x = self.relu8(x)

        x = self.pool4(x)
        x = self.conv9(x)
        x = self.bn9(x)
        x = self.relu9(x)

        x = self.conv10(x)
        x = self.bn10(x)
        x = self.relu10(x)

        x = self.pool5(x)
        x = self.conv11(x)
        x = self.bn11(x)
        x = self.relu11(x)

        x = self.conv12(x)
        x = self.bn12(x)
        x = self.relu12(x)

        x = self.pool6(x)
        x = self.conv13(x)
        x = self.bn13(x)
        x = self.relu13(x)

        x = self.conv14(x)
        x = self.bn14(x)
        x = self.relu14(x)

        x = self.pool7(x)
        x = self.conv15(x)
        x = self.bn15(x)
        x = self.relu15(x)

        x = self.conv16(x)
        x = self.bn16(x)
        x = self.relu16(x)

        x = self.pool8(x)
        x = self.flatten(x)
        x = self.fc1(x)
        x = self.relu17(x)
        x = self.fc2(x)
        return x

class SpaceNet(nn.Module):
    def __init__(self, nchannels=6, nclasses=5, preprocessing=False):
        super(SpaceNet, self).__init__()
        self.nhidden1 = 64
        self.nhidden2 = 512
        self.preprocessing = preprocessing
        if self.preprocessing:
            nchannels = nchannels*2 + 4
        self.conv1 = nn.Conv1d(in_channels=nchannels, out_channels=self.nhidden1, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm1d(self.nhidden1)
        self.relu1 = nn.ReLU()

        self.conv2 = nn.Conv1d(in_channels=self.nhidden1, out_channels=self.nhidden1, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm1d(self.nhidden1)
        self.relu2 = nn.ReLU()
        self.pool1 = nn.MaxPool1d(kernel_size=2)

        self.conv3 = nn.Conv1d(in_channels=self.nhidden1, out_channels=self.nhidden1, kernel_size=3, padding=1)
        self.bn3 = nn.BatchNorm1d(self.nhidden1)
        self.relu3 = nn.ReLU()

        self.conv4 = nn.Conv1d(in_channels=self.nhidden1, out_channels=self.nhidden1, kernel_size=3, padding=1)
        self.bn4 = nn.BatchNorm1d(self.nhidden1)
        self.relu4 = nn.ReLU()
        self.pool2 = nn.MaxPool1d(kernel_size=2)

        self.conv5 = nn.Conv1d(in_channels=self.nhidden1, out_channels=self.nhidden1, kernel_size=3, padding=1)
        self.bn5 = nn.BatchNorm1d(self.nhidden1)
        self.relu5 = nn.ReLU()

        self.conv6 = nn.Conv1d(in_channels=self.nhidden1, out_channels=self.nhidden1, kernel_size=3, padding=1)
        self.bn6 = nn.BatchNorm1d(self.nhidden1)
        self.relu6 = nn.ReLU()
        self.pool3 = nn.MaxPool1d(kernel_size=2)

        self.conv7 = nn.Conv1d(in_channels=self.nhidden1, out_channels=self.nhidden1, kernel_size=3, padding=1)
        self.bn7 = nn.BatchNorm1d(self.nhidden1)
        self.relu7 = nn.ReLU()

        self.conv8 = nn.Conv1d(in_channels=self.nhidden1, out_channels=self.nhidden1, kernel_size=3, padding=1)
        self.bn8 = nn.BatchNorm1d(self.nhidden1)
        self.relu8 = nn.ReLU()
        self.pool4 = nn.MaxPool1d(kernel_size=2)

        self.conv9 = nn.Conv1d(in_channels=self.nhidden1, out_channels=self.nhidden1, kernel_size=3, padding=1)
        self.bn9 = nn.BatchNorm1d(self.nhidden1)
        self.relu9 = nn.ReLU()

        self.conv10 = nn.Conv1d(in_channels=self.nhidden1, out_channels=self.nhidden1, kernel_size=3, padding=1)
        self.bn10 = nn.BatchNorm1d(self.nhidden1)
        self.relu10 = nn.ReLU()
        self.pool5 = nn.MaxPool1d(kernel_size=2)

        self.conv11 = nn.Conv1d(in_channels=self.nhidden1, out_channels=self.nhidden1, kernel_size=3, padding=1)
        self.bn11 = nn.BatchNorm1d(self.nhidden1)
        self.relu11 = nn.ReLU()

        self.conv12 = nn.Conv1d(in_channels=self.nhidden1, out_channels=self.nhidden1, kernel_size=3, padding=1)
        self.bn12 = nn.BatchNorm1d(self.nhidden1)
        self.relu12 = nn.ReLU()
        self.pool6 = nn.MaxPool1d(kernel_size=2)

        self.conv13 = nn.Conv1d(in_channels=self.nhidden1, out_channels=self.nhidden1, kernel_size=3, padding=1)
        self.bn13 = nn.BatchNorm1d(self.nhidden1)
        self.relu13 = nn.ReLU()

        self.conv14 = nn.Conv1d(in_channels=self.nhidden1, out_channels=self.nhidden1, kernel_size=3, padding=1)
        self.bn14 = nn.BatchNorm1d(self.nhidden1)
        self.relu14 = nn.ReLU()
        self.pool7 = nn.MaxPool1d(kernel_size=2)

        self.conv15 = nn.Conv1d(in_channels=self.nhidden1, out_channels=self.nhidden1, kernel_size=3, padding=1)
        self.bn15 = nn.BatchNorm1d(self.nhidden1)
        self.relu15 = nn.ReLU()

        self.conv16 = nn.Conv1d(in_channels=self.nhidden1, out_channels=self.nhidden1, kernel_size=3, padding=1)
        self.bn16 = nn.BatchNorm1d(self.nhidden1)
        self.relu16 = nn.ReLU()
        self.pool8 = nn.MaxPool1d(kernel_size=2)

        self.flatten = nn.Flatten()
        self.fc1 = nn.Linear(in_features=self.nhidden2, out_features=self.nhidden2)
        self.relu17 = nn.ReLU()
        self.fc2 = nn.Linear(in_features=self.nhidden2, out_features=nclasses)

    def preprocess(self, x):
        c1 = torch.sqrt(torch.sum(x[:, 0:3, :]**2, dim=1, keepdim=True) / 3)
        c2 = torch.sqrt(torch.sum(x[:, 3:6, :]**2, dim=1, keepdim=True) / 3)
        x1 = torch.cat([x, c1, c2], dim=1)
        x2 = torch.abs(torch.fft.fft(x1, dim=-1)/x1.shape[-1])
        x = torch.cat([x1, x2], dim=1)
        return x
    
    def forward(self, x):
        if self.preprocessing:
            x = self.preprocess(x)
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu1(x)

        x = self.conv2(x)
        x = self.bn2(x)
        x = self.relu2(x)

        x = self.pool1(x)
        x = self.conv3(x)
        x = self.bn3(x)
        x = self.relu3(x)

        x = self.conv4(x)
        x = self.bn4(x)
        x = self.relu4(x)

        x = self.pool2(x)
        x = self.conv5(x)
        x = self.bn5(x)
        x = self.relu5(x)

        x = self.conv6(x)
        x = self.bn6(x)
        x = self.relu6(x)

        x = self.pool3(x)
        x = self.conv7(x)
        x = self.bn7(x)
        x = self.relu7(x)

        x = self.conv8(x)
        x = self.bn8(x)
        x = self.relu8(x)

        x = self.pool4(x)
        x = self.conv9(x)
        x = self.bn9(x)
        x = self.relu9(x)

        x = self.conv10(x)
        x = self.bn10(x)
        x = self.relu10(x)

        x = self.pool5(x)
        x = self.conv11(x)
        x = self.bn11(x)
        x = self.relu11(x)

        x = self.conv12(x)
        x = self.bn12(x)
        x = self.relu12(x)

        x = self.pool6(x)
        x = self.conv13(x)
        x = self.bn13(x)
        x = self.relu13(x)

        x = self.conv14(x)
        x = self.bn14(x)
        x = self.relu14(x)

        x = self.pool7(x)
        x = self.conv15(x)
        x = self.bn15(x)
        x = self.relu15(x)

        x = self.conv16(x)
        x = self.bn16(x)
        x = self.relu16(x)

        x = self.pool8(x)
        x = self.flatten(x)
        x = self.fc1(x)
        x = self.relu17(x)
        x = self.fc2(x)
        return x
    
# class SpaceNet(nn.Module):
#     def __init__(self, nchannels=6, nclasses=5, preprocessing=False):
#         super(SpaceNet, self).__init__()
#         self.preprocessing = preprocessing
#         if self.preprocessing:
#             nchannels +=2
#         self.conv1_1 = nn.Conv1d(in_channels=nchannels, out_channels=64, kernel_size=3, padding=1)
#         self.conv2_1 = nn.Conv1d(in_channels=64, out_channels=64, kernel_size=3, padding=1)
#         self.pool1_1 = nn.MaxPool1d(kernel_size=2)
#         self.relu1_1 = nn.ReLU()
#         self.conv3_1 = nn.Conv1d(in_channels=64, out_channels=64, kernel_size=3, padding=1)
#         self.conv4_1 = nn.Conv1d(in_channels=64, out_channels=64, kernel_size=3, padding=1)
#         self.pool2_1 = nn.MaxPool1d(kernel_size=2)
#         self.relu2_1 = nn.ReLU()
#         self.conv5_1 = nn.Conv1d(in_channels=64, out_channels=128, kernel_size=3, padding=1)
#         self.conv6_1 = nn.Conv1d(in_channels=128, out_channels=128, kernel_size=3, padding=1)
#         self.pool3_1 = nn.MaxPool1d(kernel_size=2)
#         self.relu3_1 = nn.ReLU()
#         self.conv7_1 = nn.Conv1d(in_channels=128, out_channels=128, kernel_size=3, padding=1)
#         self.conv8_1 = nn.Conv1d(in_channels=128, out_channels=128, kernel_size=3, padding=1)
#         self.pool4_1 = nn.MaxPool1d(kernel_size=2)
#         self.relu4_1 = nn.ReLU()
#         self.conv9_1 = nn.Conv1d(in_channels=128, out_channels=128, kernel_size=3, padding=1)
#         self.conv10_1 = nn.Conv1d(in_channels=128, out_channels=128, kernel_size=3, padding=1)
#         self.pool5_1 = nn.MaxPool1d(kernel_size=2)
#         self.relu5_1 = nn.ReLU()
#         self.conv11_1 = nn.Conv1d(in_channels=128, out_channels=128, kernel_size=3, padding=1)
#         self.conv12_1 = nn.Conv1d(in_channels=128, out_channels=128, kernel_size=3, padding=1)
#         self.pool6_1 = nn.MaxPool1d(kernel_size=2)
#         self.relu6_1 = nn.ReLU()
#         self.conv13_1 = nn.Conv1d(in_channels=128, out_channels=128, kernel_size=3, padding=1)
#         self.conv14_1 = nn.Conv1d(in_channels=128, out_channels=128, kernel_size=3, padding=1)
#         self.pool7_1 = nn.MaxPool1d(kernel_size=2)
#         self.relu7_1 = nn.ReLU()
#         self.flatten_1 = nn.Flatten()
#         self.fc1_1 = nn.Linear(in_features=2048, out_features=2048)
#         self.relu8_1 = nn.ReLU()
#         self.fc2_1 = nn.Linear(in_features=2048, out_features=1024)

#         self.conv1_2 = nn.Conv1d(in_channels=nchannels, out_channels=64, kernel_size=3, padding=1)
#         self.conv2_2 = nn.Conv1d(in_channels=64, out_channels=64, kernel_size=3, padding=1)
#         self.pool1_2 = nn.MaxPool1d(kernel_size=2)
#         self.relu1_2 = nn.ReLU()
#         self.conv3_2 = nn.Conv1d(in_channels=64, out_channels=64, kernel_size=3, padding=1)
#         self.conv4_2 = nn.Conv1d(in_channels=64, out_channels=64, kernel_size=3, padding=1)
#         self.pool2_2 = nn.MaxPool1d(kernel_size=2)
#         self.relu2_2 = nn.ReLU()
#         self.conv5_2 = nn.Conv1d(in_channels=64, out_channels=128, kernel_size=3, padding=1)
#         self.conv6_2 = nn.Conv1d(in_channels=128, out_channels=128, kernel_size=3, padding=1)
#         self.pool3_2 = nn.MaxPool1d(kernel_size=2)
#         self.relu3_2 = nn.ReLU()
#         self.conv7_2 = nn.Conv1d(in_channels=128, out_channels=128, kernel_size=3, padding=1)
#         self.conv8_2 = nn.Conv1d(in_channels=128, out_channels=128, kernel_size=3, padding=1)
#         self.pool4_2 = nn.MaxPool1d(kernel_size=2)
#         self.relu4_2 = nn.ReLU()
#         self.conv9_2 = nn.Conv1d(in_channels=128, out_channels=128, kernel_size=3, padding=1)
#         self.conv10_2 = nn.Conv1d(in_channels=128, out_channels=128, kernel_size=3, padding=1)
#         self.pool5_2 = nn.MaxPool1d(kernel_size=2)
#         self.relu5_2 = nn.ReLU()
#         self.conv11_2 = nn.Conv1d(in_channels=128, out_channels=128, kernel_size=3, padding=1)
#         self.conv12_2 = nn.Conv1d(in_channels=128, out_channels=128, kernel_size=3, padding=1)
#         self.pool6_2 = nn.MaxPool1d(kernel_size=2)
#         self.relu6_2 = nn.ReLU()
#         self.conv13_2 = nn.Conv1d(in_channels=128, out_channels=128, kernel_size=3, padding=1)
#         self.conv14_2 = nn.Conv1d(in_channels=128, out_channels=128, kernel_size=3, padding=1)
#         self.pool7_2 = nn.MaxPool1d(kernel_size=2)
#         self.relu7_2 = nn.ReLU()
#         self.flatten_2 = nn.Flatten()
#         self.fc1_2 = nn.Linear(in_features=2048, out_features=2048)
#         self.relu8_2 = nn.ReLU()
#         self.fc2_2 = nn.Linear(in_features=2048, out_features=1024)

#         self.fc1 = nn.Linear(in_features=2048, out_features=2048)
#         self.relu1 = nn.ReLU()
#         self.fc2 = nn.Linear(in_features=2048, out_features=nclasses)

#     def preprocess(self, x):
#         c1 = torch.sqrt(torch.sum(x[:, 0:3, :]**2, dim=1, keepdim=True)/3)
#         c2 = torch.sqrt(torch.sum(x[:, 3:6, :]**2, dim=1, keepdim=True)/3)
#         x = torch.cat([x, c1, c2], dim=1)
#         return x

#     def path1(self, x):
#         x = self.conv1_1(x)
#         x = self.conv2_1(x)
#         x = self.pool1_1(x)
#         x = self.relu1_1(x)
#         x = self.conv3_1(x)
#         x = self.conv4_1(x)
#         x = self.pool2_1(x)
#         x = self.relu2_1(x)
#         x = self.conv5_1(x)
#         x = self.conv6_1(x)
#         x = self.pool3_1(x)
#         x = self.relu3_1(x)
#         x = self.conv7_1(x)
#         x = self.conv8_1(x)
#         x = self.pool4_1(x)
#         x = self.relu4_1(x)
#         x = self.conv9_1(x)
#         x = self.conv10_1(x)
#         x = self.pool5_1(x)
#         x = self.relu5_1(x)
#         x = self.conv11_1(x)
#         x = self.conv12_1(x)
#         x = self.pool6_1(x)
#         x = self.relu6_1(x)
#         x = self.conv13_1(x)
#         x = self.conv14_1(x)
#         x = self.pool7_1(x)
#         x = self.relu7_1(x)
#         x = self.flatten_1(x)
#         x = self.fc1_1(x)
#         x = self.relu8_1(x)
#         x = self.fc2_1(x)
#         return x

#     def path2(self, x):
#         x = torch.abs(torch.fft.fft(x, dim=-1)/x.shape[-1])
#         x = self.conv1_2(x)
#         x = self.conv2_2(x)
#         x = self.pool1_2(x)
#         x = self.relu1_2(x)
#         x = self.conv3_2(x)
#         x = self.conv4_2(x)
#         x = self.pool2_2(x)
#         x = self.relu2_2(x)
#         x = self.conv5_2(x)
#         x = self.conv6_2(x)
#         x = self.pool3_2(x)
#         x = self.relu3_2(x)
#         x = self.conv7_2(x)
#         x = self.conv8_2(x)
#         x = self.pool4_2(x)
#         x = self.relu4_2(x)
#         x = self.conv9_2(x)
#         x = self.conv10_2(x)
#         x = self.pool5_2(x)
#         x = self.relu5_2(x)
#         x = self.conv11_2(x)
#         x = self.conv12_2(x)
#         x = self.pool6_2(x)
#         x = self.relu6_2(x)
#         x = self.conv13_2(x)
#         x = self.conv14_2(x)
#         x = self.pool7_2(x)
#         x = self.relu7_2(x)
#         x = self.flatten_2(x)
#         x = self.fc1_2(x)
#         x = self.relu8_2(x)
#         x = self.fc2_2(x)
#         return x

#     def forward(self, x):
#         if self.preprocessing:
#             x = self.preprocess(x)
#         y1 = self.path1(x)
#         y2 = self.path2(x)
#         x = torch.cat((y1, y2), dim=1)
#         x = self.fc1(x)
#         x = self.relu1(x)
#         x = self.fc2(x)
#         return x

        
