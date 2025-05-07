# Final Report for Tank AI Project

Team Members: Jinglong Deng, Chang Li<br>
Github Link: https://github.com/dnjgld/6511_proj<br>
Video Links for AI Agent playing on 3 different maps:<br>
https://youtu.be/IxrEAwZBrLg <br>

# Notes:

Please check the main branch;<br>
We used the code of pygame-TankWar repository<br>
Github website: https://github.com/HelloZhan/pygame-TankWar<br>
Introduction Website: https://blog.csdn.net/qq_46470984/article/details/122003755<br>
There were too many Chinese comments in the original program so we didn’t replace them.<br>

We mainly did edition on:<br>
- game_loader.py<br>

We created:<br>
- ai_agent.py<br>
This file implement the Deep Q-Network (DQN) agent for tankwar game. We referenced the programs:<br>
https://github.com/keon/deep-q-learning/blob/master/dqn_batch.py<br>
https://github.com/flyyufelix/VizDoom-Keras-RL/blob/4fc27ce3d400eba5422d39e2fad565d0503a6149/ddqn.py<br>
- ai_agent_play.py<br>
- ai_agent_train.py<br>
- tank_dqn.keras (trained model file)<br>
- tank_dqn_training.keras (current training model file)<br>
- tank_dqn_replay.pkl (memory buffer for retraining)<br>


# Software Requirements and Implementation Steps

Python 3.10<br>
TensorFlow 2.x<br>
Dependencies in requirements.txt<br>

## Setup instructions:

We recommend to create a virtual python environment and use the requirements.txt file to import all dependencies:

```bash
conda create -n tankagent python=3.10
conda activate tankagent
pip install -r requirements.txt
```

main.py is not used in our project.

To train the agent:

```bash
python ai_agent_train.py
```
It will train the model saved in file_name='tank_dqn_training.keras'. <br>
You can set the number of episodes, the number of enemies and whether to render the screen in the program.<br>
The current 'tank_dqn_training.keras' only takes 6 inputs because it was trained in 1-enemy situation.<br>
If you want to train on more enemies, you can delete this model file or edit the file_name in the program.<br>

To use the trained agent to play the game:

```bash
python ai_agent_play.py
```
This will load the trained model 'tank_dqn.keras' and let the AI agent play the game automatically. <br>
You can also change file_name to use other model files.<br>
The number of enemies needs to match the number of enemies the model is trained with.<br>
You can change checkpoint from 1 to 35 to play different maps, but only 1, 2, 3 are basically winable<br>

# Report:

This report describes our attemption in developing of an AI agent capable of playing the Battle City Tanks game using deep Q-learning (DQN). We tried to let the ai agent learning to make decisions based on the state of the game, such as get close to enemy tanks, engage enemy tanks, and protect the base. 

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

### Existing Solution Methods:

Markov Decision Process: 
A mathematical framework used to model decision-making problems where outcomes are partly random and partly under the control of the agent. MDPs have been widely used in game AI, such as in board games like chess and Go.
https://web.stanford.edu/class/archive/cs/cs221/cs221.1192/2018/restricted/posters/diaozh/poster.pdf
Reinforcement Learning:
The method of learning optimal behaviors through interactions with an environment. Q-learning, and its deep learning extension DQN, are common approaches for training agents in complex environments.
 https://arxiv.org/pdf/1602.04936 https://danisotelo.netlify.app/projects/reinforcement%20learning%20for%20tank%20battalion/
Multi-Agent Reinforcement Learning (MARL):
This technique involves multiple agents learning to interact with each other within the environment. MARL has been applied to games with multiple agents, such as Battle City Tanks, where enemy tanks are controlled by their own policies.
 https://arxiv.org/pdf/1706.02275

## State Space, Actions, Transitions, and Observations
### State Space Description:<br>
The state space of our system captures the positions, health, and interactions between the player's tank and enemy tanks. <br>
We chose to simplify the representation by omitting some elements, such as the tank's direction, which did not significantly affect training. <br>
The state is represented as a fixed-length vector:<br>
- Player's Tank: (position, life)<br>
- Enemy Tanks: (up to three enemies; position, life)<br>

The state is normalized, with positions expressed relative to the game map<br>

### Mathematical Description:
State:
s = (px, py, l, e_{i,x}, e_{i,y}, e_{i,l}), i = {1}
Where:
px,py are the player's tank position
l is the player's tank life
e_{i,x}, e_{i,y} are the enemy tank positions<br>
e_{i,l} is the enemy i's tank life<br>

### action space:<br>
a = {0,1,2,3,4}<br>
a = 0 means move up<br>
a = 1 means move down<br>
a = 2 means move left<br>
a = 3 means move right<br>
a = 4 means shoot<br>

### transition:<br>
T(s, a) = s', where the state transitions from s to s' after taking action a<br>
The new state depends on the current state, action taken, and environmental changes (e.g., tank movement, bullet collisions).<br>

### observation:<br>
The agent observes the new state after each action, which includes the player's and enemies' positions, health, and other relevant game variables.<br>
so the observation is:<br>
o = s'


## Solution Method 
Our approach involves using Deep Q-Networks (DQN) for the agent's learning process. DQN is an extension of Q-learning that uses a neural network to approximate the action-value function, allowing it to handle high-dimensional state spaces such as the one in Battle City Tanks. The solution method includes the following steps:<br>
- Action Selection: The agent chooses actions using an epsilon-greedy strategy, where it either explores randomly or exploits its learned policy.
- Learning: The agent updates its Q-values by performing experience replay, storing past experiences and sampling random batches to learn from.
- Reward Calculation: The reward function is designed to incentivize the agent for actions that lead to favorable outcomes (e.g., killing enemies, surviving longer) and penalize it for bad decisions (e.g., agent tank destruction).

### Implementation of the Solution Method for the Problem
The implementation of our solution revolves around several key components in the game_loader.py file, responsible for managing the state, action transitions, and reward calculations:

- State Representation (get_current_state)<br>
The state is represented as a vector containing the positions and health of the player's tank and enemy tanks. This vector is normalized to fit within a fixed range for training.

- State Transition (get_successor_state)<br>
This function applies the agent's chosen action, updates the game environment, and calculates the new state. It also calculates the reward based on the state transition and checks if the game has been won or lost.

- Reward Calculation (reward_calculation)<br>
The reward_calculation function defines how rewards are assigned based on the transition from one state to another. Several conditions are used to compute the reward:<br>
Game Over: A large negative reward is given if the game ends in a loss.<br>
Winning the Game: A positive reward is assigned if the player defeats all enemies.<br>
Tank Destruction: A penalty is given if the player's tank loses life.<br>
Enemy Destruction: A positive reward is given if an enemy tank is destroyed.<br>
Proximity to Enemy: A small positive reward is given if the player moves closer to an enemy tank.<br>
This reward structure encourages the AI to not only survive but also to engage enemies and protect the base. It also incentivizes the agent to get closer to enemies for strategic attacks.<br>

- AI Play and Gameplay(game_running_ai_play)<br>
In the game_running_ai_play function, the agent autonomously plays the Battle City Tanks game without external control. The gameplay loop continues until the game reaches a win or loss condition. During each step of the game, the agent chooses actions based on the current game state, applies those actions, and observes the resulting state and rewards.

- AI Training and Gameplay(game_running_ai_trainning)<br>
In the game_running_ai_trainning function, the agent is trained over multiple episodes. The gameplay loop runs for a specified number of episodes (episodes=500 by default) and each episode consists of several steps, where the agent chooses actions, receives rewards, and learns from its experience.

The epsilon-greedy strategy is used during training, where the agent explores the environment randomly with a probability of epsilon and exploits its learned policy with a probability of 1-epsilon.

The training process includes:<br>
Experience Replay: The agent stores transitions in a memory buffer and samples batches for learning.<br>
Target Network Update: The target network is updated periodically to stabilize training.<br>
Model Saving: The agent's model and memory buffer are saved after every episode.<br>

### Rule-Based Action Selection<br>
In addition to the reinforcement learning-based actions, we implemented a rule-based action selection for the AI agent. This method prioritizes actions like shooting when an enemy is in the same row or column, or moving towards the nearest enemy when no immediate threats are present.<br>
This rule-based approach serves as a fallback when the agent is uncertain or needs to act quickly based on straightforward heuristics.<br>

#### We have other three main files for implementation:

#### Ai_agent.py
It is the AI agent class we build on DQN.
The contained parameters are: 
- state_size: number of input features in state
- action_size: number of actions
- memory: experience replay buffer, used to store the history of the agent's experience (state, action, reward, next state, end or not).
- gamma: discount factor that determines how much influence future rewards will have. (we set it to 0.95)
- epsilon: initial exploration rate, which controls the probability of agent to take a random action (we set a default value 1.0).
- epsilon_min: minimum value for the exploration rate so it can keep training (we set it to 0.01)
- epsilon_decay: decay factor of the exploration rate. (We moved the epsilon decay after every episode so it won't decrease too fast)
- learning_rate: learning rate of the neural network. (we set it to 0.001).
- model: main Q network, used to predict the Q value of each action in the current state.
- target_model: target Q network, used to calculate the target Q value to improve the training stability.


The methods are:
- _build_model(self)<br>
Used to build a neural network, <br>
In our program, we have two layers of 128-unit ReLU and one layer of linear output for prediction.<br>
- update_target_model(self)<br>
Copy the weights from the main Q network to the target Q network to update the target network.<br>
remember(self, state, action, reward, next_state, done)<br>
Store an experience (state, action, reward, next_state, done or not) into the playback buffer.<br>
- act(self, state)<br>
Select an action based on the current state. <br>
With probability ε, a random action is selected,<br>
With probability 1-ε, the action with the largest Q value is selected.<br>
- replay(self, batch_size)<br>
Randomly sample a batch of experiences from the experience replay buffer to update the network parameters;<br>
- load(self, path)<br>
Load the saved model weights from the specified path.<br>
- save(self, path)<br>
Save the current model weights to the specified path.<br>
- save_replay_buffer(self, path)<br>
Save the experience playback buffer to a file for continued training.<br>
- load_replay_buffer(self, path)<br>
Load the experience playback buffer from a file.<br>


#### ai_agent_train.py
One separate python file to run the function game_running_ai_training where you can change:
number of episodes of training,
enemy_num, 
state_size (automatically calculated from enemy_num), 
whether to render the screen in training or not (choose not render could fasten the training),
initial epsilon for retraining existing model,
the model file path using for ai-training,
the replay buffer file path using for ai-training


#### ai_agent_play.py
One separate python file to run the function game_running_ai_play where you can change:
enemy_num, 
state_size (automatically calculated from enemy_num),
checkpoint (the id of maps) 
the model file path using for ai-playing

## Conclusion

From our results, our agent has a better training effect when there is only one enemy in the same map. It can train a model to solve the current level and win stably. But when we try to add multiple enemies or use multiple maps for training, the model performance decreases significantly and often fails to win.
This is first related to our state design. Our state design does not add variables related to the map, which has little impact on a single map, but when there are multiple maps, the same state transition may have very different rewards.  Also, adding the number of enemies greatly expands the state space size, making learning more difficult.
Secondly, I think our reward function is not good enough. Perhaps a more detailed reward function can better guide the agent, but a more detailed reward function also means more calculations, which makes training more time-consuming, which makes it difficult for us to add more detailed reward function rules.
In short, we think that our current DQN method is not perfect enough and needs to further optimize the state design and reward function to improve its performance in multiple enemies and multiple maps. Alternatively, more advanced algorithms can be adopted to improve training efficiency

## Contribution specification

The contribution of team members are as follows:

### Jinglong:<br>
Base game code adaptation and integration so that it can interface with AI agent.<br>
Implementation of the basic DQN agent.<br>
Training AI agent on separate branch and explore the training effects under different settings<br>
Write the report. (Notes; Software Requirements and Implementation Steps; Problem Statement; The uncertainties involved; Solution Method; Conclusion) <br>

### ChangLi:<br>
Reward function refinement, current state access and transition(get_current_state, get_successor_state)<br>
Training AI agent on separate branch and explore the training effects under different settings<br>
Write the report (Non-Trivial Aspects; Existing Solution Methods; State Space, Actions, Transitions, and Observations; Solution Method)<br>
