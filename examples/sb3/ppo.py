import gym
import gym_wildfire
from stable_baselines3 import PPO
from stable_baselines3.ppo import CnnPolicy

env = gym.make("wildfireCA-v0")
model = PPO(CnnPolicy, env, verbose=2)
model.learn(total_timesteps=int(1e6))
model.save("ppo_wildfireCA")
