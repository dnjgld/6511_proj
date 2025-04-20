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
Due to the large state space and the need to flexibly adjust the strategy according to the real-time situation, we believe that the Expectimax algorithm will be difficult to achieve performance comparable to human players. Therefore, we select to use reinforcement learning to implement our ai agent. We decided to use level mode to train our ai agent, in this code there are 35 levels, ideally 15 levels can be passed.


### The uncertainties involved:

- Enemy Tank Behavior: Enemy tanks' strategies and movements are unpredictable.<br>
- Map Variability: The map layout may vary in different games. The location of walls may affect the path of action and decisions.<br>
- Game Dynamics change: The destruction of walls and evolving base status increase the complexity of state transitions and decision-making.<br>
- Data and Engine Integration: There may be challenges in capturing real-time game state data and interfacing reliably with the game engine, especially under rapidly changing conditions.<br>

### Non-Trivial Aspects:

- The problem requires learning complex strategies for both offense and defense, as the agents must adapt to unpredictable enemy behavior and changing environments. <br>
- Incorporating reinforcement learning into a dynamic game environment, especially with the added complexity of coordinating multiple allied units presents significant challenges in state representation and reward design.<br>
- Traditional algorithms like Expectimax are no longer applicable, as we will leverage deep reinforcement learning to navigate the high-dimensional state and action spaces.<br>

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

## What the agent needs to know at every frame
1. Our tank itself: its grid-cell position(row,col), the direction it's facing(up/down/left/right) and whether the gun is on cooldown
2. Bullets already in flight: for every shell on screen we track its current(row,col) cell and heading. A bullet disappears when it hits a wall, tank or map edge, so its life-span matters for predicting danger.
3. Enemy tanks (up to four at once): Each enemy's position, facing direction and remaining "health" (one hit kills most, but some special tanks take several shots). Enemy movement is semi-random, so the agent uses their current heading plus map layout to anticipate their next cell.
4. Our base: a single, fixed cell the agent must protect. Two facts matter: (a)is the base still intact; (b) how much brick wall still surrounds it(those bricks can be shot away).
5. Static terrain - a 26 x 26 grid describing what occipies every cell right now:
- indestructible steel
- destructible brick (present/absent)
- river, ice, forest (slow or hide movement)
- empty ground
Because bricks disappear when hit, this layer changes during play and therefore belongs in the state.
6. Power-ups("food" in the source): if a star, helmet, shovel, bomb, clock or tank-life icon is showing, we record its type and cell. They time-out after a few seconds, so the remaining timer is also part of state.
7. Game phase variables: current level(1-35), score remaining lives, and the global tick counter. They are not needed for a single decision, but they matter over an episode for rewards and curriculum learning.

## Why these pieces(and not more)
Everything above directly changes either (1) the legal moves we can take next, or (2) the reward we will recieve soon (survive, kill an enemy, lose the base, collect a power-up). Items such as the exact sprite image or sound channel don't affect gameplay decision, so we leave them out.

This mirrors the outline already in the proposal but fills in the details that the grader will look for: bullets, bricks, power-ups and base shielding in addition to simple tank coordinates.
