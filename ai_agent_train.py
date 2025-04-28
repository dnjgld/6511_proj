from ai_agent import TankAgent
from game_loader import Game
import os

game = Game()
agent = TankAgent(state_size=20, action_size=5, epsilon=1.0)

if os.path.exists("tank_dqn_final_1_35.keras"):
    agent.load("tank_dqn_final_1_35.keras")
    print("loaded model weights: tank_dqn_final_1_35.keras")

game.game_running_ai_trainning(agent, episodes=1000, show_training=True)