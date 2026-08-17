import torch.nn as nn
import torch.nn.functional as F

class ImageClassifierCNN(nn.Module):
    def __init__(self, num_classes: int = 10):
        super().__init__()
        # Input shape: [3, 32, 32] for CIFAR-10
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        
        self.fc1 = nn.Linear(64 * 8 * 8, 128)
        self.fc2 = nn.Linear(128, num_classes)
        self.dropout = nn.Dropout(0.25)

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x))) # [32, 16, 16]
        x = self.pool(F.relu(self.conv2(x))) # [64, 8, 8]
        x = x.view(-1, 64 * 8 * 8)
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.fc2(x)
        return x
