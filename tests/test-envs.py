import gym
import gym_wildfire
import numpy as np
from stable_baselines3.common.env_checker import check_env

env = gym.make("wilfireCA-v0")
check_env(env)
