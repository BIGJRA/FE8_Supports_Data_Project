from support_tracker import SupportTracker
from support_frame import SupportFrame

# from tkinter import filedialog as fd
from tkinter import ttk
import tkinter as tk



class SupportGUI:

    def __init__(self):
        self.tracker = SupportTracker("support_data.json")
        #self.mode = "current" # current, remaining, completed, all
        self.mode_dict = {"Show pairs in current run": "current",
            "Show to-do pairs": "remaining",
            "Show all pairs": "all"
                          }
        self.tracker = SupportTracker("support_data.json")

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
            command=self.tracker.start_new_run()
        )
        #self.start_new_run_button.pack(fill="x", side="top")
        self.start_new_run_button.grid(row=0, column=4, sticky="EW")

        # reset all button
        self.reset_all_button = ttk.Button(
            self.frame,
            text='Reset all progress',
            command=self.tracker.reset_all()
        )
        #self.reset_all_button.pack(fill="x", side="right")
        self.reset_all_button.grid(row=1, column=4, sticky="EW")

        # add random pair button
        self.add_random_pair_button = ttk.Button(
            self.frame,
            text='Add random pair to current run',
            command=self.tracker.add_new_random_pair
        )
        #self.add_random_pair_button.pack(fill="x", side="top")
        self.add_random_pair_button.grid(row=0, column=0, sticky="EW", columnspan=3)

        # drop down menu 1
        self.char_options_1 = [
            "Eirika",
            "Seth",
            "L'Arachel"
        ]
        self.char1 = tk.StringVar()
        self.char1.set("Character 1")

        self.drop_char1 = tk.OptionMenu(self.frame, self.char1, *self.char_options_1)
        self.drop_char1.grid(row=1, column=0,sticky="EW")
        self.drop_char1.config(width=10)

        # drop down menu 2
        self.char_options_2 = [
            "Eirika",
            "Seth",
            "L'Arachel"
        ]
        self.char2 = tk.StringVar()
        self.char2.set("Character 2")

        self.drop_char2 = tk.OptionMenu(self.frame, self.char2, *self.char_options_2)
        self.drop_char2.grid(row=1, column=1,sticky="EW",padx=10)
        self.drop_char2.config(width=10)

        # add this pair button
        self.add_given_pair_button = ttk.Button(
            self.frame,
            text='Add this pair',
            command=self.tracker.add_new_random_pair
        )
        # self.add_random_pair_button.pack(fill="x", side="top")
        self.add_given_pair_button.grid(row=1, column=2, sticky="EW")

        ttk.Separator(self.frame, orient=tk.HORIZONTAL).grid(row=3, column=0, columnspan=5, sticky='ew', pady=10)

        # display drop down menu
        self.display_options = [
            "Show pairs in current run",
            "Show completed pairs",
            "Show to-do pairs",
            "Show all pairs"
        ]
        self.clicked = tk.StringVar()
        self.clicked.set("Show pairs in current run")
        self.drop = tk.OptionMenu(self.frame, self.clicked, *self.display_options)
        self.drop.grid(row=4, column=0, sticky="EW", columnspan=5)
        self.drop.config(width=10)

        # pairings grid
        self.pairings_grid = ScrollFrame(self.frame)
        #self.pairings_grid.pack(fill="x", side="top")
        self.pairings_grid.grid(row=5, column=0, columnspan=5, pady=10)

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
        self.items = [] # prevents garbage collection
        self.populate()



    def populate(self):
        chars = {
        0: ("l'arachel", "dozla"),
        1: ("cormag", "artur"),
        2: ("ephraim", 'eirika'),
        3: ("tethys", 'ewan'),
        4: ('innes', 'tana'),
        5: ('myrrh', 'franz'),
        6: ('amelia', 'gilliam'),
        7: ('rennac', 'gerik'),
        8: ('colm', 'neimi'),
        9: ('lute', 'syrene')
        }
        for row in range(10):
            item = SupportFrame(self.frame, None, chars[row][0], chars[row][1])
            item.grid_me(row=row, col=0, pady=5)
            self.items.append(item)

    def onFrameConfigure(self, event):
        """Reset the scroll region to encompass the inner frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


def main():
    gui = SupportGUI()
    gui.start_mainloop()


if __name__ == "__main__":
    main()