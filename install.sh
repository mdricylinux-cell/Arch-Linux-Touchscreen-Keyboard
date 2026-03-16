#!/bin/bash

echo "Installing Touchboard dependencies..."

sudo pacman -S --needed python python-pyqt6 xdotool

echo "Done."
echo "Run with:"
echo "python src/keyboard.py"
