from bandit_walk.env import BanditWalkEnv
import random


num_times = 5

for i in range(num_times):
    print(f"\nNum Times Run: {i}")
    bw = BanditWalkEnv(start_state=1)


    is_terminal = False
    while not is_terminal:


        action = random.choice([0,1])


        next_state, reward, is_terminal = bw.step(action=action)
        print(f"I am in state: {next_state} with reward {reward}")
        print(f"This is terminal {is_terminal}")












