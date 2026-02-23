import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import config

def train_reward_model(reward_model, pairs, teacher, optimizer):
    reward_model.train()
    loss_list = []
    
    criterion = nn.BCEWithLogitsLoss()
    
    batch_loss = 0
    
    optimizer.zero_grad()
    
    for segment_1, segment_2 in pairs:
        label = teacher.get_preference(segment_1, segment_2)
        
        label_tensor = torch.tensor(
            [label], dtype=torch.float32, device=config.DEVICE
        )
        
        s1_obs = torch.tensor(
            np.array([step['obs'] for step in segment_1]),
            dtype=torch.float32,
            device=config.DEVICE
        )
        s1_act = [step['action'] for step in segment_1]
        
        s1_act_one_hot = torch.zeros(
            (len(s1_act), config.ACTION_DIM), device=config.DEVICE
        )
        s1_act_one_hot[np.arange(len(s1_act)), s1_act] = 1.0
        
        s1_input = torch.cat([s1_obs, s1_act_one_hot], dim=1)
        
        s2_obs = torch.tensor(
            np.array([step['obs'] for step in segment_2]),
            dtype=torch.float32,
            device=config.DEVICE
        )
        s2_act = [step['action'] for step in segment_2]
        
        s2_act_one_hot = torch.zeros(
            (len(s2_act), config.ACTION_DIM), device=config.DEVICE
        )
        s2_act_one_hot[np.arange(len(s2_act)), s2_act] = 1.0
        
        s2_input = torch.cat([s2_obs, s2_act_one_hot], dim=1)

        

        r1_sum = torch.sum(reward_model(s1_input))
        r2_sum = torch.sum(reward_model(s2_input))
        
        logit = r2_sum - r1_sum
        loss = criterion(logit.unsqueeze(0), label_tensor)
        
        batch_loss += loss
        loss_list.append(loss.item())
        
    if len(pairs) > 0:
        batch_loss = batch_loss / len(pairs)
        batch_loss.backward()
        optimizer.step()
        return np.mean(loss_list)
    else:
        return 0.0
