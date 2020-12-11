import random
import sys
import os
from copy import deepcopy
from cellular_automaton import CellularAutomaton, MooreNeighborhood, CAWindow, EdgeRule


NO_FUEL = 0
UNBURNED_FUEL = 40
BURNING_FUEL = 80
BURNED = 120
PREVENTATIVE_BURN = 160
UNBURNED_INIT = [40, 80, 80, 0]
BURNING_INIT = [80, 80, 80, 0]

class wildfireCA(CellularAutomaton):
    def __init__(self):
        super().__init__(dimension=[36, 36],
                         neighborhood=MooreNeighborhood(EdgeRule.IGNORE_MISSING_NEIGHBORS_OF_EDGE_CELLS))

    def init_cell_state(self, __):
        # Initializing the grid with the following probabilities
        rand = random.random()
        if rand < 0.99:
            init = UNBURNED_INIT
        if rand >= 0.99:
            init = BURNING_INIT
        return init

    def evolve_rule(self, last_cell_state, neighbors_last_states):
        rand = random.random()
        new_cell_state = deepcopy(last_cell_state)
        burning_neighbor_bool = self.__is_neighbor_burning(
            neighbors_last_states)
        # If a cell was burning in the last timestep, it extinguishes
        if last_cell_state == BURNING_INIT:
            new_cell_state[0] = BURNED
        # If there is a burning cell in the neighborhood, then an unburned cell can
        # ignite with probability 0.58
        if last_cell_state[0] == UNBURNED_FUEL and burning_neighbor_bool and rand < 0.58:
            new_cell_state[0] = BURNING_FUEL
        return new_cell_state

    @staticmethod
    def __is_neighbor_burning(neighbors):
        if BURNING_FUEL in [neighbor[0] for neighbor in neighbors]:
            return True
        else:
            return False


def state_to_color(current_state):
    # Mapping states to colors if anyone wants to observe the dynamics graphically
    if current_state[0] == NO_FUEL:
        return 0, 0, 0
    if current_state[0] == UNBURNED_FUEL:
        return 200, 150, 100
    if current_state[0] == BURNING_FUEL:
        return 255, 0, 0
    if current_state[0] == BURNED:
        return 0, 0, 0


if __name__ == "__main__":
    CAWindow(cellular_automaton=wildfireCA(),
             window_size=(1000, 830),
             state_to_color_cb=state_to_color).run(evolutions_per_second=1)
