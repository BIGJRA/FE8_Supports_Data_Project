""" Main module which runs GUI program.
"""
from gui import main


options = ["fe7", "fe8"]
game = input(f"Which tracker would you like to use? Options: {str(options)}\n")
while game not in options:
    game = input(f"Which tracker would you like to use? Options: {str(options)}\n")

main(game)
