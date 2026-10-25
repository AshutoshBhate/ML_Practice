import gymnasium as gym
import numpy as np
import torch
import config

class CliffWalkingStateWrapper(gym.ObservationWrapper):
    def __init__(self, env):
        super().__init__(env)
        self.observation_space = gym.spaces.Box(
            low=0.0, high=1.0, shape=(config.OBS_DIM,), dtype=np.float32
        )

    def observation(self, state):
        row = state // config.GRID_W
        col = state % config.GRID_W

        norm_x = col / (config.GRID_W - 1) if config.GRID_W > 1 else 0
        norm_y = row / (config.GRID_H - 1) if config.GRID_H > 1 else 0

        return np.array([norm_x, norm_y], dtype=np.float32)

class RewardPredictorWrapper(gym.Wrapper):
    def __init__(self, env, reward_model):
        super().__init__(env)
        self.reward_model = reward_model
        self._current_obs = None

    def reset(self, **kwargs):
        obs, info = self.env.reset(**kwargs)
        self._current_obs = obs
        return obs, info

    def step(self, action):
        rm_obs = self._current_obs
        next_obs, env_reward, terminated, truncated, info = self.env.step(action)
        self._current_obs = next_obs
        info['original_reward'] = env_reward

        with torch.no_grad():
            state_tensor = torch.tensor(rm_obs, dtype=torch.float32, device=config.DEVICE).unsqueeze(0)
            action_one_hot = torch.zeros((1, config.ACTION_DIM), device=config.DEVICE)
            action_one_hot[0, action] = 1.0
            rm_input = torch.cat([state_tensor, action_one_hot], dim=1)
            
            raw_logit = self.reward_model(rm_input).item()

        prob_good = 1 / (1 + np.exp(-raw_logit))

        final_reward = prob_good - 0.55

        return next_obs, final_reward, terminated, truncated, info
