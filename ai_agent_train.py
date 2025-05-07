from ai_agent import TankAgent
from game_loader import Game
import os

game = Game()
enemy_num = 1
state_size = 3*(enemy_num+1)
agent = TankAgent(state_size=state_size, action_size=5)

file_name = "tank_dqn_training.keras"
replay_file_name = "tank_dqn_replay.pkl"

# exists, retraining model sey epsilon = 0.5
if os.path.exists(file_name):
    agent.epsilon = 0.5
    agent.load(file_name)
    print("loaded model weights: " + file_name)
    if os.path.exists(replay_file_name):
        agent.load_replay_buffer(replay_file_name)
        print("loaded replay buffer: " + replay_file_name)
    # agent.model.summary()

game.game_running_ai_trainning(agent, episodes = 1000, enemy_num=enemy_num, show_training=True, file_name=file_name)