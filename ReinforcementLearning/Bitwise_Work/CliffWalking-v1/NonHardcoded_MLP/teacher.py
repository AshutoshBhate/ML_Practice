import numpy as np
import config

class CliffWalkingTranslator:
    def __init__(self):
        self.cliff_row = 3
        self.cliff_cols = range(1, 11)
        self.goal_pos = (3, 11)
    
    def translate(self, segment):
        log = set()
        
        for step in segment:
            obs = step['obs']
            col = int(round(obs[0] * (config.GRID_W - 1)))
            row = int(round(obs[1] * (config.GRID_H - 1)))
            
            if row == self.cliff_row and col in self.cliff_cols:
                log.add("CRITICAL_FAILURE")
            elif (row, col) == self.goal_pos:
                log.add("TASK_COMPLETE")

        if len(segment) > 0:
            start_obs = segment[0]['obs']
            end_obs = segment[-1]['obs']
            
            start_dist = self._get_dist(start_obs)
            end_dist = self._get_dist(end_obs)
            
            if end_dist < start_dist:
                log.add("MADE_PROGRESS")
            elif end_dist > start_dist:
                log.add("LOST_PROGRESS")
            
        return log

    def _get_dist(self, obs):
        col = int(round(obs[0] * (config.GRID_W - 1)))
        row = int(round(obs[1] * (config.GRID_H - 1)))
        return abs(row - self.goal_pos[0]) + abs(col - self.goal_pos[1])

class SemanticTeacher:
    def __init__(self):
        self.translator = CliffWalkingTranslator()

    def get_preference(self, segment_1, segment_2):
        log_a = self.translator.translate(segment_1)
        log_b = self.translator.translate(segment_2)

        # Apply Hierarchical Rules
        
        # Priority 1 : Don't fall off the cliff
        a_died = "CRITICAL_FAILURE" in log_a
        b_died = "CRITICAL_FAILURE" in log_b
        
        if a_died and not b_died: return 1  # B wins (Segment 2)
        if b_died and not a_died: return 0  # A wins (Segment 1)
        if a_died and b_died: return -1     # Tie (Both bad)

        # Priority 2 : Reach the goal
        a_won = "TASK_COMPLETE" in log_a
        b_won = "TASK_COMPLETE" in log_b
        
        if a_won and not b_won: return 0
        if b_won and not a_won: return 1

        # Priority 3 : Go closer to goal
        a_prog = "MADE_PROGRESS" in log_a
        b_prog = "MADE_PROGRESS" in log_b
        
        if a_prog and not b_prog: return 0
        if b_prog and not a_prog: return 1
        
        return -1 # Tie