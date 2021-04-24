import time
from tkinter import Canvas, Tk

import gym
import numpy as np
from gym import spaces
from pandas import DataFrame

from gym_wildfire.cellular_automata.alexandridis_et_al.wildfire_ca import (
    wildfireCA,
)

NO_FUEL = 0
UNBURNED_FUEL = 40
BURNING_FUEL = 80
BURNED = 120
PREVENTATIVE_BURNED = 160

# CMAP is a color map used in GUI display
CMAP = {
    NO_FUEL: "white",
    UNBURNED_FUEL: "tan",
    BURNING_FUEL: "red",
    BURNED: "black",
    PREVENTATIVE_BURNED: "blue",
}


class EnvWildfireCA(gym.Env):

    metadata = {"render.modes": ["human"]}

    def __init__(
        self,
        display=False,
        dimension=36,
        thetas=[[45, 0, 45], [90, 0, 90], [135, 180, 135]],
        wind_velocity=5,
    ):
        self.dimension = dimension
        self.factor = (
            20  # This determines how big a cell will appear graphically
        )
        self.display_width = self.factor * self.dimension
        self.observation_space = spaces.Box(
            low=0,
            high=255,
            shape=(self.dimension, self.dimension, 1),
            dtype=np.uint8,
        )
        # An agent can select 2 cells for preventative burns
        self.action_space = spaces.MultiDiscrete(
            [self.dimension for i in range(2)]
        )
        self.wildfire_ca = wildfireCA(
            thetas=thetas,
            wind_velocity=wind_velocity,
            n_row=dimension,
            n_col=dimension,
        )
        self.thetas = thetas
        self.wind_velocity = wind_velocity
        self.lag = 8  # time steps for agent before evolving model
        self.time = 0
        self.Tmax = 800
        self.sleep = 0.05
        self.display = display
        self.debug_flag = False
        self.done = False
        if self.display:
            self.tk = Tk()
            self.canvas = Canvas(
                self.tk,
                bg="white",
                width=(self.display_width),
                height=(self.display_width),
                borderwidth=0,
                highlightthickness=0,
            )
            self.canvas.pack()
            self.canvas_rect = {}
            self.render()

    def step(self, action):
        action = list(action)
        position_tup = ()
        # I check to make sure that there are no Nones in the action
        # as in my reactive_agent script, I use Nones for skipping an action
        if action[0] is not None:
            position_tup = (action[0], action[1])
        self.time += 1  # Advance a timestep
        self.state = []
        self.reward = 0
        # Going through every cell in the model
        for cell in self.wildfire_ca._current_state:
            # Where there is a prevent. burn inputted, burn the cell
            if (
                cell == position_tup
                and self.wildfire_ca._current_state[cell].state[0]
                == UNBURNED_FUEL
            ):
                self.wildfire_ca._current_state[cell].state[
                    0
                ] = PREVENTATIVE_BURNED
            # Penalize the agent acc. to # of actively burning cells
            if self.wildfire_ca._current_state[cell].state[0] == BURNING_FUEL:
                self.reward -= 1

        if self.time == self.Tmax or self.reward == 0:
            self.done = True
        if self.time % self.lag == 0:
            self.wildfire_ca.evolve()
        # Recording the state to report as the observation
        for cell in self.wildfire_ca._current_state:
            self.state.append(self.wildfire_ca._current_state[cell].state[0])
        if self.display:
            self.render()
        return (
            np.array(self.state).reshape(self.dimension, self.dimension, 1),
            self.reward,
            self.done,
            {},
        )

    def reset(self):
        self.wildfire_ca = wildfireCA(
            thetas=self.thetas,
            wind_velocity=self.wind_velocity,
            n_row=self.dimension,
            n_col=self.dimension,
        )
        self.time = 0
        self.done = False
        if self.display:
            self.render()
        self.state = []
        # Recording the state to report
        for cell in self.wildfire_ca._current_state:
            self.state.append(self.wildfire_ca._current_state[cell].state[0])
        return np.array(self.state).reshape(self.dimension, self.dimension, 1)

    def render(self):
        for column in range(self.dimension):
            for row in range(self.dimension):
                x1 = column * self.factor
                y1 = row * self.factor
                x2 = x1 + self.factor
                y2 = y1 + self.factor
                if self.debug_flag:
                    import pdb

                    pdb.set_trace()
                color = CMAP[
                    self.wildfire_ca._current_state[(column, row)].state[0]
                ]
                self.canvas_rect[row, column] = self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill=color
                )
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
            row.append([t + 1, obs, None, reward, rep])
        df = DataFrame(
            row, columns=["time", "state", "action", "reward", "rep"]
        )
        return df

    def close(self):
        pass
