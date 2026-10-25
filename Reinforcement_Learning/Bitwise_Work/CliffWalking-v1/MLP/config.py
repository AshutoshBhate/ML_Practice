import torch
import os

DEVICE = "cpu"

ENV_ID = "CliffWalking-v1"
GRID_H = 4
GRID_W = 12
MAX_STEPS = 100

OBS_DIM = 2
ACTION_DIM = 4

#PPO Hyperparameters
PPO_LR = 3e-4
PPO_GAMMA = 0.99
PPO_EPS_CLIP = 0.2
PPO_K_EPOCHS = 10
PPO_BATCH_SIZE = 64
PPO_ENTROPY_COEF = 0.01
PPO_GAE_LAMBDA = 0.95

#Reward Model Hyperparameters
RM_LR = 1e-3
RM_HIDDEN_DIM = 64
RM_BATCH_SIZE = 32

SEGMENT_LENGTH = 25
BUFFER_CAPACITY = 1000

TOTAL_TIMESTEPS = 50000
PRETRAIN_STEPS = 1000
FEEDBACK_FREQ = 2048

LOG_DIR = "./rlhf_logs/"
TB_LOG_DIR = "./rlhf_tb_logs/"
CHECKPOINT_FREQ = 5000 
EVAL_FREQ = 2000     

os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(TB_LOG_DIR, exist_ok=True)