# gym_wildfire

This repository provides [OpenAI-gym](https://github.com/openai/gym/) class definitions for wildfire management control problems.  See [Creating your own Gym Environments](https://github.com/openai/gym/blob/master/docs/creating-environments.md) for details on how a new gym environment is defined.

## Installation

Run `pip install -e .` from the home directory (preferably in a separate virtual environmetn) to get the requisite python packages installed.

## Environments

So far, we have the following environments defined:

- `wildfireCA-v0`: This defines a wildfire cellular automata model, based off of [Alexandridis et al.](https://www.sciencedirect.com/science/article/abs/pii/S0096300308004943). The dynamics here are quite simple, allowing for wind, variation in vegetation type and density, and elevation. The agent is allowed to do a variable number of preventative burns per evolution time step. 


