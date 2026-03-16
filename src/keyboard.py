import sys
import subprocess
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout
from PyQt6.QtCore import Qt

# Full layout with special keys
layout_keys = [
    ['1','2','3','4','5','6','7','8','9','0','Backspace'],
    ['Tab','q','w','e','r','t','y','u','i','o','p'],
    ['Caps','a','s','d','f','g','h','j','k','l','Enter'],
    ['Shift','z','x','c','v','b','n','m','Shift'],
    ['Space']
]

class Keyboard(QWidget):

    def __init__(self):
        super().__init__()
        self.shift = False
        self.caps = False
        self.init_ui()

    def init_ui(self):
        grid = QGridLayout()
        grid.setSpacing(5)

        # Loop over each row
        for row_idx, row in enumerate(layout_keys):

            # Calculate "weight" for centering row
            total_weight = sum([6 if k=="Space" else 2 if k in ["Shift","Backspace","Enter","Caps","Tab"] else 1 for k in row])
            col_idx = 0

            for key in row:
                btn = QPushButton(key)
                btn.setMinimumHeight(70)
                btn.setStyleSheet("""
                    font-size:18px;
                    border-radius:8px;
                    padding:10px;
                """)

                # assign width based on key type
                if key == "Space":
                    width = 6
                elif key in ["Shift","Backspace","Enter","Caps","Tab"]:
                    width = 2
                else:
                    width = 1

                # Center row by adding empty columns before it
                start_col = (12 - total_weight) // 2
                grid.addWidget(btn, row_idx, col_idx + start_col, 1, width)

                btn.clicked.connect(lambda _, k=key: self.key_press(k))
                col_idx += width

        self.setLayout(grid)
        self.setWindowTitle("Touchboard")
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.resize(1000,350)
        self.setStyleSheet("""
            QWidget { background:#202020; }
            QPushButton { font-size:18px; border-radius:8px; padding:10px; }
            QPushButton:pressed { background:#444; }
        """)

    def key_press(self,key):
        # Handle special keys first
        if key == "Space":
            subprocess.run(["xdotool","key","space"])
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
        if key == "Shift":
            self.shift = not self.shift
            return
        if key == "Caps":
            self.caps = not self.caps
            return

        # Letters / numbers
        if len(key) == 1:
            char = key
            if self.shift ^ self.caps:
                char = char.upper()
            subprocess.run(["xdotool","type",char])
            if self.shift:
                self.shift = False  # Shift only applies once

def main():
    app = QApplication(sys.argv)
    keyboard = Keyboard()
    keyboard.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
