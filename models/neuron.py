class IzhikevichNeuron:
    def __init__(self, a: float = 0.02, b: float = 0.2, c: float = -65.0, d: float = 8.0) -> None:
        self.a: float = a
        self.b: float = b
        self.c: float = c
        self.d: float = d
        self.v: float = -65.0
        self.u: float = self.b * self.v
        self.spike_threshold: float = 30.0

    def step(self, input_current: float, dt: float = 0.5) -> tuple[float, float, bool]:
        dv: float = (0.04 * self.v**2 + 5 * self.v + 140 - self.u + input_current) * dt
        du: float = self.a * (self.b * self.v - self.u) * dt

        self.v += dv
        self.u += du

        spike: bool = False
        if self.v >= self.spike_threshold:
            self.v = self.c
            self.u += self.d
            spike = True

        return self.v, self.u, spike

    def reset(self) -> None:
        self.v = -65.0
        self.u = self.b * self.v
