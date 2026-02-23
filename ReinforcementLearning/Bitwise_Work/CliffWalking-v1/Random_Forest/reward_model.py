import numpy as np
import joblib
from sklearn.ensemble import RandomForestRegressor
import config

class RewardModel:
    def __init__(self):
        self.model = RandomForestRegressor(
            n_estimators=config.RF_N_ESTIMATORS,
            max_depth=config.RF_MAX_DEPTH,
            min_samples_leaf=config.RF_MIN_SAMPLES,
            n_jobs=1
        )
        self.is_fitted = False

    def predict(self, obs, action):
        if not self.is_fitted:
            return 0.0

        obs = np.array(obs).reshape(-1)
        action_one_hot = np.zeros(config.ACTION_DIM)
        action_one_hot[action] = 1.0
        input_vec = np.concatenate([obs, action_one_hot]).reshape(1, -1)

        return self.model.predict(input_vec)[0]

    def predict_batch(self, obs_batch, act_batch):
        if not self.is_fitted:
            return np.zeros(len(obs_batch))

        obs_batch = np.array(obs_batch)
        act_batch = np.array(act_batch)

        batch_size = len(obs_batch)
        action_one_hot = np.zeros((batch_size, config.ACTION_DIM))
        action_one_hot[np.arange(batch_size), act_batch] = 1.0

        input_vec = np.hstack([obs_batch, action_one_hot])

        return self.model.predict(input_vec)

    def fit(self, X, y):
        self.model.fit(X, y)
        self.is_fitted = True

    def save(self, path):
        joblib.dump(self.model, path)

    def load(self, path):
        self.model = joblib.load(path)
        self.is_fitted = True
