import math
import random
from copy import deepcopy

from cellular_automaton import CellularAutomaton, EdgeRule, MooreNeighborhood

from gym_wildfire.cellular_automata.alexandridis_et_al.utils import (
    get_slope,
    get_wind,
)

# Format for a cellular automata state is:
#        [fuel state, vegetation, density, altitude, (x, y)]
# Fuel State: 0 - no fuel, 40 - unburned fuel,
#             80 - burning fuel, 120 - burned fuel, 160 - preventative burn
# Vegetation: 40 - agricultural, 80 - thickets, 120 - hallepo-pine
# Density: 40 - low density, 80 normal density, 120 - high density
# Altitude:

NO_FUEL = 0
UNBURNED_FUEL = 40
BURNING_FUEL = 80
BURNED = 120
PREVENTATIVE_BURN = 160
UNBURNED_INIT = [40, 80, 80, 0]
BURNING_INIT = [80, 80, 80, 0]

thetas = [[45, 0, 45], [90, 0, 90], [135, 180, 135]]
wind_velocity = 0


class wildfireCA(CellularAutomaton):
    def __init__(self, thetas, wind_velocity, n_row=36, n_col=36):
        super().__init__(
            dimension=[n_row, n_col],
            neighborhood=MooreNeighborhood(
                EdgeRule.IGNORE_MISSING_NEIGHBORS_OF_EDGE_CELLS
            ),
        )
        self.n_row = n_row
        self.n_col = n_col
        self.add_position_index()
        self.wind_matrix = get_wind(thetas, wind_velocity)
        self.slope_matrix = get_slope(self)

    def init_cell_state(self, __):
        # Initializing the grid with the following probabilities
        rand = random.random()
        if rand < 0.998:
            init = UNBURNED_INIT
        if rand >= 0.998:
            init = BURNING_INIT
        return init

    def add_position_index(self):
        for cell in self._current_state:
            # For whatever reason using `append` or += would add
            # cell to every state; this is only fix I can find to
            # remedy this issue -- don't know why this is
            self._current_state[cell].state = self._current_state[
                cell
            ].state + [cell]
            self._current_state[cell].state[3] = cell[1] ** 4

    def evolve_rule(self, last_cell_state, neighbors_last_states):
        new_cell_state = deepcopy(last_cell_state)
        # If a cell was burning in the last timestep, it extinguishes
        if last_cell_state[0] == BURNING_FUEL:
            new_cell_state[0] = BURNED
        # If there is a burning cell in the neighborhood,
        # then an unburned cell can ignite with probability 0.58
        if last_cell_state[0] == UNBURNED_FUEL:
            p_h = 0.58
            a = 0.078
            p_veg = {40: -0.3, 80: 0.3, 120: 0.4}[last_cell_state[1]]
            p_den = {40: -0.3, 80: 0.3, 120: 0.3}[last_cell_state[2]]
            for neighbor in neighbors_last_states:
                if neighbor[0] == BURNING_FUEL:
                    x_loc = 1 + neighbor[-1][0] - last_cell_state[-1][0]
                    y_loc = 1 + neighbor[-1][1] - last_cell_state[-1][1]
                    x_abs = last_cell_state[-1][0]
                    y_abs = last_cell_state[-1][1]
                    slope = self.slope_matrix[y_abs][x_abs][y_loc][x_loc]
                    p_wind = self.wind_matrix[y_loc][x_loc]
                    p_burn = p_h * (1 + p_veg) * (1 + p_den) * p_wind
                    p_slope = math.exp(a * slope)
                    p_burn *= p_slope
                    if random.random() < p_burn:
                        new_cell_state[0] = BURNING_FUEL
                        break
        return new_cell_state

    @staticmethod
    def get_burning_neighbors(neighbors):
        burning_neighbors = []
        for neighbor in neighbors:
            if neighbor[0] == BURNING_FUEL:
                burning_neighbors.append(neighbor)
        return burning_neighbors


def state_to_color(current_state):
    # Mapping states to colors if anyone wants to observe
    # the dynamics graphically
    if current_state[0] == NO_FUEL:
        return 0, 0, 0
    if current_state[0] == UNBURNED_FUEL:
        return 200, 150, 100
    if current_state[0] == BURNING_FUEL:
        return 255, 0, 0
    if current_state[0] == BURNED:
        return 0, 0, 0


# if __name__ == "__main__":
#    CAWindow(
#        cellular_automaton=wildfireCA(thetas, wind_velocity),
#        window_size=(1000, 830),
#        state_to_color_cb=state_to_color,
#    ).run(evolutions_per_second=1)
