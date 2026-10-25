import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

class RewardNetwork(nn.Module):
    def __init__(self, input_dim, lr=0.01):
        super(RewardNetwork, self).__init__()
        
        self.model = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 1) 
        )
        
        self.optimizer = optim.Adam(self.parameters(), lr=lr)

    def forward(self, state):
        return self.model(state)

    def predict_reward(self, state_np):
        # This function takes the state and outputs a reward
        
        state_t = torch.FloatTensor(state_np).unsqueeze(0)
        
        with torch.no_grad():
            reward = self.forward(state_t)
            
        return reward.item()

    def train_on_batch(self, traj_A_states, traj_B_states, label_A_is_better):
    
        # traj_A_states: Numpy array of states in Trajectory A
        # traj_B_states: Numpy array of states in Trajectory B

        # Prepare data
        states_A = torch.FloatTensor(traj_A_states)
        states_B = torch.FloatTensor(traj_B_states)
        
        # Reset gradients
        self.optimizer.zero_grad()
        
        # Predict rewards for every step in both trajectories
        r_A = self.forward(states_A)
        r_B = self.forward(states_B)
        
        # Sum them up to get Total Reward
        sum_r_A = torch.sum(r_A)
        sum_r_B = torch.sum(r_B)
        
        # Calculate Loss (Bradley-Terry Model)
        # Probability that A is better = Sigmoid(Sum_A - Sum_B)
        
        diff = sum_r_A - sum_r_B
        
        # Binary Cross Entropy with Logits combines Sigmoid + Log Loss
        criterion = nn.BCEWithLogitsLoss()
        
        # Create the target tensor (1.0 or 0.0)
        target = torch.tensor([label_A_is_better], dtype=torch.float32)
        
        # Calculate loss between our difference and the target
        loss = criterion(diff.unsqueeze(0), target)
        
        # 6. Backpropagate
        loss.backward()
        self.optimizer.step()
        
        return loss.item()