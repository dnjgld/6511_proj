from ai_agent import TankAgent
from game_loader import Game
import os

game = Game()
agent = TankAgent(state_size=20, action_size=5)

if os.path.exists("tank_dqn_level_2.h5"):
    agent.model.load_weights("tank_dqn_level_2.h5")
    print("loaded model weights: tank_dqn_level_2.h5")

game.game_running_ai_trainning(agent, episode = 10)