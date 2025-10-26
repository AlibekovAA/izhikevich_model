from PyQt6.QtWidgets import QDoubleSpinBox, QGroupBox, QHBoxLayout, QLabel, QVBoxLayout


class ParameterPanel(QGroupBox):
    def __init__(self, title: str) -> None:
        super().__init__(title)
        self._layout: QVBoxLayout = QVBoxLayout()
        self.setLayout(self._layout)
        self.spinboxes: dict[str, QDoubleSpinBox] = {}

    def add_parameter(
        self,
        name: str,
        label: str,
        value: float,
        min_val: float,
        max_val: float,
        step: float,
        decimals: int = 3,
    ) -> QDoubleSpinBox:
        row: QHBoxLayout = QHBoxLayout()
        label_widget: QLabel = QLabel(f"{label}:")
        label_widget.setMinimumWidth(80)

        spinbox: QDoubleSpinBox = QDoubleSpinBox()
        spinbox.setMinimum(min_val)
        spinbox.setMaximum(max_val)
        spinbox.setSingleStep(step)
        spinbox.setDecimals(decimals)
        spinbox.setValue(value)

        row.addWidget(label_widget)
        row.addWidget(spinbox)
        self._layout.addLayout(row)

        self.spinboxes[name] = spinbox
        return spinbox

    def get_value(self, name: str) -> float:
        return self.spinboxes[name].value()
