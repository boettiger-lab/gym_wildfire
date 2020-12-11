import math

def calc_pw(theta):
    c_1 = 0.045
    c_2 = 0.131
    V = 100
    t = math.radians(theta)
    ft = math.exp(V*c_2*(math.cos(t)-1))
    return math.exp(c_1*V)*ft


def get_wind():

    wind_matrix = [[0 for col in [0,1,2]] for row in [0,1,2]]
    thetas = [[45,0,45],
              [90,0,90],
              [135,180,135]]
    for row in [0,1,2]:
        for col in [0,1,2]:
            wind_matrix[row][col] = calc_pw(thetas[row][col])
    wind_matrix[1][1] = 0
    return wind_matrix
