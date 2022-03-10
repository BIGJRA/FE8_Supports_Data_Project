from support_tracker import SupportTracker
from support_frame import SupportFrame

# from tkinter import filedialog as fd
from tkinter import ttk
import tkinter as tk

from fe8_custom_sort import fe8_sort

class SupportGUI:

    def __init__(self):
        try:
            self.tracker = SupportTracker("support_data.json")
        except FileNotFoundError:
            self.tracker = SupportTracker(r"sacred_stones/support_data.json")
        #self.mode = "current" # current, remaining, completed, all
        self.mode_dict = {"Show pairs in current run": "current",
            "Show to-do pairs": "remaining",
            "Show all pairs": "all"
                          }

        self.root = tk.Tk()
        self.root.title('FE8 Support Tracker')
        #self.root.geometry("500x500")

        self.frame = ttk.Frame(self.root, padding=10)
        self.frame.grid()

        ttk.Separator(self.frame, orient=tk.VERTICAL).grid(row=0, column=3, rowspan=2, sticky='ns')

        # start new run button
        self.start_new_run_button = ttk.Button(
            self.frame,
            text='Start new run',
            command=self.start_new_run_helper
        )
        #self.start_new_run_button.pack(fill="x", side="top")
        self.start_new_run_button.grid(row=0, column=4, sticky="EW")

        # reset all button
        self.reset_all_button = ttk.Button(
            self.frame,
            text='Reset all progress',
            command=self.reset_all_helper
        )
        #self.reset_all_button.pack(fill="x", side="right")
        self.reset_all_button.grid(row=1, column=4, sticky="EW")

        # add random pair button
        self.add_random_pair_button = ttk.Button(
            self.frame,
            text='Add random pair to current run',
            command=self.add_new_random_pair_helper
        )
        #self.add_random_pair_button.pack(fill="x", side="top")
        self.add_random_pair_button.grid(row=0, column=0, sticky="EW", columnspan=3)

        ttk.Separator(self.frame, orient=tk.HORIZONTAL).grid(row=2, column=0, columnspan=5, sticky='ew', pady=10)

        # display drop down menu
        self.display_options = [
            "Show pairs in current run",
            #"Show to-do pairs",
            "Show all pairs"
        ]
        self.clicked = tk.StringVar()
        self.clicked.set("Show pairs in current run")
        self.drop = tk.OptionMenu(self.frame, self.clicked, *self.display_options)
        self.drop.grid(row=1, column=0, sticky="EW", columnspan=2)
        self.drop.config(width=10)

        # accept button
        self.submit_button = tk.Button(self.frame, text="Update", command=self.set_mode_helper)
        self.submit_button.grid(row=1, column=2, sticky = "EW", columnspan=1)

        # pairings grid
        self.scroll_frame = ScrollFrame(self.frame, self.tracker, self)
        #self.pairings_grid.pack(fill="x", side="top")
        self.scroll_frame.grid(row=3, column=0, columnspan=5, pady=10)

    def start_mainloop(self):
        """ Runs mainloop of GUI program"""
        self.root.mainloop()

    def start_new_run_helper(self):
        self.tracker.start_new_run()
        self.scroll_frame.update()

    def reset_all_helper(self):
        self.tracker.reset_all()
        self.scroll_frame.update()

    def add_new_random_pair_helper(self):
        self.tracker.add_new_random_pair()
        self.scroll_frame.update()

    def set_mode_helper(self):
        self.scroll_frame.set_mode(self.mode_dict[self.clicked.get()])
        self.scroll_frame.update()

class ScrollFrame(tk.Frame):

    def __init__(self, parent, tracker=None, gui=None):
        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, height=500, width=800)
        self.frame = tk.Frame(self.canvas)
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4, 4), window=self.frame, anchor="nw",
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)
        self.items = [] # prevents garbage collection
        self.tracker = tracker
        self.mode = 'current'

        self.gui = gui
        self.update()

    def set_mode(self, mode):
        self.mode = mode

    def update(self):
        """
        :return: None
        Updates the Scroll Frame with the information in the tracker with the given mode.
        """

        # resets the entire table before doing the update
        for item in self.items:
            item.destroy()

        #gets the correct set of characters
        mode = self.mode
        if self.mode == "current":
            chars = self.tracker.get_current_pairs()
        if self.mode == "all":
            chars = self.tracker.get_all_pairs()
        if self.mode == "remaining":
            chars = self.tracker.get_remaining_pairs()
        chars.sort(key = lambda x: (fe8_sort.index(x[0]), fe8_sort.index(x[1])))

        # add the correct rows
        for row in range(len(chars)):
            item = SupportFrame(self.frame, self.tracker, self, chars[row][0], chars[row][1])
            item.grid_me(row=row, col=0, pady=5)
            self.items.append(item)

    def onFrameConfigure(self, event):
        """Helper function that resets the scroll region to encompass the inner frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


def main():
    gui = SupportGUI()
    gui.start_mainloop()


if __name__ == "__main__":
    main()