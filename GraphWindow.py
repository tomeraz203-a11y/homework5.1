from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PySide6.QtWidgets import QComboBox, QHBoxLayout, QPushButton, QVBoxLayout, QWidget


class GraphWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setupUI()

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
