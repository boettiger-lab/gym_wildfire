import gym
from stable_baselines3.common.env_checker import check_env

import gym_wildfire


def test_base_env():
    env = gym.make("wildfireCA-v0")
    check_env(env)
