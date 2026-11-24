from About1 import Aboutwindow
from Body import Body
from GraphWindow import GraphWindow
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QAbstractSpinBox,
    QApplication,
    QCheckBox,
    QComboBox,
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

        self.body1 = None
        self.body2 = None
        self.dt = 0.1
        self.current_time = 0.0
        self.time_history = []
        self.body1_temp_history = []
        self.body2_temp_history = []

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timer_method)

        self.setupUI()

        self.left_slider.valueChanged.connect(self.left_temperature_changed)
        self.right_slider.valueChanged.connect(self.right_temperature_changed)
        self.start_stop_button.clicked.connect(self.start_stop_button_method)
        self.about_button.clicked.connect(self.open_about_window)
        self.graphs_button.clicked.connect(self.open_graph_window)
        self.left_material_combo.currentTextChanged.connect(self.left_material_changed)    
        self.right_material_combo.currentTextChanged.connect(self.right_material_changed) 

    def open_about_window(self):
        self.about_window.show()

    def open_graph_window(self):
        self.graph_window.show()

    def left_temperature_changed(self):
        temp = float(self.left_slider.value())
        self.left_temp_spinbox.setValue(temp)
        self.update_body_color(self.left_body_widget, temp)

    def right_temperature_changed(self):
        temp = float(self.right_slider.value())
        self.right_temp_spinbox.setValue(temp)
        self.update_body_color(self.right_body_widget, temp)

    def left_material_changed(self):
        materials = {
            "Copper": 0.39,
            "Iron": 0.45,
            "Aluminum": 0.90,
            "Water": 4.18,
        }
        selected = self.left_material_combo.currentText()
        if selected in materials:
            self.left_hcap_spinbox.setValue(materials[selected])

    def right_material_changed(self):
        materials = {
            "Copper": 0.39,
            "Iron": 0.45,
            "Aluminum": 0.90,
            "Water": 4.18,
        }
        selected = self.right_material_combo.currentText()
        if selected in materials:
            self.right_hcap_spinbox.setValue(materials[selected])

    def update_body_color(self, widget, temperature):
        red_value = int((temperature / 200.0) * 255)
        widget.setStyleSheet(f"background-color: rgb({red_value}, 0, 0);")

    def set_inputs_enabled(self, enabled):
        self.left_slider.setEnabled(enabled)
        self.right_slider.setEnabled(enabled)
        self.left_mass_spinbox.setEnabled(enabled)
        self.right_mass_spinbox.setEnabled(enabled)
        self.left_hcap_spinbox.setEnabled(enabled)
        self.right_hcap_spinbox.setEnabled(enabled)
        self.conductivity_spinbox.setEnabled(enabled)
        self.left_material_combo.setEnabled(enabled)
        self.right_material_combo.setEnabled(enabled)

    def start_stop_button_method(self):
        if self.start_stop_button.isChecked():
            self.start_stop_button.setText("Stop")
            self.set_inputs_enabled(False)

            t1 = self.left_temp_spinbox.value()
            t2 = self.right_temp_spinbox.value()
            m1 = self.left_mass_spinbox.value()
            m2 = self.right_mass_spinbox.value()
            c1 = self.left_hcap_spinbox.value()
            c2 = self.right_hcap_spinbox.value()

            self.body1 = Body(m1, c1, t1)
            self.body2 = Body(m2, c2, t2)

            self.current_time = 0.0
            self.time_history = [self.current_time]
            self.body1_temp_history = [t1]
            self.body2_temp_history = [t2]

            self.timer.start(int(self.dt * 1000))
        else:
            self.timer.stop()
            self.start_stop_button.setText("Start")
            self.set_inputs_enabled(True)

    def timer_method(self):
        conductivity = self.conductivity_spinbox.value()
        t1 = self.body1.temperature
        t2 = self.body2.temperature

        rate1 = conductivity * (t2 - t1)
        rate2 = conductivity * (t1 - t2)

        dq1 = rate1 * self.dt
        dq2 = rate2 * self.dt

        new_t1 = self.body1.add_heat(dq1)
        new_t2 = self.body2.add_heat(dq2)

        self.current_time += self.dt
        self.time_history.append(self.current_time)
        self.body1_temp_history.append(new_t1)
        self.body2_temp_history.append(new_t2)

        self.left_temp_spinbox.setValue(new_t1)
        self.right_temp_spinbox.setValue(new_t2)

        self.left_slider.blockSignals(True)
        self.left_slider.setValue(int(round(new_t1)))
        self.left_slider.blockSignals(False)

        self.right_slider.blockSignals(True)
        self.right_slider.setValue(int(round(new_t2)))
        self.right_slider.blockSignals(False)

        self.update_body_color(self.left_body_widget, new_t1)
        self.update_body_color(self.right_body_widget, new_t2)
       
        if self.auto_stop_checkbox.isChecked() and abs(new_t1 - new_t2) < 0.05:
            self.start_stop_button.setChecked(False)
            self.start_stop_button_method()

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
        self.left_body_widget.setStyleSheet("background-color: rgb(255, 0, 0);")
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
        self.right_body_widget.setStyleSheet("background-color: rgb(0, 0, 0);")
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

        self.left_temp_spinbox = self.create_temperature_spinbox(200.0)
        self.left_mass_spinbox = self.create_parameter_spinbox(
            2, 0.01, 10000.0, 10.00, " kg"
        )
        self.left_hcap_spinbox = self.create_parameter_spinbox(
            2, 0.01, 10000.0, 0.40, " J/kg°C"
        )
        self.add_labeled_field(left_column, 0, "Temp.", self.left_temp_spinbox)
        self.add_labeled_field(left_column, 1, "Mass", self.left_mass_spinbox)
        self.add_labeled_field(left_column, 2, "H. Cap.", self.left_hcap_spinbox)
        self.left_material_combo = QComboBox()
        self.left_material_combo.addItems(["Custom", "Copper", "Iron", "Aluminum", "Water"])
        self.add_labeled_field(left_column, 3, "Material", self.left_material_combo)
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
        self.auto_stop_checkbox = QCheckBox("Auto-stop")
        button_column.addWidget(self.auto_stop_checkbox)

        bottom_layout.addLayout(button_column)

        right_column = QGridLayout()
        right_column.setHorizontalSpacing(8)
        right_column.setVerticalSpacing(10)

        self.right_temp_spinbox = self.create_temperature_spinbox(0.0)
        self.right_mass_spinbox = self.create_parameter_spinbox(
            2, 0.01, 10000.0, 10.00, " kg"
        )
        self.right_hcap_spinbox = self.create_parameter_spinbox(
            2, 0.01, 10000.0, 0.40, " J/kg°C"
        )
        self.add_labeled_field(
            right_column, 0, "Temp.", self.right_temp_spinbox, label_on_right=True
        )
        self.add_labeled_field(
            right_column, 1, "Mass", self.right_mass_spinbox, label_on_right=True
        )
        self.add_labeled_field(
            right_column, 2, "H. Cap.", self.right_hcap_spinbox, label_on_right=True
        )
        self.right_material_combo = QComboBox()
        self.right_material_combo.addItems(["Custom", "Copper", "Iron", "Aluminum", "Water"])
        self.add_labeled_field(
            right_column, 3, "Material", self.right_material_combo, label_on_right=True
        )
        bottom_layout.addLayout(right_column, 1)

        main_layout.addLayout(bottom_layout)

    def create_temperature_spinbox(self, value):
        spinbox = QDoubleSpinBox()
        spinbox.setDecimals(1)
        spinbox.setRange(0.0, 200.0)
        spinbox.setValue(value)
        spinbox.setSuffix(" °C")
        spinbox.setReadOnly(True)
        spinbox.setButtonSymbols(QAbstractSpinBox.NoButtons)
        spinbox.setStyleSheet("background-color: #eeeeee;")
        return spinbox

    def create_parameter_spinbox(self, decimals, minimum, maximum, value, suffix):
        spinbox = QDoubleSpinBox()
        spinbox.setDecimals(decimals)
        spinbox.setRange(minimum, maximum)
        spinbox.setValue(value)
        spinbox.setSuffix(suffix)
        return spinbox

    def add_labeled_field(self, layout, row, label_text, spinbox, label_on_right=False):
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