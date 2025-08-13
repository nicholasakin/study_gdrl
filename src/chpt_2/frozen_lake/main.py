from frozen_lake.env import FrozenLake
import random



custom_map = [
    "SFFF",
    "FHFF",
    "FFFF",
    "HFGH"
]

env = FrozenLake(slippery=True, custom_layout=custom_map)


state = env.reset()
done = False
env.render()

num_steps = 20
counter = 0
while counter < num_steps:
    action = random.choice([0, 1, 2, 3])  # 0=left, 1=down, 2=right, 3=up
    state, reward, done = env.step(action)
    env.render()
    print(f"Action: {action}, State: {state}, Reward: {reward}, Done: {done}")
    counter += 1













