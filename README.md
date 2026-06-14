# AI Assignment

| | |
|---|---|
| **Name** | Nirupam Chakraborty |
| **Semester** | 8th |
| **Roll No.** | 220710007040 |
| **Department** | Computer Science & Engineering (CSE) |

---

## Overview

This repository contains Python implementations of three classic Artificial Intelligence algorithms — Alpha-Beta Pruning, Hidden Markov Models, and Minimax-based Tic-Tac-Toe. Each program is self-contained and runnable from the terminal.

---

## Files

### 1. `alpha-beta-pruning.py` — Alpha-Beta Pruning Visualizer

An interactive visualizer for the **Alpha-Beta Pruning** algorithm, an optimization of the Minimax algorithm used in adversarial game trees.

**Features**
- Configurable tree depth (1–6) and branching factor (2–5)
- Manual or random leaf value input
- Full step-by-step trace of α and β updates in the terminal
- Matplotlib visualization with dark theme:
  - 🔵 Blue = MAX nodes
  - 🟡 Amber = MIN nodes
  - 🟢 Green = Leaf nodes
  - 🔴 Red = Pruned nodes/edges (dashed)
- Saves diagram as `alpha_beta_tree.png`

**How to run**
```bash
python alpha-beta-pruning.py
```

**Example output**
```
Depth (levels below root, 1–6): 3
Branching factor (children per node, 2–5): 2
...
Optimal value at root = 4
Pruned nodes: ['root→1→1→1']
Tree diagram saved → alpha_beta_tree.png
```

**Dependencies**
```bash
pip install matplotlib networkx
```

---

### 2. `hmm.py` — Hidden Markov Model (Patient Health)

A from-scratch implementation of a **Hidden Markov Model** applied to patient health monitoring, using the **Forward Algorithm** and **Viterbi Algorithm**.

**Model**
- **Hidden states:** `Healthy`, `Sick`
- **Observations:** `No Fever`, `Fever`
- **Initial probabilities (π):** Healthy = 0.7, Sick = 0.3
- **Transition matrix (A):** Models daily health transitions
- **Emission matrix (B):** Models probability of fever given health state

**Features**
- Forward Algorithm — computes `P(O | λ)`, the probability of the observation sequence
- Viterbi Algorithm — finds the most likely hidden state sequence
- What-if scenario analysis for three test observation sequences

**How to run**
```bash
python hmm.py
```

**Example output**
```
Observations: ['Fever', 'No Fever', 'Fever', 'Fever']

[Forward] P(O | λ) = 0.020892

[Viterbi] Most likely hidden states:
  t=0: Sick   (observed: Fever)
  t=1: Healthy (observed: No Fever)
  ...
```

**Dependencies**

None — pure Python standard library.

---

### 3. `tictactoe.py` — Tic-Tac-Toe with Minimax AI

A terminal-based **Tic-Tac-Toe** game where you play against an unbeatable AI powered by the **Minimax algorithm**.

**Features**
- Human plays as `X`, AI plays as `O`
- AI uses full Minimax search — it never loses
- Clean terminal board display
- Play-again prompt after each game

**How to run**
```bash
python tictactoe.py
```

**How to play**

Enter a number 1–9 corresponding to the board position:
```
 1 | 2 | 3
---+---+---
 4 | 5 | 6
---+---+---
 7 | 8 | 9
```

**Dependencies**

None — pure Python standard library.

---

## Algorithms at a Glance

| Algorithm | File | Concept |
|---|---|---|
| Alpha-Beta Pruning | `alpha-beta-pruning.py` | Optimized adversarial search by pruning branches that can't affect the outcome |
| Forward Algorithm | `hmm.py` | Dynamic programming to compute observation sequence probability |
| Viterbi Algorithm | `hmm.py` | Dynamic programming to find the most likely hidden state path |
| Minimax | `tictactoe.py` | Recursive game tree search assuming optimal play from both sides |

---

## Requirements

```bash
pip install matplotlib networkx
```

Python 3.8+ is required. `hmm.py` and `tictactoe.py` use only the standard library.
