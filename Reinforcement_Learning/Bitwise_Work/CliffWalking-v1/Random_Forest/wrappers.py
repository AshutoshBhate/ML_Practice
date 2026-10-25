import gymnasium as gym
import numpy as np
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

    def step(self, action):
        if not hasattr(self, '_current_obs') or self._current_obs is None:
            self._current_obs, _ = self.env.reset()

        current_obs = self._current_obs
        next_obs, env_reward, terminated, truncated, info = self.env.step(action)
        info['original_reward'] = env_reward

        rf_reward = self.reward_model.predict(current_obs, action)
        final_reward = (rf_reward * 2.0) - 2.1

        self._current_obs = next_obs
        return next_obs, final_reward, terminated, truncated, info

    def reset(self, **kwargs):
        obs, info = self.env.reset(**kwargs)
        self._current_obs = obs
        return obs, info
