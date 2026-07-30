# Reinforcement Learning & Optimization Repository

This repository contains my coursework and experiments for the Reinforcement Learning course at Howest. It includes implementations of various search algorithms, reinforcement learning agents, and interactive visualizations.

##  Key Projects & Scripts

### 1. A* Pathfinding Visualization (`astar.py`)
An interactive Pygame-based visualization of the A* pathfinding algorithm with multiple heuristic functions.

- **Features**: 
  - Real-time pathfinding
  - Weighted Euclidean, Manhattan, Chebyshev, and Octile heuristics
  - Interactive wall drawing and start/goal placement
- **Controls**:
  - `Space`: Run/Pause
  - `S` + Click: Set Start
  - `G` + Click: Set Goal
  - `Left Click`: Draw Wall
  - `Right Click`: Erase Wall
  - `1-4`: Switch Heuristics
  - `[` / `]`: Adjust heuristic weight

### 2. Search-Based Optimization (`cartpole_search.py`)
A comprehensive CLI tool exploring search-based optimization methods on the **CartPole-v1** environment.

**Supported Algorithms:**
- Random Search
- Hill Climbing
- Simulated Annealing (with optional adaptive noise)
- Angle-based Heuristic Policy

**Usage Examples:**
```bash
# Run Random Search
python cartpole_search.py --task random_search --iters 1000

# Run Hill Climbing
python cartpole_search.py --task hill --iters 1000 --sigma 0.1

# Run Simulated Annealing with Adaptive Noise
python cartpole_search.py --task anneal --iters 1000 --adaptive --plot sa_results.png
```

### 3. Actor-Critic LunarLander (`ActorCritic_LunarLander.py`)
Implementation of an **Advantage Actor-Critic (A2C)** agent for solving the `LunarLander-v2` environment using TensorFlow/Keras.

### 4. Policy Gradients (`reinforcethis.py`, `reinforce.py`)
Scripts experimenting with the **REINFORCE** algorithm and reward discounting mechanisms.

##  Course Notebooks

The repository includes Jupyter Notebooks covering course sessions:
- `Session_01_Assignment`: Intro to RL concepts
- `Session_02_Multi...`: Multi-armed Bandits
- `Session_03_Temporal...`: TD Learning (SARSA, Q-Learning)
- `Session_04_DQN...`: Deep Q-Networks
- `Session_05_Policy_Gradients...`: Policy Gradient methods

###  Lab Exam
- `Reinforcement_Learning_Lab_Exam...`: The final lab exam for the course, containing implemented solutions and analysis.


##  Dependencies

To run the scripts in this repository, you will need:

- Python 3.8+
- `gymnasium` (and `gymnasium[box2d]` for LunarLander)
- `pygame`
- `numpy`
- `tensorflow`
- `matplotlib`
- `seaborn`

```bash
pip install gymnasium[box2d] pygame numpy tensorflow matplotlib seaborn
```

##  Author
**Pascal Musabyimana**
Reinforcement Learning Course - Howest
