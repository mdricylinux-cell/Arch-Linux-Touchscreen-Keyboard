import sys
import subprocess
import os
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout
from PyQt6.QtCore import Qt
import json

# Load layout from JSON
LAYOUT_FILE = os.path.join(os.path.dirname(__file__), "../layouts/default.json")
with open(LAYOUT_FILE) as f:
    layout = json.load(f)

class Keyboard(QWidget):

    def __init__(self):
        super().__init__()
        self.shift = False
        self.caps = False
        self.symbols = False
        self.init_ui()

    def init_ui(self):
        self.grid = QGridLayout()
        self.grid.setSpacing(5)
        self.setLayout(self.grid)

        self.rows = []
        self.build_keyboard()
        self.setWindowTitle("Touchboard")
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.resize(1000,350)
        self.setStyleSheet("""
            QWidget { background:#202020; }
            QPushButton { font-size:18px; border-radius:8px; padding:10px; }
            QPushButton:pressed { background:#444; }
            QPushButton.active { background:#555; }
        """)

    def build_keyboard(self):
        self.clear_grid()
        self.buttons = []

        # Top row: numbers or symbols
        top_keys = layout["symbols"] if self.symbols else layout["numbers"]
        self.add_row(top_keys + ["Backspace"], 0)

        # Letter rows
        for i, letter_row in enumerate(layout["letters"]):
            row_keys = letter_row.copy()
            if i == 0:
                row_keys = ["Tab"] + row_keys
            elif i == 1:
                row_keys = ["Caps"] + row_keys + ["Enter"]
            elif i == 2:
                row_keys = ["Shift"] + row_keys + ["Shift"]
            self.add_row(row_keys, i+1)

        # Space row
        self.add_row(["Space"], 4)

    def clear_grid(self):
        # Remove previous buttons
        for i in reversed(range(self.grid.count())):
            self.grid.itemAt(i).widget().setParent(None)

    def add_row(self, keys, row):
        col = 0
        total_weight = sum([6 if k=="Space" else 2 if k in ["Shift","Backspace","Enter","Caps","Tab"] else 1 for k in keys])
        start_col = (12 - total_weight)//2

        for k in keys:
            btn = QPushButton(k)
            btn.setMinimumHeight(70)
            width = 1
            if k == "Space": width = 6
            elif k in ["Shift","Backspace","Enter","Caps","Tab"]: width = 2

            btn.clicked.connect(lambda _, key=k: self.key_press(key))
            self.grid.addWidget(btn, row, col + start_col, 1, width)
            self.buttons.append(btn)
            col += width

        self.update_shift_caps_visual()

    def update_shift_caps_visual(self):
        for btn in self.buttons:
            if btn.text() == "Shift":
                btn.setStyleSheet("background:#555;" if self.shift else "")
            elif btn.text() == "Caps":
                btn.setStyleSheet("background:#555;" if self.caps else "")

    def key_press(self, key):
        # Toggle layers
        if key == "Shift":
            self.shift = not self.shift
            self.update_shift_caps_visual()
            return
        if key == "Caps":
            self.caps = not self.caps
            self.update_shift_caps_visual()
            return
        if key == "Backspace":
            subprocess.run(["xdotool","key","BackSpace"])
            return
        if key == "Enter":
            subprocess.run(["xdotool","key","Return"])
            return
        if key == "Tab":
            subprocess.run(["xdotool","key","Tab"])
            return
        if key == "Space":
            subprocess.run(["xdotool","key","space"])
            return

        # Determine character
        char = key
        if len(char) == 1:  # letters/numbers
            if char.isalpha():
                if self.shift ^ self.caps:
                    char = char.upper()
                else:
                    char = char.lower()
                if self.shift:
                    self.shift = False
                    self.update_shift_caps_visual()
            elif self.shift:
                # Shift + symbol = toggle to symbol layer
                self.symbols = not self.symbols
                self.build_keyboard()
        subprocess.run(["xdotool","type",char])

def main():
    app = QApplication(sys.argv)
    kb = Keyboard()
    kb.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
