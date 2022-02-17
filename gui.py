from support_tracker import SupportTracker
# from tkinter import filedialog as fd
from tkinter import ttk
import tkinter as tk


class SupportGUI:

    def __init__(self):
        self.tracker = SupportTracker("support_data.json")

        self.root = tk.Tk()
        self.root.title('FE8 Support Tracker')
        #self.root.geometry("500x500")

        self.frame = ttk.Frame(self.root, padding=10)
        self.frame.grid()

        ttk.Separator(self.frame, orient=tk.VERTICAL).grid(column=0, row=3, rowspan=2, sticky='ns')

        # start new run button
        self.start_new_run_button = ttk.Button(
            self.frame,
            text='Start new run',
            command=self.tracker.start_new_run()
        )
        #self.start_new_run_button.pack(fill="x", side="top")
        self.start_new_run_button.grid(row=0, column=4, sticky="EW", padx=10)

        # reset all button
        self.reset_all_button = ttk.Button(
            self.frame,
            text='Reset all progress',
            command=self.tracker.reset_all()
        )
        #self.reset_all_button.pack(fill="x", side="right")
        self.reset_all_button.grid(row=1, column=4, sticky="EW", padx=10)

        # add random pair button
        self.add_random_pair_button = ttk.Button(
            self.frame,
            text='Add random pair to current run',
            command=self.tracker.add_new_random_pair
        )
        #self.add_random_pair_button.pack(fill="x", side="top")
        self.add_random_pair_button.grid(row=0, column=0, sticky="EW", columnspan=3)

        # drop down menu 1
        self.label_options = [
            "Eirika",
            "Seth",
            "L'Arachel"
        ]
        self.clicked = tk.StringVar()
        self.clicked.set("Character 1")

        self.drop = tk.OptionMenu(self.frame, self.clicked, *self.label_options)
        self.drop.grid(row=1, column=0,sticky="EW")
        self.drop.config(width=10)

        # drop down menu 2
        self.label_options = [
            "Eirika",
            "Seth",
            "L'Arachel"
        ]
        self.clicked = tk.StringVar()
        self.clicked.set("Character 2")

        self.drop = tk.OptionMenu(self.frame, self.clicked, *self.label_options)
        self.drop.grid(row=1, column=1,sticky="EW",padx=10)
        self.drop.config(width=10)

        # add this pair button
        self.add_given_pair_button = ttk.Button(
            self.frame,
            text='Add this pair',
            command=self.tracker.add_new_random_pair
        )
        # self.add_random_pair_button.pack(fill="x", side="top")
        self.add_given_pair_button.grid(row=1, column=2, sticky="EW")

        # pairings grid
        self.pairings_grid = ScrollFrame(self.frame)
        #self.pairings_grid.pack(fill="x", side="top")
        self.pairings_grid.grid(row=3, column=0, columnspan=5)

    def start_mainloop(self):
        """ Runs mainloop of GUI program"""
        self.root.mainloop()

    def update_pairings_grid(self):
        for pairing in self.tracker.get_current_pairs():
            pass


class ScrollFrame(tk.Frame):

    def __init__(self, parent):
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

        self.populate()

    def populate(self):
        """Put in some fake data"""
        for row in range(100):
            tk.Label(self.frame, text="%s" % row, width=3, borderwidth="1",
                     relief="solid").grid(row=row, column=0)
            t = "this is the second column for row fffffffffffffffffffff %s" % row
            tk.Label(self.frame, text=t).grid(row=row, column=1)

    def onFrameConfigure(self, event):
        """Reset the scroll region to encompass the inner frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


if __name__ == "__main__":
    gui = SupportGUI()
    gui.start_mainloop()
