from gym.envs.registration import register

__version__ = "0.0.0"
entry_point = "gym_wildfire.cellular_automata.alexandridis_et_al:EnvWildfireCA"

register(
    id="wildfireCA-v0",
    entry_point=entry_point,
)
