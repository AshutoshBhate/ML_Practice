import gymnasium as gym
import numpy as np

class PbRLWrapper(gym.Wrapper):
    def __init__(self, env, reward_network, trajectory_buffer):
        super().__init__(env)
        self.reward_network = reward_network
        self.trajectory_buffer = trajectory_buffer

    def step(self, action):
        # Run the real environment step (ignore the reward)
        obs, real_reward, terminated, truncated, info = self.env.step(action)

        # Store the observation in our buffer 
        self.trajectory_buffer.add_step(obs)

        # Hijack here, we ask our reward model to predict the reward
        fake_reward = self.reward_network.predict_reward(obs)

        # Return the fake reward to the agent
        return obs, fake_reward, terminated, truncated, info

    def reset(self, **kwargs):
        # When episode ends
        self.trajectory_buffer.commit_trajectory()

        obs, info = self.env.reset(**kwargs)
        
        # Store the very first frame of the new game
        self.trajectory_buffer.add_step(obs)
        
        return obs, info