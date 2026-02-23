import numpy as np
import random

class TrajectoryBuffer:
    def __init__(self):
        
        self.trajectories = []
        
        self.current_trajectory = []

    def add_step(self, obs):
        
        self.current_trajectory.append(obs)

    def commit_trajectory(self):
        
        if len(self.current_trajectory) > 0:
            self.trajectories.append(np.array(self.current_trajectory))
            self.current_trajectory = []

    def sample_pair(self):

        if len(self.trajectories) < 2:
            return None, None
        
        idx_a, idx_b = random.sample(range(len(self.trajectories)), 2)
        
        return self.trajectories[idx_a], self.trajectories[idx_b]

    def clear(self):
        self.trajectories = []
        self.current_trajectory = []