import torch
import torch.nn as nn
import config

class RewardModel(nn.Module):
    def __init__(self):
        super().__init__()
        
        input_dim = config.OBS_DIM + config.ACTION_DIM
        
        self.network = nn.Sequential(
            nn.Linear(input_dim, config.RM_HIDDEN_DIM),
            nn.ReLU(),
            nn.Linear(config.RM_HIDDEN_DIM, config.RM_HIDDEN_DIM),
            nn.ReLU(),
            nn.Linear(config.RM_HIDDEN_DIM, 1)
        )
        
        self.to(config.DEVICE)

    def forward(self, x):
        return self.network(x)

    def save(self, path):
        torch.save(self.state_dict(), path)

    def load(self, path):
        self.load_state_dict(torch.load(path))
