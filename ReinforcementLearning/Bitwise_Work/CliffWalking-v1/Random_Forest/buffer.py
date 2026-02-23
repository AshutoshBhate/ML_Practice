import numpy as np
import random
from collections import deque

class TrajectoryBuffer:
    def __init__(self, capacity, segment_length):
        self.capacity = capacity
        self.segment_length = segment_length
        self.segments = deque(maxlen=capacity)
        self.current_segment = []

    def add_step(self, obs, action, original_reward):
        self.current_segment.append({
            'obs': obs,
            'action': action,
            'original_reward': original_reward
        })

        if len(self.current_segment) >= self.segment_length:
            self.segments.append(self.current_segment)
            self.current_segment = []

    def finalize_episode(self):
        if len(self.current_segment) > 0:
            self.segments.append(self.current_segment)
        self.current_segment = []

    def sample_pairs(self, batch_size):
        if len(self.segments) < 2:
            return []

        pairs = []
        for _ in range(batch_size):
            idx1, idx2 = random.sample(range(len(self.segments)), 2)
            seg1 = self.segments[idx1]
            seg2 = self.segments[idx2]
            pairs.append((seg1, seg2))
            
        return pairs

    def __len__(self):
        return len(self.segments)
