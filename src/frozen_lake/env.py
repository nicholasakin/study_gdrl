import numpy as np
import random
from typing import Tuple, Dict, List, Optional

class FrozenLake:
    def __init__(self, start_state: int = 0, slippery: bool = True, custom_layout: Optional[List[str]] = None):
        self.grid_size = 4
        self.state = start_state
        self.slippery = slippery
        self.layout = custom_layout or [
            "SFFF",
            "FHFH",
            "FFFH",
            "HFFG"
        ]
        self.goal_states = []
        self.terminal_states = []
        self._init_states()
        self._build_transition_table()

    def _init_states(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                char = self.layout[i][j]
                if char == "H":
                    self.terminal_states.append((i, j))
                elif char == "G":
                    self.goal_states.append((i, j))

    def _build_transition_table(self):
        self.state_table: Dict[int, Dict[int, List[Tuple[int, float, int, bool]]]] = {}
        for s in range(self.grid_size ** 2):
            row, col = divmod(s, self.grid_size)
            self.state_table[s] = {}
            for action in range(4):  # 0:left, 1:down, 2:right, 3:up
                transitions = []
                moves = self.get_slippery_moves(action) if self.slippery else [action]
                prob = 1.0 / len(moves)
                for actual_move in moves:
                    new_row, new_col = self.move(row, col, actual_move)
                    new_state = self.to_state(new_row, new_col)
                    is_terminal = (new_row, new_col) in self.terminal_states
                    is_goal = (new_row, new_col) in self.goal_states
                    reward = 1 if is_goal else 0
                    transitions.append((new_state, prob, reward, is_terminal or is_goal))
                self.state_table[s][action] = transitions

    def to_state(self, row: int, col: int) -> int:
        return row * self.grid_size + col

    def move(self, row: int, col: int, action: int) -> Tuple[int, int]:
        if action == 0 and col > 0: col -= 1       # left
        elif action == 1 and row < self.grid_size - 1: row += 1  # down
        elif action == 2 and col < self.grid_size - 1: col += 1  # right
        elif action == 3 and row > 0: row -= 1     # up
        return row, col

    def get_slippery_moves(self, action: int) -> List[int]:
        left = (action - 1) % 4
        right = (action + 1) % 4
        return [left, action, right]

    def step(self, action: int) -> Tuple[int, int, bool]:
        transitions = self.state_table[self.state][action]
        chosen = random.choices(transitions, weights=[t[1] for t in transitions])[0]
        next_state, _, reward, done = chosen
        self.state = next_state
        return next_state, reward, done

    def reset(self):
        self.state = 0
        return self.state

    def render(self):
        print()
        for i in range(self.grid_size):
            row = ""
            for j in range(self.grid_size):
                state_id = self.to_state(i, j)
                if state_id == self.state:
                    row += "A "  # Agent
                else:
                    char = self.layout[i][j]
                    if char == "S": row += ". "
                    elif char == "F": row += "- "
                    elif char == "H": row += "H "
                    elif char == "G": row += "G "
            print(row)
        print()
