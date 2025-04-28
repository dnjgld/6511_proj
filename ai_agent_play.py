from ai_agent import TankAgent
from game_loader import Game
import os

game = Game()
agent = TankAgent(state_size=20, action_size=5, epsilon=0.01)

if os.path.exists("tank_dqn_final_1_35.keras"):
    agent.load("tank_dqn_final_1_35.keras")
    print("loaded model weights: tank_dqn_final_1_35.keras")
    # agent.model.summary()

game.game_running_ai_play(agent)