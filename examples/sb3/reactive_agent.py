import gym
import gym_wildfire
import numpy as np
import argparse

BURNING_FUEL = 80

# Parsing CL arguments to allow for GUI display
parser = argparse.ArgumentParser()
parser.add_argument("--display", dest="display", action="store_true")
parser.add_argument("--no-display", dest="display", action="store_false")
parser.add_argument("--env", type=str, default="wildfireCA-v0")
parser.set_defaults(display=False)
args = parser.parse_args()

env = gym.make(args.env, display=args.display, wind_velocity=25)
obs = env.reset()
rewards = []
done = False
rewards.append(0)
while done is False:
    # Here I find where there are cells on fire, then I do preventative burns in
    # the Moore neighborhood. If there are additional actions available, the agent
    # burns the (0, 0) cell repeatedly.
    indices = [[] for i in range(len(obs))]
    for index, row in enumerate(obs):
        for x in row:
            indices[index].append(x[0])
    indices = np.where(np.array(indices) == BURNING_FUEL)
    action = []
    position_list = []
    if len(indices[0]) > 0:
        center = (indices[0][0], indices[1][0])
        for x, y in [
            (center[0] - 1, center[1] - 1),
            (center[0] - 1, center[1]),
            (center[0] - 1, center[1] + 1),
            (center[0], center[1] + 1),
            (center[0], center[1] - 1),
            (center[0] + 1, center[1] - 1),
            (center[0] + 1, center[1]),
            (center[0] + 1, center[1] + 1),
        ]:
            if not (0 <= x < env.dimension and 0 <= y < env.dimension):
                continue
            else:
                position_list.extend([x, y])
    for i in range(8):
        if len(position_list) == 0:
            obs, reward, done, _ = env.step([None, None])
        else:
            obs, reward, done, _ = env.step(position_list[:2])
            position_list = position_list[2:]
        rewards.append(reward)

print(sum(rewards))
