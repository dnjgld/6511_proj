import numpy as np
import random
from collections import deque
from tensorflow.keras import layers, models, optimizers

class TankAgent:
    def __init__(self, state_size, action_size, epsilon=1.0):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=10000)
        self.gamma = 0.95
        self.learning_rate = 0.005
        self.epsilon = epsilon
        self.epsilon_min = 0.05
        self.epsilon_decay = 0.995
        self.model = self._build_model()

    def _build_model(self):
        model = models.Sequential()
        model.add(layers.Input(shape=(self.state_size,)))
        model.add(layers.Dense(64, activation='relu'))
        model.add(layers.Dense(64, activation='relu'))
        model.add(layers.Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=optimizers.Adam(learning_rate=self.learning_rate))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        # 将列表状态转换为数组形状 (1, state_size)
        state_arr = np.array(state, dtype=np.float32).reshape(1, -1)
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        q_values = self.model.predict(state_arr, verbose=0)[0]
        return np.argmax(q_values)

    def replay(self, batch_size):
        if len(self.memory) < batch_size:
            return
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state, done in minibatch:
            state_arr = np.array(state, dtype=np.float32).reshape(1, -1)
            next_arr = np.array(next_state, dtype=np.float32).reshape(1, -1)
            target = reward
            if not done:
                target = reward + self.gamma * np.max(self.model.predict(next_arr, verbose=0)[0])
            target_f = self.model.predict(state_arr, verbose=0)
            target_f[0][action] = target
            self.model.fit(state_arr, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, path):
        self.model = models.load_model(path)

    def save(self, path):
        self.model.save(path)