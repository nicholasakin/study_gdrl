import numpy as np
import math
import random
from typing import Tuple

class BanditWalkEnv():
    '''
    Grid world
    [0] [1] [2] 

    Corridor with 3 states, 0,1,2.
    State 0 is a hole, a terminal state with no reward.
    State 1 is a state, non-terminal, no reward.
    State 2 is a terminal state of reward +1.
    '''

    def __init__(self, start_state:int=1):
        """Initializes the environment with agent at the start state

        Args:
            start_state (int): Starting state of the agent.
        """
        self.state: int = start_state
        self.next_state: int = 0
        '''
        -state table is of keys state
            state 1, state2, state3 

        - At each state, the agent can take two actions, 0 (left), 1 (right)

        - Each action results in the next_state, reward, and if it is a terminal
        '''
        self.state_table: dict = {
            0: {
                0: [
                    (0, 0.8, 0, True),
                    (1, 0.2, 0, False)
                ],
                1: [
                    (1, 0.8, 0, False),
                    (0, 0.2, 0, True),
                ]
            }, #state: 0
            1: {
                0: [
                    (0, 0.8, 0, True),
                    (2, 0.2, 1, True)
                ],
                1: [
                    (2, 0.8, 1, True),
                    (0, 0.2, 0, True)
                ]
            }, #state: 1
            2: {
                0: [
                    (1, 0.8, 0, True),
                    (2, 0.2, 1, True)
                ],
                1: [
                    (2, 0.8, 0, True)
                    (1, 0.2, 0, True)
                ]
            } #state: 2
        } #self.state_table




    def step(self, action:int) -> Tuple[int, int, bool]:
        """A single step through the environment.

        Args:
            action (int): Action by the agent.
        """
        probs = []
        for tup in self.state_table[self.state][action]:
            (next_state,
             trans_prob,
             reward,
             is_terminal) = tup
            probs.append(trans_prob)

        selected_action = random.choices([0,1], weights=probs)
        (next_state,
         trans_prob,
         reward,
         is_terminal) = self.state_table[self.state][selected_action]

        self.state = next_state
        
        return (next_state, reward, is_terminal)






    