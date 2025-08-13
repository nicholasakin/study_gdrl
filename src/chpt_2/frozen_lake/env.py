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
        self.state_table: Dict[int, Dict[int, List[Tuple[int, float, int, bool]]]] = {}
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




class FrozenLakeHCode:
    def __init__(self, start_state: int = 0, name = "FrozenLakeHCode"):
        self.name = name
        self.grid_size = 4
        self.state = start_state

        '''
        Dictionary representing state, action
        inner keys: next state, transition probability, reward, is_terminal
        Total transition probabilty between 3 orthogonal directions is: 0.33*3
        actions:
         0 - Left
         1 - Down
         2 - Right
         3 - up

        '''
        self.state_table: dict = {
            0: { 
                0: [(0, 0.66, 0, False), (4, 0.33, 0, False)],
                1: [(4, 0.33, 0, False), (0, 0.33, 0, False), (1, 0.33, 0, False)],
                2: [(4, 0.33, 0, False), (0, 0.33, 0, False), (1, 0.33, 0, False)],
                3: [(0, 0.66, 0, False), (1, 0.33, 0, False)] },
            1: {0: [(0, 0.33, 0, False), (1, 0.33, 0, False), (5, 0.33, 0, True)],
                1: [(5, 0.33, 0, True),  (0, 0.33, 0, False), (2, 0.33, 0, False)],
                2: [(2, 0.33, 0, False), (1, 0.33, 0, False), (5, 0.33, 0, True)],
                3: [(1, 0.33, 0, False), (0, 0.33, 0, False), (2, 0.33, 0, False)]},
            2: {0: [(2, 0.33, 0, False), (1, 0.33, 0, False), (6, 0.33, 0, False)],
                1: [(6, 0.33, 0, False), (1, 0.33, 0, False), (3, 0.33, 0, False)],
                2: [(3, 0.33, 0, False), (2, 0.33, 0, False), (6, 0.33, 0, False)],
                3: [(2, 0.33, 0, False), (1, 0.33, 0, False), (3, 0.33, 0, False)]},
            3: {0: [(2, 0.33, 0, False), (7, 0.33, 0, True),  (3, 0.33, 0, False)],
                1: [(7, 0.33, 0, True),  (3, 0.33, 0, False), (2, 0.33, 0, False)],
                2: [(3, 0.66, 0, False), (7, 0.33, 0, True)],
                3: [(3, 0.66, 0, False), (2, 0.33, 0, False)]},
            4: {0: [(4, 0.33, 0, False), (8, 0.33, 0, False), (0, 0.33, 0, False)],
                1: [(8, 0.33, 0, False), (4, 0.33, 0, False), (5, 0.33, 0, True)],
                2: [(5, 0.33, 0, True),  (0, 0.33, 0, False), (8, 0.33, 0, False)],
                3: [(0, 0.33, 0, False), (4, 0.33, 0, False), (5, 0.33, 0, True)]},
            5: {0: [(4, 0.33, 0, False), (9, 0.33, 0, False), (1, 0.33, 0, False)],
                1: [(9, 0.33, 0, False), (4, 0.33, 0, False), (6, 0.33, 0, False)],
                2: [(6, 0.33, 0, False), (1, 0.33, 0, False), (9, 0.33, 0, False)],
                3: [(1, 0.33, 0, False), (4, 0.33, 0, False), (6, 0.33, 0, False)]},
            6: {0: [(5, 0.33, 0, True),  (10, 0.33, 0, False),(2, 0.33, 0, False)],
                1: [(10, 0.33, 0, False), (5, 0.33, 0, True), (6, 0.33, 0, True)],
                2: [(7, 0.33, 0, True), (2, 0.33, 0, False), (10, 0.33, 0, False)],
                3: [(2, 0.33, 0, False), (5, 0.33, 0, True),  (7, 0.33, 0, True)]},
            7: {0: [(6, 0.33, 0, False), (11, 0.33, 0, True), (3, 0.33, 0, False)],
                1: [(11, 0.33, 0, True), (7, 0.33, 0, True),  (6, 0.33, 0, False)],
                2: [(7, 0.33, 0, True), (11, 0.33, 0, True), (3, 0.33, 0, False)],
                3: [(3, 0.33, 0, False), (7, 0.33, 0, True), (6, 0.33, 0, False)]},
            8: {0: [(8, 0.33, 0, False), (12, 0.33, 0, True), (4, 0.33, 0, False)],
                1: [(12, 0.33, 0, False),(8, 0.33, 0, False), (9, 0.33, 0, False)],
                2: [(9, 0.33, 0, False), (4, 0.33, 0, False), (12, 0.33, 0, True)],
                3: [(4, 0.33, 0, False), (8, 0.33, 0, False), (9, 0.33, 0, False)]},
            9: {0: [(8, 0.33, 0, False), (13, 0.33, 0, False), (5, 0.33, 0, True)],
                1: [(13, 0.33, 0, False), (8, 0.33, 0, False), (10, 0.33, 0, False)],
                2: [(10, 0.33, 0, False), (5, 0.33, 0, True), (13, 0.33, 0, False)], 
                3: [(5, 0.33, 0, True),  (8, 0.33, 0, False), (10, 0.33, 0, False)]},
            10: {0: [(9, 0.33, 0, False), (14, 0.33, 0, False), (6, 0.33, 0, False)],
                1: [(14, 0.33, 0, False), (11, 0.33, 0, True), (9, 0.33, 0, False)],
                2: [(11, 0.33, 0, True), (6, 0.33, 0, False), (14, 0.33, 0, False)],
                3: [(6, 0.33, 0, False), (9, 0.33, 0, False), (11, 0.33, 0, False)]},
            11: {0: [(10, 0.33, 0, False), (15, 0.33, 1, True), (7, 0.33, 0, True)],
                1: [(15, 0.33, 1, True), (11, 0.33, 0, True), (10, 0.33, 0, False)],
                2: [(11, 0.33, 0, True), (7, 0.33, 0, True), (15, 0.33, 1, True)],
                3: [(7, 0.33, 0, True), (11, 0.33, 0, True), (10, 0.33, 0, False)]},
            12: {0: [(12, 0.66, 0, True), (8, 0.33, 0, False)],
                1: [(12, 0.66, 0, True), (13, 0.33, 0, False)],
                2: [(13, 0.33, 0, False), (8, 0.33, 0, False), (12, 0.33, 0, True)],
                3: [(8, 0.33, 0, False), (12, 0.33, 0, True), (13, 0.33, 0, False)]},
            13: {0: [(12, 0.33, 0, False), (13, 0.33, 0, False), (9, 0.33, 0, False)],
                1: [(13, 0.33, 0, False), (12, 0.33, 0, True), (14, 0.33, 0, False)],
                2: [(14, 0.33, 0, False), (9, 0.33, 0, False), (13, 0.33, 0, False)],
                3: [(9, 0.33, 0, False), (12, 0.33, 0, True), (14, 0.33, 0, False)]},
            14: {0: [(13, 0.33, 0, False), (14, 0.33, 0, False), (10, 0.33, 0, False)],
                1: [(14, 0.33, 0, False), (15, 0.33, 1, True), (13, 0.33, 0, False)],
                2: [(15, 0.33, 1, True), (10, 0.33, 0, False), (14, 0.33, 0, False)],
                3: [(10, 0.33, 0, False), (13, 0.33, 0, False), (15, 0.33, 1, True)]},
            15: {0: [(14, 0.33, 0, False), (15, 0.33, 1, True), (11, 0.33, 0, False)],
                1: [(15, 0.66, 1, True), (14, 0.33, 0, False)],
                2: [(15, 0.66, 1, True), (11, 0.33, 0, True)],
                3: [(11, 0.33, 0, True), (14, 0.33, 0, False), (15, 0.33, 1, True)]},
        } # state_table


    def step(self, action: int) -> Tuple[int, int, bool]:
        transitions = self.state_table[self.state][action]
        chosen = random.choices(transitions, weights=[t[1] for t in transitions])[0]
        next_state, _, reward, done = chosen
        self.state = next_state

        return next_state, reward, done

    def reset(self):
        self.state = 0
        return self.state

