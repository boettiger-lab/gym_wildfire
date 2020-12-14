## Env and Utils

- `env_wildfire_ca.py`: This defines the "wildfireCA-v0" environment. 

- `wildfire_ca.py`: This defines the "wildfireCA" object which allows the user to do some very basic wildfire modelling. It's a celllular automaton model where each cell can either be inflammable or flammable. And if flammable, a cell can be unburned, burning or burned. The dynamics for wildfire spread are very simple, basically if a neighboring cell is burning, the cell can ignite with some probability. If you run this script as `python wildfire_ca.py`, there will be a GUI displaying the dynamics. 
