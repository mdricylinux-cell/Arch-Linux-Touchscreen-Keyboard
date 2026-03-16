import sys
import subprocess
import json

from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout
from PyQt6.QtCore import Qt


LAYOUT_FILE = "layouts/default.json"


class Keyboard(QWidget):

    def __init__(self):
        super().__init__()
        self.load_layout()
        self.init_ui()

    def load_layout(self):

        try:
            with open(LAYOUT_FILE) as f:
                data = json.load(f)
                self.layout_keys = data["layout"]

        except:
            self.layout_keys = [
                ['1','2','3','4','5','6','7','8','9','0'],
                ['q','w','e','r','t','y','u','i','o','p'],
                ['a','s','d','f','g','h','j','k','l'],
                ['z','x','c','v','b','n','m'],
                ['space']
            ]

    def init_ui(self):

        grid = QGridLayout()

        for row, line in enumerate(self.layout_keys):
            for col, key in enumerate(line):

                button = QPushButton(key)

                button.setMinimumSize(70,70)

                button.clicked.connect(
                    lambda _, k=key: self.key_press(k)
                )

                grid.addWidget(button,row,col)

        self.setLayout(grid)

        self.setWindowTitle("Touchboard")

        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint
        )

        self.resize(900,300)

        self.setStyleSheet("""

        QPushButton {

            font-size:20px;
            border-radius:10px;
            padding:10px;

        }

        """)

    def key_press(self,key):

        if key == "space":

            subprocess.run(["xdotool","key","space"])

        else:

            subprocess.run(["xdotool","type",key])


def main():

    app = QApplication(sys.argv)

    keyboard = Keyboard()

    keyboard.show()

    sys.exit(app.exec())


if __name__ == "__main__":

    main()
