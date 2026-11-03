# Artificial Intelligence Concept (AIC)

This repository contains learning modules, practical implementations, and comparative benchmarks for fundamental **Artificial Intelligence (AI)** problem-solving paradigms, focusing on **Uninformed (Blind)** and **Informed (Heuristic)** search algorithms.

These materials are based on standard AI curricula and reference *Russell & Norvig's Artificial Intelligence: A Modern Approach (AIMA, 4th Edition, Chapter 3)*.

---

## 📌 Overview

Search algorithms are central to classical Artificial Intelligence, where an intelligent agent explores a discrete state space to navigate from an initial configuration to a predefined goal state.

### Key Search Paradigms Explored

1. **Uninformed (Blind) Search**
   - Operates without domain-specific knowledge beyond the problem formulation (action costs, state transitions, goal tests).
   - **Algorithms Covered:**
     - **DFS (Depth-First Search)**: Explores deepest unvisited nodes first (LIFO stack).
     - **BFS (Breadth-First Search)**: Explores level by level (FIFO queue), guaranteeing shortest-hop path.
     - **UCS (Uniform Cost Search)**: Expands lowest-cost paths first using priority queues (Dijkstra's equivalent).
     - **DLS (Depth-Limited Search)**: DFS bounded by depth limit $\ell$ to prevent infinite loops.
     - **IDS (Iterative Deepening Search)**: Combines space efficiency of DFS with the optimality of BFS.
     - **Bidirectional Search**: Simultaneous search forward from start and backward from goal (demonstrated with chess knight moves).

2. **Informed (Heuristic) Search**
   - Leverages heuristic functions $h(n)$ to guide the frontier toward the goal more efficiently.
   - **Algorithms Covered:**
     - **GBFS (Greedy Best-First Search)**: Prioritizes nodes purely by lowest heuristic distance $h(n)$.
     - **A\* Search**: Balances historical cost $g(n)$ and predicted cost $h(n)$ with $f(n) = g(n) + h(n)$, ensuring optimality when $h(n)$ is admissible and consistent.
     - **IDA\* (Iterative Deepening A\*)**: Memory-bounded search using cost thresholds ($f$-limits).
     - **RBFS (Recursive Best-First Search)**: Linear-space best-first search that tracks alternative candidate branches.
     - **SMA\* / Bounded-Frontier Search**: Prunes worst candidates when memory constraints are reached.
     - **Weighted A\***: Suboptimal heuristic weighting $f(n) = g(n) + w \cdot h(n)$ to accelerate search speed and reduce memory expansions.

---

## 📂 Repository Structure

```text
├── data/
│   ├── search_lab.py               # Lab maze benchmarks, 8-puzzle configurations, visualizers
│   └── utils.py                    # Maze rendering and helper utilities
├── Modul_Pembelajaran_Uninformed_KKA.ipynb  # Uninformed Search Module & Labs
├── Modul_Pembelajaran_Informed_KKA.ipynb    # Informed Search Module & Labs
├── requirements.txt                         # Dependencies
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Jupyter Notebook / JupyterLab

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/PopSharkkk/artificial-inteligence-concept.git
   cd artificial-inteligence-concept
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Launch Jupyter:
   ```bash
   jupyter lab
   # or
   jupyter notebook
   ```

---

## 📊 Evaluation & Metrics

The implementations evaluate search strategies based on:
- **Completeness**: Does the algorithm guarantee finding a solution if one exists?
- **Optimality**: Does it find the lowest-cost solution path?
- **Time Complexity**: Number of nodes expanded and execution time.
- **Space Complexity**: Peak frontier / recursion stack size during execution.

---

## 📖 References
- Russell, S., & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach (4th Edition)*. Pearson.
- [AIMA Python Code Repository](https://github.com/aimacode/aima-python)
