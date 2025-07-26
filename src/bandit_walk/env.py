import numpy as np
from typing import tuple

class BanditWalkEnv():
    '''
    Grid world
    [0] [1] [2] 

    Corridor with 3 states, 0,1,2.
    State 0 is a hole, a terminal state with no reward.
    State 1 is a state, non-terminal, no reward.
    State 2 is a terminal state of reward +1.
    '''

    def __init__(self, start_state):
        state: int = 0 
        next_state: int = 0
        state_table: dict = {state: 0}

        transition_probs: int = 0



    def step(self, action:int) -> tuple(int, int, int, bool):
        """A single step through the environment.


        Args:
            action (int): Action by the agent.
        """
        reward, next_state, is_terminal = self.state_table[self.state][action]
        self.state = next_state
        if not is_terminal:
            

        return (reward, next_state, is_terminal)

        




    