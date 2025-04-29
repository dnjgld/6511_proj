from ai_agent import TankAgent
from game_loader import Game
import os

game = Game()
enemy_num = 1
state_size = 3*(enemy_num+1)
agent = TankAgent(state_size=state_size, action_size=5, epsilon=0.01)

file_name = "tank_dqn_6.keras"
if os.path.exists(file_name):
    agent.load(file_name)
    print("loaded model weights: " + file_name)

game.game_running_ai_play(agent, enemy_num=enemy_num)