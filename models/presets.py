from enum import Enum


class NeuronPresets(Enum):
    REGULAR_SPIKING = {"a": 0.02, "b": 0.2, "c": -65.0, "d": 8.0}
    FAST_SPIKING = {"a": 0.1, "b": 0.2, "c": -65.0, "d": 2.0}
    INTRINSICALLY_BURSTING = {"a": 0.02, "b": 0.2, "c": -55.0, "d": 4.0}
    CHATTERING = {"a": 0.02, "b": 0.2, "c": -50.0, "d": 2.0}
    LOW_THRESHOLD = {"a": 0.02, "b": 0.25, "c": -65.0, "d": 2.0}

    def parameters(self) -> dict[str, float]:
        return self.value
