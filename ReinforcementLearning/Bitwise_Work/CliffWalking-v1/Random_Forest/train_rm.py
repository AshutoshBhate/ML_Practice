import numpy as np
import config

def train_reward_model(reward_model, pairs, teacher, optimizer=None):
    X_train = []
    y_train = []

    for segment_1, segment_2 in pairs:
        label = teacher.get_preference(segment_1, segment_2)

        if label == 0:
            winner, loser = segment_1, segment_2
        else:
            winner, loser = segment_2, segment_1

        for step in winner:
            obs = step['obs']
            act = step['action']
            act_one_hot = np.zeros(config.ACTION_DIM)
            act_one_hot[act] = 1.0
            feature_vector = np.concatenate([obs, act_one_hot])
            X_train.append(feature_vector)
            y_train.append(1.0)

        if len(loser) > 0:
            last_step = loser[-1]
            obs = last_step['obs']
            act = last_step['action']
            act_one_hot = np.zeros(config.ACTION_DIM)
            act_one_hot[act] = 1.0
            feature_vector = np.concatenate([obs, act_one_hot])
            X_train.append(feature_vector)
            y_train.append(0.0)

    if len(X_train) > 0:
        X_train = np.array(X_train)
        y_train = np.array(y_train)
        reward_model.fit(X_train, y_train)
        preds = reward_model.model.predict(X_train)
        mse_loss = np.mean((preds - y_train) ** 2)
        return mse_loss

    return 0.0
