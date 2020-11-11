import gym
import gym_wildfire
import numpy as np

BURNING_FUEL = [160]
env = gym.make("wildfireCA-v0", display=True)
obs = env.reset()
rewards = []
done = False
rewards.append(0)
while done is False:
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

