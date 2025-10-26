import pyqtgraph as pg
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (
    QButtonGroup,
    QGroupBox,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QRadioButton,
    QVBoxLayout,
    QWidget,
)

from models.neuron import IzhikevichNeuron
from models.presets import NeuronPresets
from simulation.engine import SimulationEngine
from ui.parameter_panel import ParameterPanel


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Izhikevich Neuron Model Simulator")
        self.setGeometry(100, 100, 1400, 800)

        self.neuron = IzhikevichNeuron()
        self.simulation = SimulationEngine(self.neuron)
        self.is_running = False

        self.param_spinboxes = {}

        self.setup_ui()
        self.setup_timer()

    def setup_ui(self) -> None:
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        graph_layout = QVBoxLayout()

        self.voltage_plot = pg.PlotWidget(title="Membrane Potential (v)")
        self.voltage_plot.setLabel("left", "v (mV)")
        self.voltage_plot.setLabel("bottom", "Time (ms)")
        self.voltage_plot.setYRange(-100, 60)
        self.voltage_plot.showGrid(x=True, y=True)
        self.voltage_plot.addLegend()
        self.voltage_curve = self.voltage_plot.plot(pen=pg.mkPen("cyan", width=2), name="Voltage (v)")

        self.recovery_plot = pg.PlotWidget(title="Recovery Variable (u)")
        self.recovery_plot.setLabel("left", "u")
        self.recovery_plot.setLabel("bottom", "Time (ms)")
        self.recovery_plot.setYRange(-20, 20)
        self.recovery_plot.showGrid(x=True, y=True)
        self.recovery_plot.addLegend()
        self.recovery_curve = self.recovery_plot.plot(pen=pg.mkPen("yellow", width=2), name="Recovery (u)")

        graph_layout.addWidget(self.voltage_plot)
        graph_layout.addWidget(self.recovery_plot)

        control_layout = QVBoxLayout()

        self.model_params = ParameterPanel("Model Parameters")
        params = [
            ("a", "a", 0.02, 0.001, 0.5, 0.001),
            ("b", "b", 0.2, 0.0, 1.0, 0.01),
            ("c", "c", -65.0, -80.0, -40.0, 1.0, 1),
            ("d", "d", 8.0, 0.0, 20.0, 0.5, 1),
        ]
        for name, label, value, min_v, max_v, step, *decimals in params:
            decimals = decimals[0] if decimals else 3
            spinbox = self.model_params.add_parameter(name, label, value, min_v, max_v, step, decimals)
            spinbox.valueChanged.connect(self.on_param_changed)
            self.param_spinboxes[name] = spinbox
        control_layout.addWidget(self.model_params)

        self.input_params = ParameterPanel("Input Current")
        self.param_spinboxes["I"] = self.input_params.add_parameter("I", "I (pA)", 10.0, -50.0, 50.0, 1.0, 1)
        self.param_spinboxes["I"].valueChanged.connect(self.on_param_changed)
        control_layout.addWidget(self.input_params)

        self.presets_group = QGroupBox("Neuron Type Presets")
        presets_layout = QVBoxLayout()
        self.preset_buttons = QButtonGroup()
        presets = [
            ("Regular Spiking", NeuronPresets.REGULAR_SPIKING.parameters()),
            ("Fast Spiking", NeuronPresets.FAST_SPIKING.parameters()),
            ("Intrinsically Bursting", NeuronPresets.INTRINSICALLY_BURSTING.parameters()),
            ("Chattering", NeuronPresets.CHATTERING.parameters()),
            ("Low-Threshold Spiking", NeuronPresets.LOW_THRESHOLD.parameters()),
        ]
        for index, (name, preset) in enumerate(presets):
            radio_btn = QRadioButton(name)
            self.preset_buttons.addButton(radio_btn, id=index)
            presets_layout.addWidget(radio_btn)
            radio_btn.toggled.connect(lambda checked, p=preset: checked and self.load_preset(p))

        first_button = self.preset_buttons.button(0)
        if first_button:
            first_button.setChecked(True)
        self.presets_group.setLayout(presets_layout)
        control_layout.addWidget(self.presets_group)

        self.control_buttons = QGroupBox("Simulation Control")
        buttons_layout = QVBoxLayout()

        self.start_btn = QPushButton("Start")
        self.start_btn.clicked.connect(self.toggle_simulation)
        buttons_layout.addWidget(self.start_btn)

        self.reset_btn = QPushButton("Reset")
        self.reset_btn.clicked.connect(self.reset_simulation)
        buttons_layout.addWidget(self.reset_btn)

        self.quit_btn = QPushButton("Exit")
        self.quit_btn.clicked.connect(self.close)
        buttons_layout.addWidget(self.quit_btn)

        self.control_buttons.setLayout(buttons_layout)
        control_layout.addWidget(self.control_buttons)

        control_layout.addStretch()

        main_layout.addLayout(graph_layout, 3)
        main_layout.addLayout(control_layout, 1)

    def on_param_changed(self):
        if not self.is_running:
            self.apply_parameters()

    def setup_timer(self) -> None:
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_simulation)
        self.timer.setInterval(50)

    def toggle_simulation(self) -> None:
        if self.is_running:
            self.timer.stop()
            self.start_btn.setText("Start")
            self.is_running = False
            self.set_controls_enabled(True)
        else:
            self.timer.start()
            self.start_btn.setText("Stop")
            self.is_running = True
            self.set_controls_enabled(False)

    def set_controls_enabled(self, enabled: bool) -> None:
        for spinbox in self.param_spinboxes.values():
            spinbox.setEnabled(enabled)
        for btn in self.preset_buttons.buttons():
            btn.setEnabled(enabled)

    def update_simulation(self) -> None:
        input_current = self.param_spinboxes["I"].value()
        self.simulation.update(input_current)

        max_points = 1000
        time_arr = self.simulation.get_time_array()[-max_points:]
        voltage_arr = self.simulation.get_voltage_array()[-max_points:]
        recovery_arr = self.simulation.get_recovery_array()[-max_points:]

        self.voltage_curve.setData(time_arr, voltage_arr)
        self.recovery_curve.setData(time_arr, recovery_arr)

        if len(time_arr) > 0:
            max_time = time_arr[-1]
            x_min = max(0, max_time - 1500)
            self.voltage_plot.setXRange(x_min, max_time)
            self.recovery_plot.setXRange(x_min, max_time)

    def apply_parameters(self) -> None:
        for param in ("a", "b", "c", "d"):
            setattr(self.neuron, param, self.param_spinboxes[param].value())

    def reset_simulation(self) -> None:
        was_running = self.is_running
        if was_running:
            self.toggle_simulation()
        self.simulation.reset()
        self.voltage_curve.setData([], [])
        self.recovery_curve.setData([], [])
        if was_running:
            self.toggle_simulation()

    def load_preset(self, preset: dict[str, float]) -> None:
        for param in ("a", "b", "c", "d"):
            self.param_spinboxes[param].setValue(preset[param])
        self.apply_parameters()
