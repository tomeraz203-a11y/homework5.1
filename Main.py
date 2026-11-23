from About1 import Aboutwindow
from GraphWindow import GraphWindow
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QAbstractSpinBox,
    QApplication,
    QDoubleSpinBox,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)


class HeatTransfer(QWidget):
    def __init__(self):
        super().__init__()
        self.about_window = Aboutwindow()
        self.graph_window = GraphWindow(self)
        self.setupUI()
        self.about_button.clicked.connect(self.open_about_window)
        self.graphs_button.clicked.connect(self.open_graph_window)

    def open_about_window(self):
        self.about_window.show()

    def open_graph_window(self):
        self.graph_window.show()

    def setupUI(self):
        self.setWindowTitle("Heat Transfer")

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(24)

        top_layout = QHBoxLayout()
        top_layout.setSpacing(0)

        self.left_slider = QSlider(Qt.Vertical)
        self.left_slider.setRange(0, 200)
        self.left_slider.setValue(200)
        self.left_slider.setFixedHeight(220)
        top_layout.addWidget(self.left_slider)
        top_layout.addSpacing(12)

        self.left_body_widget = QFrame()
        self.left_body_widget.setFixedSize(70, 220)
        self.left_body_widget.setStyleSheet("background-color: #ff0000;")
        top_layout.addWidget(self.left_body_widget)

        center_layout = QVBoxLayout()
        center_layout.setSpacing(6)

        conductivity_label = QLabel("Conductivity")
        conductivity_label.setAlignment(Qt.AlignCenter)
        center_layout.addWidget(conductivity_label)

        self.conductivity_spinbox = QDoubleSpinBox()
        self.conductivity_spinbox.setDecimals(2)
        self.conductivity_spinbox.setRange(0.01, 1000.0)
        self.conductivity_spinbox.setValue(1.00)
        self.conductivity_spinbox.setSuffix(" J/s°C")
        center_layout.addWidget(self.conductivity_spinbox)

        center_layout.addStretch()

        connector_bar = QFrame()
        connector_bar.setFixedHeight(8)
        connector_bar.setStyleSheet("background-color: #808080;")
        center_layout.addWidget(connector_bar)
        center_layout.addStretch()

        center_widget = QWidget()
        center_widget.setFixedHeight(220)
        center_widget.setMinimumWidth(220)
        center_widget.setLayout(center_layout)
        top_layout.addWidget(center_widget)

        self.right_body_widget = QFrame()
        self.right_body_widget.setFixedSize(70, 220)
        self.right_body_widget.setStyleSheet("background-color: #000000;")
        top_layout.addWidget(self.right_body_widget)
        top_layout.addSpacing(12)

        self.right_slider = QSlider(Qt.Vertical)
        self.right_slider.setRange(0, 200)
        self.right_slider.setValue(0)
        self.right_slider.setFixedHeight(220)
        top_layout.addWidget(self.right_slider)

        main_layout.addLayout(top_layout)

        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(24)

        left_column = QGridLayout()
        left_column.setHorizontalSpacing(8)
        left_column.setVerticalSpacing(10)

        self.left_temp_spinbox = self._create_temperature_spinbox(200.0)
        self.left_mass_spinbox = self._create_parameter_spinbox(
            2, 0.01, 10000.0, 10.00, " kg"
        )
        self.left_hcap_spinbox = self._create_parameter_spinbox(
            2, 0.01, 10000.0, 0.40, " J/kg°C"
        )
        self._add_labeled_field(left_column, 0, "Temp.", self.left_temp_spinbox)
        self._add_labeled_field(left_column, 1, "Mass", self.left_mass_spinbox)
        self._add_labeled_field(left_column, 2, "H. Cap.", self.left_hcap_spinbox)
        bottom_layout.addLayout(left_column, 1)

        button_column = QVBoxLayout()
        button_column.setSpacing(10)

        self.start_stop_button = QPushButton("Start")
        self.start_stop_button.setCheckable(True)
        button_column.addWidget(self.start_stop_button)

        self.graphs_button = QPushButton("Graphs")
        button_column.addWidget(self.graphs_button)

        self.about_button = QPushButton("About")
        button_column.addWidget(self.about_button)

        bottom_layout.addLayout(button_column)

        right_column = QGridLayout()
        right_column.setHorizontalSpacing(8)
        right_column.setVerticalSpacing(10)

        self.right_temp_spinbox = self._create_temperature_spinbox(0.0)
        self.right_mass_spinbox = self._create_parameter_spinbox(
            2, 0.01, 10000.0, 10.00, " kg"
        )
        self.right_hcap_spinbox = self._create_parameter_spinbox(
            2, 0.01, 10000.0, 0.40, " J/kg°C"
        )
        self._add_labeled_field(
            right_column, 0, "Temp.", self.right_temp_spinbox, label_on_right=True
        )
        self._add_labeled_field(
            right_column, 1, "Mass", self.right_mass_spinbox, label_on_right=True
        )
        self._add_labeled_field(
            right_column, 2, "H. Cap.", self.right_hcap_spinbox, label_on_right=True
        )
        bottom_layout.addLayout(right_column, 1)

        main_layout.addLayout(bottom_layout)

    @staticmethod
    def _create_temperature_spinbox(value):
        spinbox = QDoubleSpinBox()
        spinbox.setDecimals(1)
        spinbox.setRange(0.0, 200.0)
        spinbox.setValue(value)
        spinbox.setSuffix(" °C")
        spinbox.setReadOnly(True)
        spinbox.setButtonSymbols(QAbstractSpinBox.NoButtons)
        spinbox.setStyleSheet("background-color: #eeeeee;")
        return spinbox

    @staticmethod
    def _create_parameter_spinbox(decimals, minimum, maximum, value, suffix):
        spinbox = QDoubleSpinBox()
        spinbox.setDecimals(decimals)
        spinbox.setRange(minimum, maximum)
        spinbox.setValue(value)
        spinbox.setSuffix(suffix)
        return spinbox

    @staticmethod
    def _add_labeled_field(layout, row, label_text, spinbox, label_on_right=False):
        label = QLabel(label_text)
        if label_on_right:
            layout.addWidget(spinbox, row, 0)
            layout.addWidget(label, row, 1)
        else:
            layout.addWidget(label, row, 0)
            layout.addWidget(spinbox, row, 1)


if __name__ == "__main__":
    app = QApplication([])
    window = HeatTransfer()
    window.show()
    app.exec()
