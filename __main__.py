from gui import main
from tkinter import ttk
import tkinter as tk

options = ["fe7", "fe8"]
game = input(f"Which tracker would you like to use? Options: {str(options)}\n")
while game not in options:
    game = input(f"Which tracker would you like to use? Options: {str(options)}\n")

main(game)
