from ai_agent import TankAgent
from game_loader import Game
import os

game = Game()
agent = TankAgent(state_size=20, action_size=5)

file_name = "tank_dqn_level_2.keras"
if os.path.exists(file_name):
    agent.model.load_weights(file_name)
    print("loaded model weights: " + file_name)
    
game.game_running_ai_play(agent, epsilon = 0.01)