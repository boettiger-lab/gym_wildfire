import gym
import gym_wildfire
import numpy as np
import argparse

BURNING_FUEL = [160]

# Parsing CL arguments to allow for GUI display
parser = argparse.ArgumentParser()
parser.add_argument("--display", dest='display', action='store_true')
parser.add_argument("--no-display", dest='display', action='store_false')
parser.set_defaults(display=False)
args = parser.parse_args()

env = gym.make("wildfireCA-v0", display=args.display)
obs = env.reset()
rewards = []
done = False
rewards.append(0)
while done is False:
    # Here I find where there are cells on fire, then I do preventative burns in
    # the Moore neighborhood. If there are additional actions available, the agent
    # burns the (0, 0) cell repeatedly.
    indices = np.where(obs == BURNING_FUEL)
    action = []
    if len(indices[0]) > 0:
        center = (indices[0][0], indices[1][0])
        for x, y in [(center[0]-1, center[1]-1), (center[0]-1, center[1]), 
                     (center[0]-1, center[1]+1), (center[0], center[1]+1), 
                     (center[0], center[1]-1), (center[0]+1, center[1]-1),
                     (center[0]+1, center[1]), (center[0]+1, center[1]+1)]:
            if not (0 <= x < env.dimension and 0 <= y < env.dimension):
                continue
            else:
                action.extend((x, y))
    while len(action) < 16:
        action.append(0)
    obs, reward, done, _ = env.step(action)
    rewards.append(reward)

print(sum(rewards))
