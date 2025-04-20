# Notes:

Please check the main branch;<br>
We used the code of pygame-TankWar repository<br>
Github website: https://github.com/HelloZhan/pygame-TankWar<br>
Introduction Website: https://blog.csdn.net/qq_46470984/article/details/122003755<br>

We will mainly do edition on:<br>
- game_loader.py<br>
- main.py<br>

We created:<br>
- ai_agent.py<br>
This file implement the Deep Q-Network (DQN) agent for tankwar game. We referenced the program:<br>
https://github.com/keon/deep-q-learning/blob/master/dqn_batch.py<br>
We currently didn't make changes to it but we may modify it later.<br>
- ai_agent_play.py

# Report:

## Problem Statement:

The objective of this project is to create an AI agent capable of playing the Battle City Tanks game. The agent will control a tank in a dynamic, maze-like battlefield, engaging enemy tanks, and protecting its own base. That means this project will explore complex tactics and defensive maneuvers in an environment with partially unpredictable elements, pushing beyond traditional decision-making approaches.
Due to the large state space and the need to flexibly adjust the strategy according to the real-time situation, we believe that the Expectimax algorithm will be difficult to achieve performance comparable to human players. Therefore, we select to use reinforcement learning to implement our ai agent.


### The uncertainties involved:

●Enemy Tank Behavior: Enemy tanks' strategies and movements are unpredictable.<br>
●Map Variability: The map layout may vary in different games. The location of walls may affect the path of action and decisions.<br>
●Game Dynamics change: The destruction of walls and evolving base status increase the complexity of state transitions and decision-making.<br>
●Data and Engine Integration: There may be challenges in capturing real-time game state data and interfacing reliably with the game engine, especially under rapidly changing conditions.<br>

### Non-Trivial Aspects:

● The problem requires learning complex strategies for both offense and defense, as the agents must adapt to unpredictable enemy behavior and changing environments. <br>
●Incorporating reinforcement learning into a dynamic game environment, especially with the added complexity of coordinating multiple allied units presents significant challenges in state representation and reward design.<br>
●Traditional algorithms like Expectimax are no longer applicable, as we will leverage deep reinforcement learning to navigate the high-dimensional state and action spaces.<br>

### Existing Solution Methods

Markov Decision Process: https://web.stanford.edu/class/archive/cs/cs221/cs221.1192/2018/restricted/posters/diaozh/poster.pdf <br>
Reinforcement Learning:
https://arxiv.org/pdf/1602.04936
https://danisotelo.netlify.app/projects/reinforcement%20learning%20for%20tank%20battalion/ <br>
Multi-Agent Reinforcement Learning (MARL):
https://arxiv.org/pdf/1706.02275

## State space description:
- Natural language description of state space in draft report
- Complete mathematical description of states, transitions, actions, and observations

