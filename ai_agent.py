# Original resource: https://github.com/keon/deep-q-learning/blob/master/dqn_batch.py

import numpy as np
import random
from collections import deque
from tensorflow.keras import models, layers, optimizers

# a agent build on DQN
class TankAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        # memory buffer to store the experience of the agent
        self.memory = deque(maxlen=2000)
        # discount rate for future rewards
        self.gamma = 0.95 
        # exploration rate for epsilon-greedy policy
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        # learning rate for the optimizer
        self.learning_rate = 0.001
        # the model that will be used to predict the Q-values
        self.model = self._build_model()

    def _build_model(self):
        model = models.Sequential()
        # the model now has 3 layers
        model.add(layers.Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(layers.Dense(24, activation='relu'))
        model.add(layers.Dense(self.action_size, activation='linear'))
        # mean squared error loss function and Adam optimizer
        model.compile(loss='mse', optimizer=optimizers.Adam(learning_rate=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        # store the experience in the memory buffer
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        # choose an action to take
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state, verbose=0)
        return np.argmax(act_values[0])

    def replay(self, batch_size):
        # using the experience replay to train the model
        if len(self.memory) < batch_size:
            return
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * np.amax(self.model.predict(next_state, verbose=0)[0])
            target_f = self.model.predict(state, verbose=0)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
            
    def load(self, path):
        # load the model weights
        self.model.load_weights(path)

    def save(self, path):
        # save the model weights
        self.model.save_weights(path)