from support_tracker import SupportTracker
#from tkinter import filedialog as fd
from tkinter import ttk
import tkinter as tk


class SupportGUI:
    def __init__(self):
        self.tracker = SupportTracker("support_data.json")

        self.root = tk.Tk()
        self.root.title('FE8 Support Tracker')
        self.frame = ttk.Frame(self.root, padding=10)
        self.frame.grid()

        # add random pair button
        self.add_random_pair_button = ttk.Button(
            self.frame,
            text='Add random pair to current run',
            command=self.tracker.add_new_random_pair
        )
        self.add_random_pair_button.grid(row=0, column=0)

        # start new run button
        self.add_random_pair_button = ttk.Button(
            self.frame,
            text='Start new run',
            command=self.tracker.start_new_run()
        )
        self.add_random_pair_button.grid(row=1, column=0)

        # reset all button
        self.add_random_pair_button = ttk.Button(
            self.frame,
            text='Reset all progress',
            command=self.tracker.reset_all()
        )
        self.add_random_pair_button.grid(row=2, column=0)

        # pairings grid
        self.pairings_grid = ttk.Frame(self.frame)
        self.pairings_grid.grid(row=3, column=0)

    def start_mainloop(self):
        """ Runs mainloop of GUI program"""
        self.root.mainloop()

    def update_pairings_grid(self):
        for pairing in self.tracker.get_current_pairs():
            pass

if __name__ == "__main__":
    gui = SupportGUI()
    gui.start_mainloop()
