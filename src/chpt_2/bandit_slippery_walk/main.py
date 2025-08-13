from bandit_walk.env import BanditWalkEnv
import random


num_steps = 10

bw = BanditWalkEnv(start_state=1)
for i in range(num_steps):
    print(f"\nRun: {i}")

    is_terminal = False
    if is_terminal:
        print("In terminal state")

    action = random.choice([0,1])
    if action == 0:
        a = "left"
    else:
        a = "right"

    (next_state,
     reward,
     is_terminal) = bw.step(action=action)
    print(f"I chose action {a}\n"
          f"Now in state: {next_state}\n"
          f"With reward {reward}")
    print(f"This is terminal {is_terminal}")












