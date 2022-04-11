""" Creates support frame GUI piece
"""

import os
import tkinter as tk
from PIL import Image, ImageTk

EXTENSIONS = {"fe7": ".png", "fe8": ".gif"}


def custom_caps(char_name):
    """
    :param char_name: str
    :return: str
    Performs custom capitalization to get rid of L'Arachel problem
    """
    char_name = char_name.capitalize()
    if char_name == "L'arachel":
        char_name = "L'Arachel"
    return char_name


class SupportFrame:
    """ Creates support frame for GUI
    """
    def __init__(self, master, tracker, scroll_frame, chars):
        self.frame = tk.Frame(master, width=900, height=80)
        self.tracker = tracker
        self.scroll_frame = scroll_frame
        self.images = []  # prevent garbage collecting
        self.buttons = {}  # prevent garbage collecting

        # place items
        self.chars = [chars[0], chars[1]]
        self.place_name_label(self.chars[0], 153)
        self.place_name_label(self.chars[1], 380)
        self.place_image(self.chars[0], 48)
        self.place_image(self.chars[1], 275)
        self.place_button(" ", 500)
        self.place_button("C", 575)
        self.place_button("B", 650)
        self.place_button("A", 725)
        if self.tracker.get_in_progress(self.chars[0], self.chars[1]):
            self.place_button("X", 825)
        else:
            self.place_button("+", 825)
        self.chosen_button = None

    def destroy(self):
        """
        Destroys the entire frame
        """
        self.frame.destroy()

    def grid_me(self, row, col, pady=5):
        """
        :param row: int
        :param col: int
        :param pady: int
        :return: None
        Grids this item at the given row and column, with specified vertical padding
        """
        self.frame.grid(row=row, column=col, pady=pady)

    def place_name_label(self, char_name, x_pos, y_pos=40):
        """
        :param char_name: str
        :param x_pos: int
        :param y_pos: int
        :return: None
        Places the label with the correct character name onto the frame
        """
        label = tk.Label(self.frame, text=custom_caps(char_name), font=("courier", 20))
        label.place(x=x_pos, y=y_pos, anchor='center')

    def place_image(self, char_name, x_pos, y_pos=80):
        """
        :param char_name: str
        :param x_pos: int
        :param y_pos: int
        :return: None
        Places the char_name's image at x, y coordinates
        """
        try:
            pth = f'{self.tracker.get_game()}{char_name}{EXTENSIONS[self.tracker.get_game()]}'
            filename = os.path.join('img', pth)
            img = Image.open(filename)
        except FileNotFoundError:  # handles l'arachel case
            filename = os.path.join('img', 'fe8larachel.gif')
            img = Image.open(filename)

        img = img.convert("RGBA")
        pimg = ImageTk.PhotoImage(img)
        self.images.append(pimg)
        label = tk.Label(self.frame, image=pimg,
                         borderwidth=0, compound="center", highlightthickness=0)
        label.place(x=x_pos, y=y_pos, anchor='s')

    def place_button(self, title, x_pos, y_pos=40, ):
        """
        :param title: str
        :param x_pos: int
        :param y_pos: int
        :return: None
        Places the button with the given title at the specified x and y positions
        """
        commands_dict = {" ": self.process_space_button,
                         "C": self.process_c_button,
                         "B": self.process_b_button,
                         "A": self.process_a_button,
                         "X": self.process_x_button,
                         "+": self.process_plus_button
                         }
        color = "black"
        if self.tracker.get_rank(self.chars[0], self.chars[1]) in ["C", "B", "A"] and title == "C":
            color = "green"
        elif self.tracker.get_rank(self.chars[0], self.chars[1]) in ["B", "A"] and title == "B":
            color = "green"
        elif self.tracker.get_rank(self.chars[0], self.chars[1]) in ["A"] and title == "A":
            color = "green"
        button = tk.Button(self.frame, font=('courier', 50),
                           command=commands_dict[title], text=title, fg=color)
        self.buttons[title] = button
        button.place(x=x_pos, y=y_pos, anchor='center')

    def process_button(self):
        """
        :return: None
        Processes the button pressed
        """
        if self.chosen_button == " ":
            self.tracker.update_pair(self.chars[0], self.chars[1], "N/A")
        if self.chosen_button in ["C", "B", "A"]:
            self.tracker.update_pair(self.chars[0], self.chars[1], self.chosen_button)
        elif self.chosen_button == "X":
            self.tracker.set_current(self.chars[0], self.chars[1], False)
        elif self.chosen_button == "+":
            self.tracker.set_current(self.chars[0], self.chars[1])
        self.scroll_frame.update()

    def process_c_button(self):
        """
        :return: None
        Processes C button press
        """
        self.chosen_button = "C"
        self.process_button()

    def process_b_button(self):
        """
        :return: None
        Processes B button press
        """
        self.chosen_button = "B"
        self.process_button()

    def process_a_button(self):
        """
        :return: None
        Processes A button press
        """
        self.chosen_button = "A"
        self.process_button()

    def process_x_button(self):
        """
        :return: None
        Processes X button press
        """
        self.chosen_button = "X"
        self.process_button()

    def process_plus_button(self):
        """
        :return: None
        Processes + button press
        """
        self.chosen_button = "+"
        self.process_button()

    def process_space_button(self):
        """
        :return: None
        Processes Space button press
        """
        self.chosen_button = " "
        self.process_button()


if __name__ == "__main__":
    root = tk.Tk()
    f1 = SupportFrame(root, None, None, ['Eirika, Tana'])
    f1.frame.pack()
    f2 = SupportFrame(root, None, None, ['Myrrh', 'Ephraim'])
    f2.frame.pack()
    f3 = SupportFrame(root, None, None, ['Dozla', 'Ross'])
    f3.frame.pack()
    root.mainloop()
