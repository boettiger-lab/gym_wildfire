import numpy as np
import gym
from gym import spaces, logger, error, utils
from gym.utils import seeding
import random
from pandas import DataFrame
import time
from gym_wildfire.cellular_automata.realistic.wildfire_ca import wildfireCA
from tkinter import *

NO_FUEL = 0
UNBURNED_FUEL = 40
BURNING_FUEL = 80
BURNED = 120
PREVENTATIVE_BURNED = 160

# CMAP is a color map used in GUI display
CMAP = {NO_FUEL: "white", UNBURNED_FUEL: "tan",
    BURNING_FUEL: "red", BURNED: "black", PREVENTATIVE_BURNED:"blue"}


class EnvWildfireCA(gym.Env):

    metadata = {"render.modes": ['human']}

    def __init__(self, display=False, dimension=36):
        self.dimension = dimension
        self.factor=20 # This determines how big a cell will appear graphically
        self.display_width = self.factor * self.dimension
        self.observation_space = spaces.Box(low=0, high=255, shape=(self.dimension, self.dimension, 1), dtype=np.uint8)
        self.action_space = spaces.MultiDiscrete([36 for i in range(2)]) # An agent can select 2 cells for preventative burns
        self.wildfire_ca = wildfireCA()
        self.lag = 8 # How many time steps do you allow agent to have before evolving model
        self.time = 0
        self.Tmax = 800
        self.sleep = 0.5
        self.display = display
        self.debug_flag = False
        self.done = False
        if self.display:
            self.tk = Tk()
            self.canvas = Canvas(self.tk, bg='white', width=(self.display_width), height=(self.display_width),
                                 borderwidth=0, highlightthickness=0)
            self.canvas.pack()
            self.canvas_rect = {}
            self.render()

    def step(self, action):
        action = list(action)
        position_tup = ()
        # I check to make sure that there are no Nones in the action
        # as in my reactive_agent script, I use Nones to denote skipping an action
        if action[0] != None:
            position_tup = (action[0], action[1])
        self.time += 1 # Advance a timestep
        self.state = []
        self.reward = 0
        # Going through every cell in the model
#        for cell in self.wildfire_ca._current_state:
           # Where there is a preventative burn inputted in action, burn the cell
#            if cell == position_tup and self.wildfire_ca._current_state[cell].state[0] == UNBURNED_FUEL:
#                self.wildfire_ca._current_state[cell].state[0] = PREVENTATIVE_BURNED
            # Penalize the agent based on how many actively burning cells there are
#            if self.wildfire_ca._current_state[cell].state[0] == BURNING_FUEL:
#                self.reward -= 1
        
        if self.time == self.Tmax or self.reward == 0:
            self.done = True
        # Only evolving every 8 time steps to allow agent to burn 8 cells at a time
        if self.time % self.lag == 0:
            self.wildfire_ca.evolve()
        # Recording the state to report as the observation
        for cell in self.wildfire_ca._current_state:
            self.state.append(self.wildfire_ca._current_state[cell].state)
        if self.display:
            self.render()
        return np.array(self.state).reshape(self.dimension, self.dimension, 4), self.reward, self.done, {}

    def reset(self):
        self.wildfire_ca = wildfireCA()
        self.time = 0
        self.done = False
        if self.display:
            self.render()
        self.state = []
        # Recording the state to report
        for cell in self.wildfire_ca._current_state:
            self.state.append(self.wildfire_ca._current_state[cell].state)
        return np.array(self.state).reshape(self.dimension, self.dimension, 4)

    def render(self):
        for column in range(self.dimension):
            for row in range(self.dimension):
                x1 = column * self.factor
                y1 = row * self.factor
                x2 = x1 + self.factor
                y2 = y1 + self.factor
                if self.debug_flag:
                    import pdb; pdb.set_trace()
                color = CMAP[self.wildfire_ca._current_state[(column, row)].state[0]]
                self.canvas_rect[row, column] = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)
        self.tk.update()
        time.sleep(self.sleep)

    def simulate(self, model, reps=1):
        row = []
        for rep in range(reps):
            obs = self.reset()
            reward = 0
            for t in range(self.Tmax):
                action, _state = model.predict(obs)
                row.append([t, obs, action, reward, rep])
                obs, reward, done, info = self.step(action)
                if done:
                    break
            row.append([t+1, obs, None, reward, rep])
        df = DataFrame(row, columns=['time', 'state', 'action', 'reward', 'rep'])
        return df

    def close(self):
        pass