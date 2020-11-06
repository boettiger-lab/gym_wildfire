import random
import sys
import os

from cellular_automaton import CellularAutomaton, MooreNeighborhood, CAWindow, EdgeRule

NO_FUEL = [0]
UNBURNED_FUEL = [1]
BURNING = [2]
BURNT = [3]

class wildfireCA(CellularAutomaton):
    def __init__(self):
        super().__init__(dimension=[200,200],
                         neighborhood=MooreNeighborhood(EdgeRule.IGNORE_MISSING_NEIGHBORS_OF_EDGE_CELLS))

    def init_cell_state(self, __):
        rand = random.random()
        if rand < 0.75:
            init = 1
        if rand < 0.95 and rand >= 0.75:
            init = 0
        if rand >= 0.95:
            init = 2
        return [init]

    def evolve_rule(self, last_cell_state, neighbors_last_states):
        rand = random.random()
        new_cell_state = last_cell_state
        burning_neighbor_bool = self.__is_neighbor_burning(neighbors_last_states)
        if last_cell_state == UNBURNED_FUEL and burning_neighbor_bool and rand < 0.58:
            new_cell_state = BURNING_FUEL
        if last_cell_state == BURNING_FUEL:
            new_cell_state = BURNT
        return new_cell_state

    @staticmethod
    def __is_neighbor_burning(neighbors):
        if BURNING in neighbors:
            return True
        else:
            return False

if __name__=="__main__":
    CAWindow(cellular_automaton=wildfireCA(),
             window_size=(1000, 830)).run(evolutions_per_second=5)
