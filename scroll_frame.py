from data.sorts import *
import tkinter as tk
from support_frame import SupportFrame


class ScrollFrame(tk.Frame):

    def __init__(self, parent, gui=None):

        # Do not change this block - from the internet. Creates the scroll block
        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, height=500, width=900)
        self.frame = tk.Frame(self.canvas)
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4, 4), window=self.frame, anchor="nw",
                                  tags="self.frame")
        self.frame.bind("<Configure>", self.on_frame_configure)

        # prevents garbage collection
        self.items = []

        # instantiates referential objects
        self.gui = gui
        self.tracker = gui.get_tracker()
        self.game = self.tracker.get_game()

        # initially updates frame
        self.update()

    def on_frame_configure(self, event):
        """
        :return: event
        Helper function that resets the scroll region to encompass the inner frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        return event

    def update(self):
        """
        :return: None
        Updates the Scroll Frame with the information in the tracker with the given mode.
        """

        # resets the entire table before doing the update
        for item in self.items:
            item.destroy()
        self.items = []

        # gets the correct set of characters
        mode = self.gui.get_mode()
        chars = []
        if mode == "current":
            chars = self.tracker.get_current_pairs()
        elif mode == "all":
            chars = self.tracker.get_all_pairs()
        # elif mode == "remaining":
        #    chars = self.tracker.get_remaining_pairs()

        #  sort: sorts according to MAX of the sort index.
        if self.game == 'fe8':
            chars.sort(key=lambda x: (max(fe8_sort.index(x[0]), fe8_sort.index(x[1])), fe8_sort.index(x[0])))
        else:  # self.game == 'fe7':
            chars.sort(key=lambda x: (max(fe7_sort.index(x[0]), fe7_sort.index(x[1])), fe7_sort.index(x[0])))

        # add the correct rows
        for pos, data in enumerate(chars):
            item = SupportFrame(self.frame, self.tracker, self, data[0], data[1])
            item.grid_me(row=pos, col=0, pady=5)
            self.items.append(item)
