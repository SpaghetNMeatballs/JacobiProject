from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QTableWidgetItem,
    QTableWidget,
    QVBoxLayout,
    QWidget,
    QSpinBox,
)
from main import Jacobi

import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        self.input = QSpinBox()
        self.table = QTableWidget(self)
        self.button = QPushButton("Calculate")
        self.button.clicked.connect(self.calculate)
        self.input.valueChanged.connect(self.table.setColumnCount)
        self.input.valueChanged.connect(self.table.setRowCount)
        self.input.setValue(5)
        self.table.setRowCount(self.input.value())
        self.table.setColumnCount(self.input.value())

        layout = QVBoxLayout()
        layout.addWidget(self.input)
        layout.addWidget(self.table)
        layout.addWidget(self.button)

        container = QWidget()
        container.setLayout(layout)

        # Устанавливаем центральный виджет Window.
        self.setCentralWidget(container)

    def load_table(self, data: list[list[int]]):
        assert len(data) == self.table.rowCount()
        assert len(data[0]) == self.table.columnCount()
        assert sum([len(i) == len(data[0]) for i in data]) == len(data)
        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                self.table.setItem(
                    row, col, QTableWidgetItem(str(round(data[row][col], 3)))
                )

    def calculate(self):
        data = []
        for row in range(self.table.rowCount()):
            data.append([])
            for col in range(self.table.columnCount()):
                data[row].append(float(self.table.item(row, col).text()))
        jac = Jacobi(data)
        while jac.s > 0.1:
            jac.iterate()
            self.load_table(jac.a)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
