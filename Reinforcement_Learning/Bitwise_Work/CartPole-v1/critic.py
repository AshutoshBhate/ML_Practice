class AutomatedCritic:
    def judge(self, traj_A, traj_B):
        
        # Decides which trajectory is better
        score_A = self.calculate_score(traj_A)
        score_B = self.calculate_score(traj_B)

        return 1 if score_A > score_B else 0

    def calculate_score(self, trajectory):
        
        score = len(trajectory)
        
        return score