import numpy as np

from models.neuron import IzhikevichNeuron


class SimulationEngine:
    def __init__(self, neuron: IzhikevichNeuron, dt: float = 0.5, history_size: int = 2000) -> None:
        self.neuron = neuron
        self.dt = dt
        self.history_size = history_size

        self.time = np.zeros(history_size, dtype=np.float64)
        self.voltage = np.zeros(history_size, dtype=np.float64)
        self.recovery = np.zeros(history_size, dtype=np.float64)

        self.current_time = 0.0
        self.index = 0
        self.filled = False

    def update(self, input_current: float) -> bool:
        v, u, spike = self.neuron.step(input_current, self.dt)

        idx = self.index % self.history_size
        self.time[idx] = self.current_time
        self.voltage[idx] = v
        self.recovery[idx] = u

        self.index += 1
        if self.index >= self.history_size:
            self.filled = True

        self.current_time += self.dt
        return spike

    def get_time_array(self) -> np.ndarray:
        if not self.filled:
            return self.time[: self.index]
        idx = self.index % self.history_size
        return np.concatenate([self.time[idx:], self.time[:idx]])

    def get_voltage_array(self) -> np.ndarray:
        if not self.filled:
            return self.voltage[: self.index]
        idx = self.index % self.history_size
        return np.concatenate([self.voltage[idx:], self.voltage[:idx]])

    def get_recovery_array(self) -> np.ndarray:
        if not self.filled:
            return self.recovery[: self.index]
        idx = self.index % self.history_size
        return np.concatenate([self.recovery[idx:], self.recovery[:idx]])

    def reset(self) -> None:
        self.neuron.reset()
        self.time.fill(0.0)
        self.voltage.fill(0.0)
        self.recovery.fill(0.0)
        self.current_time = 0.0
        self.index = 0
        self.filled = False
