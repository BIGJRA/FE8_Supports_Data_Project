""" Runs the Support Tracker GUI
"""

from tkinter import ttk
import tkinter as tk
from support_tracker import SupportTracker
from scroll_frame import ScrollFrame

MODE_DICT = {"Show pairs in current run": "current", "Show all pairs": "all"}


class SupportGUI:
    """ SupportGUI class
    """

    def __init__(self, game):
        # stores the given tracker as a class object
        self.tracker = SupportTracker(f"data/{game}_support_data.json")
        self.game = game

        # Tkinter root object
        self.root = tk.Tk()
        self.root.title(f'{self.game.upper()} Support Tracker')

        # Tkinter frame, master root. Holds all other objects of the GUI
        self.gui_elements = {"frame": ttk.Frame(self.root, padding=10)}
        self.gui_elements["frame"].grid()

        # Separators for left side and right side buttons, top and bottom sections
        ttk.Separator(self.gui_elements["frame"], orient=tk.VERTICAL) \
            .grid(row=0, column=3, rowspan=2, sticky='ns')
        ttk.Separator(self.gui_elements["frame"], orient=tk.HORIZONTAL) \
            .grid(row=2, column=0, columnspan=5, sticky='ew', pady=10)

        # start new run button
        self.gui_elements["start_new_run_button"] = ttk.Button(
            self.gui_elements["frame"],
            text='Start new run',
            command=self.start_new_run_helper
        )
        self.gui_elements["start_new_run_button"].grid(row=0, column=4, sticky="EW")

        # reset all button
        self.gui_elements["reset_all_button"] = ttk.Button(
            self.gui_elements["frame"],
            text='Reset all progress',
            command=self.reset_all_helper
        )
        self.gui_elements["reset_all_button"].grid(row=1, column=4, sticky="EW")

        # add random pair button
        self.gui_elements["add_random_pair_button"] = ttk.Button(
            self.gui_elements["frame"],
            text='Add random pair to current run',
            command=self.add_new_random_pair_helper
        )
        self.gui_elements["add_random_pair_button"].grid(row=0, column=0, sticky="EW", columnspan=3)

        # display drop down menu
        self.gui_elements["display_options"] = [
            "Show pairs in current run",
            "Show all pairs"
        ]

        self.gui_elements["clicked"] = tk.StringVar()
        self.gui_elements["clicked"]\
            .set(self.gui_elements["display_options"][0])  # default drop text
        self.gui_elements["drop"] = tk.OptionMenu(
            self.gui_elements["frame"],
            self.gui_elements["clicked"],
            *self.gui_elements["display_options"])
        self.gui_elements["drop"].grid(row=1, column=0, sticky="EW", columnspan=2)

        # accept button
        self.gui_elements["submit_button"] = tk.Button(self.gui_elements["frame"], text="Update",
                                                       command=self.set_mode_helper)
        self.gui_elements["submit_button"].grid(row=1, column=2, sticky="EW", columnspan=1)

        # pairings grid - uses my ScrollFrame class
        self.scroll_frame = ScrollFrame(self.gui_elements["frame"], self)
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
        Command done when "Update" button is pressed.
        Updates the internal mode and the SupportFrame.
        :return: None
        """
        # self.scroll_frame.set_mode(self.get_mode())
        self.scroll_frame.update()

    def get_mode(self):
        """
        Returns the short string version of the mode
        :return: str
        """
        return MODE_DICT[self.gui_elements["clicked"].get()]

    def get_tracker(self):
        """
        Returns the tracker object of this gui
        :return: SupportTracker
        """
        return self.tracker


def main(game):
    """
    :param game: str
    :return: None
    Starts the game.
    """
    gui = SupportGUI(game)
    gui.start_mainloop()


if __name__ == "__main__":
    main("fe7")
