import numpy as np
import gym
from gym import spaces, logger, error, utils
from gym.utils import seeding
import random
import time
from gym_wildfire.cellular_automata.wildfire_ca import wildfireCA
from tkinter import *

NO_FUEL = [0]
UNBURNED_FUEL = [80]
BURNING_FUEL = [160]
BURNT = [240]

CMAP = {NO_FUEL[0]: "white", UNBURNED_FUEL[0]: "tan",
    BURNING_FUEL[0]: "red", BURNT[0]: "black"}


class EnvWildfireCA(gym.Env):

    metadata = {"render.modes": ['human']}

    def __init__(self, display=False, dimension=36):
        self.dimension = dimension
        self.factor=20
        self.display_width = self.factor * self.dimension
        self.observation_space = spaces.Box(low=0, high=255, shape=(self.dimension, self.dimension, 1), dtype=np.uint8)
        self.action_space = spaces.MultiDiscrete([36 for i in range(16)])
        self.wildfire_ca = wildfireCA()
        self.time = 0
        self.display = display
        self.done = False
        # NEED TO FIX DIMENSION OF CANVAS HERE AND IN RENDER
        if self.display:
            self.tk = Tk()
            self.canvas = Canvas(self.tk, bg='white', width=(self.display_width), height=(self.display_width), 
                                 borderwidth=0, highlightthickness=0)
            self.canvas.pack()
            self.canvas_rect = {}
            self.render()

    def step(self, action):
        assert action in self.action_space
        position_list = [(action[i], action[i+1]) for i in range(0, len(action), 2)]
        self.time += 1
        self.state = []
        self.reward = 0
        # Recording the state and reward; altering the env acc to the action
        for cell in self.wildfire_ca._current_state:
            if cell in position_list and self.wildfire_ca._current_state[cell].state != NO_FUEL:
                self.wildfire_ca._current_state[cell].state = BURNT
            if self.wildfire_ca._current_state[cell].state == BURNING_FUEL:
                self.reward -= 1
        # Keeping track of the time
        if self.time == 100 or self.reward == 0:
            self.done = True
        # Taking the next time step
        self.wildfire_ca.evolve()
        for cell in self.wildfire_ca._current_state:
            self.state.append(self.wildfire_ca._current_state[cell].state)
        if self.display:
            self.render()
        return np.array(self.state).reshape(self.dimension, self.dimension, 1), self.reward, self.done, {}

    def reset(self):
        self.wildfire_ca = wildfireCA()
        self.time = 0
        self.done = False
        if self.display:
            self.render()
        self.state = []
        for cell in self.wildfire_ca._current_state:
            self.state.append(self.wildfire_ca._current_state[cell].state)
        return np.array(self.state).reshape(self.dimension, self.dimension, 1)

    def render(self):
        for column in range(self.dimension):
            for row in range(self.dimension):
                x1 = column * self.factor
                y1 = row * self.factor
                x2 = x1 + self.factor
                y2 = y1 + self.factor
                color = CMAP[self.wildfire_ca._current_state[(column, row)].state[0]]
                self.canvas_rect[row, column] = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)
        self.tk.update()
        time.sleep(1)


    def close(self):
        pass
