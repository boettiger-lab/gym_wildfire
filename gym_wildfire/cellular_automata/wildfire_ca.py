import random
import sys
import os

from cellular_automaton import CellularAutomaton, MooreNeighborhood, CAWindow, EdgeRule

# Defining the numerical values describing the states of each cell
NO_FUEL = [0]
UNBURNED_FUEL = [80]
BURNING_FUEL = [160]
BURNT = [240]


class wildfireCA(CellularAutomaton):
    def __init__(self):
        super().__init__(dimension=[36, 36],
                         neighborhood=MooreNeighborhood(EdgeRule.IGNORE_MISSING_NEIGHBORS_OF_EDGE_CELLS))

    def init_cell_state(self, __):
        # Initializing the grid with the following probabilities
        rand = random.random()
        if rand < 0.75:
            init = UNBURNED_FUEL[0]
        if rand < 0.999 and rand >= 0.75:
            init = NO_FUEL[0]
        if rand >= 0.999:
            init = BURNING_FUEL[0]
        return [init]

    def evolve_rule(self, last_cell_state, neighbors_last_states):
        rand = random.random()
        new_cell_state = last_cell_state
        burning_neighbor_bool = self.__is_neighbor_burning(
            neighbors_last_states)
        # If there is a burning cell in the neighborhood, then an unburned cell can
        # ignite with probability 0.58
        if last_cell_state == UNBURNED_FUEL and burning_neighbor_bool and rand < 0.58:
            new_cell_state = BURNING_FUEL
        # If a cell was burning in the last timestep, it extinguishes
        if last_cell_state == BURNING_FUEL:
            new_cell_state = BURNT
        return new_cell_state

    @staticmethod
    def __is_neighbor_burning(neighbors):
        if BURNING_FUEL in neighbors:
            return True
        else:
            return False


def state_to_color(current_state):
    # Mapping states to colors if anyone wants to observe the dynamics graphically
    if current_state == NO_FUEL:
        return 0
    if current_state == UNBURNED_FUEL:
        return 200
    if current_state == BURNING_FUEL:
        return 400
    if current_state == BURNT:
        return 600


if __name__ == "__main__":
    CAWindow(cellular_automaton=wildfireCA(),
             window_size=(1000, 830),
             state_to_color_cb=state_to_color).run(evolutions_per_second=1)
