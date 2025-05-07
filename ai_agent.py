# The referenced resource: 
# https://github.com/keon/deep-q-learning/blob/master/dqn_batch.py (DQN)
# https://github.com/flyyufelix/VizDoom-Keras-RL/blob/4fc27ce3d400eba5422d39e2fad565d0503a6149/ddqn.py (double DQN)

import numpy as np
import random
from collections import deque
from tensorflow.keras import layers, models, optimizers
import pickle

# an agent build on DQN
class TankAgent:
    def __init__(self, state_size, action_size, epsilon = 1.0):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=10000)
        self.gamma = 0.95  # discount rate
        self.epsilon = epsilon
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()
        self.target_model = self._build_model()
        self.update_target_model()

    def _build_model(self):
        model = models.Sequential()
        model.add(layers.Input(shape=(self.state_size,)))
        model.add(layers.Dense(128, activation='relu'))
        model.add(layers.Dense(128, activation='relu'))
        model.add(layers.Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=optimizers.Adam(learning_rate=self.learning_rate))
        return model

    def update_target_model(self):
        self.target_model.set_weights(self.model.get_weights())

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state, verbose=0)
        return np.argmax(act_values[0])

    def replay(self, batch_size):
        if len(self.memory) < batch_size:
            return
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = self.model.predict(state, verbose=0)
            if done:
                target[0][action] = reward
            else:
                next_action = np.argmax(self.model.predict(next_state, verbose=0)[0])
                t = self.target_model.predict(next_state, verbose=0)[0][next_action]
                target[0][action] = reward + self.gamma * t
            self.model.fit(state, target, epochs=1, verbose=0)
    
    def load(self, path):
        # load the model
        self.model = models.load_model(path)

    def save(self, path):
        # save the model
        self.model.save(path)
        
    def save_replay_buffer(self, path):
        with open(path, 'wb') as f:
            pickle.dump(self.memory, f)

    def load_replay_buffer(self, path):
        try:
            with open(path, 'rb') as f:
                self.memory = pickle.load(f)
        except FileNotFoundError:
            print("No replay buffer file found, starting fresh.")