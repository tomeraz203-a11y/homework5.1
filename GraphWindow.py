from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PySide6.QtWidgets import QComboBox, QHBoxLayout, QPushButton, QVBoxLayout, QWidget


class GraphWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setupUI()
        self.draw_button.clicked.connect(self.draw_graph)
        self.clear_button.clicked.connect(self.clear_graph)

    def setupUI(self):
        self.setWindowTitle("Graph Window")

        main_layout = QHBoxLayout(self)

        self.figure = Figure()
        self.ax = self.figure.add_subplot(111)
        self.ax.set_ylabel("Temperature (°C)")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_xlim(0.0, 1.0)
        self.ax.set_ylim(0.0, 1.0)

        self.canvas = FigureCanvasQTAgg(self.figure)
        main_layout.addWidget(self.canvas, 1)

        controls_layout = QVBoxLayout()

        self.body_combo = QComboBox()
        self.body_combo.addItems(["Body 1", "Body 2"])
        controls_layout.addWidget(self.body_combo)

        self.draw_button = QPushButton("Draw")
        controls_layout.addWidget(self.draw_button)

        self.clear_button = QPushButton("Clear")
        controls_layout.addWidget(self.clear_button)

        self.export_button = QPushButton("Export to CSV")
        controls_layout.addWidget(self.export_button)

        controls_layout.addStretch()
        main_layout.addLayout(controls_layout)


    def draw_graph(self):
        times = self.main_window.time_history
        if not times:
            return

        selected_body = self.body_combo.currentText()
        if selected_body == "Body 1":
            temps = self.main_window.body1_temp_history
            mass = self.main_window.left_mass_spinbox.value()
            hcap = self.main_window.left_hcap_spinbox.value()
        else:
            temps = self.main_window.body2_temp_history
            mass = self.main_window.right_mass_spinbox.value()
            hcap = self.main_window.right_hcap_spinbox.value()

        conductivity = self.main_window.conductivity_spinbox.value()
        label = f"{selected_body} (m={mass}kg, c={hcap}, k={conductivity})"

        self.ax.plot(times, temps, label=label)
        self.ax.relim()
        self.ax.autoscale()
        self.ax.legend()
        self.canvas.draw()

    def clear_graph(self):
        self.ax.clear()
        self.ax.set_ylabel("Temperature (°C)")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_xlim(0.0, 1.0)
        self.ax.set_ylim(0.0, 1.0)
        self.canvas.draw()