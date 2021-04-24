import math


def calc_pw(theta, wind_velocity):
    c_1 = 0.045
    c_2 = 0.131
    V = wind_velocity
    t = math.radians(theta)
    ft = math.exp(V * c_2 * (math.cos(t) - 1))
    return math.exp(c_1 * V) * ft


def get_wind(thetas, wind_velocity):

    wind_matrix = [[0 for col in [0, 1, 2]] for row in [0, 1, 2]]
    thetas = thetas  # [[45,0,45],
    # [90,0,90],
    # [135,180,135]]
    for row in [0, 1, 2]:
        for col in [0, 1, 2]:
            wind_matrix[row][col] = calc_pw(thetas[row][col], wind_velocity)
    wind_matrix[1][1] = 0
    return wind_matrix


def tg(x):
    return math.degrees(math.atan(x))


def get_slope(wildfire_ca):
    slope_matrix = [
        [0 for col in range(wildfire_ca.n_col)]
        for row in range(wildfire_ca.n_row)
    ]
    for row in range(wildfire_ca.n_row):
        for col in range(wildfire_ca.n_col):
            sub_slope_matrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
            if (
                row == 0
                or row == wildfire_ca.n_row - 1
                or col == 0
                or col == wildfire_ca.n_col - 1
            ):  # margin is flat
                slope_matrix[row][col] = sub_slope_matrix
                continue
            current_altitude = wildfire_ca._current_state[(row, col)].state[3]
            sub_slope_matrix[0][0] = tg(
                (
                    current_altitude
                    - wildfire_ca._current_state[(row - 1, col - 1)].state[3]
                )
                / 1.414
            )
            sub_slope_matrix[0][1] = tg(
                current_altitude
                - wildfire_ca._current_state[(row - 1, col)].state[3]
            )
            sub_slope_matrix[0][2] = tg(
                (
                    current_altitude
                    - wildfire_ca._current_state[(row - 1, col + 1)].state[3]
                )
                / 1.414
            )
            sub_slope_matrix[1][0] = tg(
                current_altitude
                - wildfire_ca._current_state[(row, col - 1)].state[3]
            )
            sub_slope_matrix[1][1] = 0
            sub_slope_matrix[1][2] = tg(
                current_altitude
                - wildfire_ca._current_state[(row, col + 1)].state[3]
            )
            sub_slope_matrix[2][0] = tg(
                (
                    current_altitude
                    - wildfire_ca._current_state[(row + 1, col - 1)].state[3]
                )
                / 1.414
            )
            sub_slope_matrix[2][1] = tg(
                current_altitude
                - wildfire_ca._current_state[(row + 1, col)].state[3]
            )
            sub_slope_matrix[2][2] = tg(
                (
                    current_altitude
                    - wildfire_ca._current_state[(row + 1, col + 1)].state[3]
                )
                / 1.414
            )
            slope_matrix[row][col] = sub_slope_matrix
    return slope_matrix
