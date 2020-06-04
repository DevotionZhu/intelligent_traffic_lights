import torch
import torch.nn as nn
import torch.nn.functional as F
import random
import numpy as np


class DQNetwork(nn.Module):

    def __init__(self):
        super().__init__()

        self.features1 = nn.Sequential(
                nn.Conv2d(1, 16, 4, stride=2, padding=1),
                nn.LeakyReLU(),
                nn.Conv2d(16, 32, 2, stride=1),
                nn.LeakyReLU(),
                )
        self.features2 = nn.Sequential(
                nn.Conv2d(1, 16, 4, stride=2, padding=1),
                nn.LeakyReLU(),
                nn.Conv2d(16, 32, 2, stride=1),
                nn.LeakyReLU(),
                )
        # self.features3 = nn.Linear(4, 4)

        self.linear_relu1 = nn.Sequential(
                nn.Linear(32*7*7 + 32*7*7 + 4, 128),
                nn.LeakyReLU(),
                nn.Dropout(0.2),
                nn.Linear(128, 128),
                nn.LeakyReLU(),
                nn.Dropout(0.2),
                nn.Linear(128, 128),
                nn.LeakyReLU()
                )

        self.classifier = nn.Sequential(
                nn.Linear(128, 4),
                # nn.Softmax(dim=-1)
                # nn.ReLU()
                )


    def forward(self, state):
        x1, x2, x3 = state
        x1 = self.features1(x1.view(x1.size(0), 1, -1, 16))
        x2 = self.features2(x2.view(x1.size(0), 1, -1, 16))
        # x3 = self.features3(x3)

        x1 = x1.view(x1.size(0), -1)
        x2 = x2.view(x2.size(0), -1)
        x3 = x3.view(x3.size(0), -1)

        x = torch.cat((x1, x2, x3), dim=1)

        x = self.linear_relu1(x)
        x = self.classifier(x)

        return x

    def predict(self, state, eps):
        act = self.forward(state)
        prob = random.random()
        if prob < eps:
            return random.randint(0, 3)
        else:
            return act.argmax().item()