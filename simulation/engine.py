from collections import deque

import numpy as np

from models.neuron import IzhikevichNeuron


class SimulationEngine:
    def __init__(self, neuron: IzhikevichNeuron, dt: float = 0.5, history_size: int = 2000) -> None:
        self.neuron = neuron
        self.dt = dt
        self.history_size = history_size
        self.time = deque(maxlen=history_size)
        self.voltage = deque(maxlen=history_size)
        self.recovery = deque(maxlen=history_size)
        self.current_time = 0.0

    def update(self, input_current: float) -> bool:
        v, u, spike = self.neuron.step(input_current, self.dt)

        self.time.append(self.current_time)
        self.voltage.append(v)
        self.recovery.append(u)

        self.current_time += self.dt

        return spike

    def reset(self) -> None:
        self.neuron.reset()
        self.time.clear()
        self.voltage.clear()
        self.recovery.clear()
        self.current_time = 0.0

    def get_time_array(self) -> np.ndarray:
        return np.array(self.time)

    def get_voltage_array(self) -> np.ndarray:
        return np.array(self.voltage)

    def get_recovery_array(self) -> np.ndarray:
        return np.array(self.recovery)
