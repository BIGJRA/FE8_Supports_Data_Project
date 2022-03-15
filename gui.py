from support_tracker import SupportTracker
from scroll_frame import ScrollFrame
from tkinter import ttk
import tkinter as tk


class SupportGUI:

    def __init__(self, game):
        # stores the given tracker as a class object
        self.tracker = SupportTracker(f"data/{game}_support_data.json")  # TODO: fix this via os module
        self.game = game

        # Tkinter root object
        self.root = tk.Tk()
        self.root.title(f'{self.game.upper()} Support Tracker')

        # Tkinter frame, master root. Holds all other objects of the GUI
        self.frame = ttk.Frame(self.root, padding=10)
        self.frame.grid()

        # Separators for left side and right side buttons, top and bottom sections
        ttk.Separator(self.frame, orient=tk.VERTICAL).grid(row=0, column=3, rowspan=2, sticky='ns')
        ttk.Separator(self.frame, orient=tk.HORIZONTAL).grid(row=2, column=0, columnspan=5, sticky='ew', pady=10)

        # start new run button
        self.start_new_run_button = ttk.Button(
            self.frame,
            text='Start new run',
            command=self.start_new_run_helper
        )
        self.start_new_run_button.grid(row=0, column=4, sticky="EW")

        # reset all button
        self.reset_all_button = ttk.Button(
            self.frame,
            text='Reset all progress',
            command=self.reset_all_helper
        )
        self.reset_all_button.grid(row=1, column=4, sticky="EW")

        # add random pair button
        self.add_random_pair_button = ttk.Button(
            self.frame,
            text='Add random pair to current run',
            command=self.add_new_random_pair_helper
        )
        self.add_random_pair_button.grid(row=0, column=0, sticky="EW", columnspan=3)

        # display drop down menu
        self.display_options = [
            "Show pairs in current run",
            # "Show to-do pairs",
            "Show all pairs"  # TODO: add more modes here
        ]
        self.mode_dict = {"Show pairs in current run": "current",
                          # "Show to-do pairs": "remaining",
                          "Show all pairs": "all"
                          }

        self.clicked = tk.StringVar()
        self.clicked.set(self.display_options[0])  # sets default drop menu text
        self.drop = tk.OptionMenu(self.frame, self.clicked, *self.display_options)
        self.drop.grid(row=1, column=0, sticky="EW", columnspan=2)

        # accept button
        self.submit_button = tk.Button(self.frame, text="Update", command=self.set_mode_helper)
        self.submit_button.grid(row=1, column=2, sticky="EW", columnspan=1)

        # pairings grid - uses my ScrollFrame class
        self.scroll_frame = ScrollFrame(self.frame, self)
        self.scroll_frame.grid(row=3, column=0, columnspan=5, pady=10)

    def start_mainloop(self):
        """ Runs mainloop of GUI program"""
        self.root.mainloop()

    def start_new_run_helper(self):
        """
        :return: None
        Command done when "Start new run" button is pressed. """
        self.tracker.start_new_run()
        self.scroll_frame.update()

    def reset_all_helper(self):
        """
        :return: None
        Command done when "Reset all" button is pressed.
        TODO: maybe do a check that the user is serious?
        """
        self.tracker.reset_all()
        self.scroll_frame.update()

    def add_new_random_pair_helper(self):
        """
        :return: None
        Command done when "Add new random pair" button is pressed.
        """
        self.tracker.add_new_random_pair()
        self.scroll_frame.update()

    def set_mode_helper(self):
        """
        Command done when "Update" button is pressed. Updates the internal mode and the SupportFrame.
        :return: None
        """
        # self.scroll_frame.set_mode(self.get_mode())
        self.scroll_frame.update()

    def get_mode(self):
        """
        Returns the short string version of the mode
        :return: str
        """
        return self.mode_dict[self.clicked.get()]

    def get_tracker(self):
        """
        Returns the tracker object of this gui
        :return: SupportTracker
        """
        return self.tracker


def main():
    gui = SupportGUI("fe8")
    gui.start_mainloop()


if __name__ == "__main__":
    main()
