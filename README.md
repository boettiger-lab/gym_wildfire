# gym_wildfire

This repository provides [OpenAI-gym](https://github.com/openai/gym/) class definitions for wildfire management control problems.  See [Creating your own Gym Environments](https://github.com/openai/gym/blob/master/docs/creating-environments.md) for details on how a new gym environment is defined.

## Installation

Run `pip install -e .` and `pip install -r requirements.txt` from the home directory (preferably in a separate virtual environmetn) to get everything ready to run.

## Environments

So far, we have the following environments defined:

- `wildfireCA-v0`: This defines a wildfire cellular automata model. The dynamics here are very simple and the agent is allowed to do prevantative burns in 8 cells at each timestep. 

## Future Directions

After finding some decent agent behavior on this first environment, we plan on building additional cellular automata models that have more complex and accurate dynamics. Additionally, we will probably change the action space to be more realistic. The inspiration for creating this environment came from the recent [Purnomo et al. paper](https://www.sciencedirect.com/science/article/pii/S1540748920306490), which shows that cellular automata models can be very accurate for describing peat moss fires.
