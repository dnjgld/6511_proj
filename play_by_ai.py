import threading
import time
from game_loader import Game
from ai_agent import TankAgent
import os
import random

game = Game()
agent = TankAgent(state_size=5, action_size=5)

if os.path.exists("tank_dqn_final.h5"):
    agent.model.load_weights("tank_dqn_final.h5")
    print("Load model weights: tank_dqn_final.h5")

lock = threading.Lock()

def run_game():
    num = random.randint(26, 35)
    game.game_running(checkpoint=num, isEndless=False) 


def ai_controller():
    while True:
        time.sleep(0.1)
        if game.myTank_T1.life <= 0:
            continue
        with lock:
            state = game.get_game_state().reshape(1, -1)
            action = agent.act(state)
            game.update_game_with_action(action)

if __name__ == "__main__":
    threading.Thread(target=ai_controller, daemon=True).start()
    run_game()
