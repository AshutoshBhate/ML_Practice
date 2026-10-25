import numpy as np

class Teacher:
    def __init__(self):
        pass

    def get_preference(self, segment_1, segment_2):
        score_1 = sum([step['original_reward'] for step in segment_1])
        score_2 = sum([step['original_reward'] for step in segment_2])

        if score_1 > score_2:
            return 0
        elif score_2 > score_1:
            return 1

        progress_1 = sum([step['obs'][0] for step in segment_1])
        progress_2 = sum([step['obs'][0] for step in segment_2])

        if progress_1 > progress_2:
            return 0
        elif progress_2 > progress_1:
            return 1

        return np.random.choice([0, 1])
