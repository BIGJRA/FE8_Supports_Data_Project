import tkinter as tk
from PIL import Image, ImageTk
import os


def custom_caps(char_name):
    char_name = char_name.capitalize()
    if char_name == "L'arachel":
        char_name = "L'Arachel"
    return char_name


class SupportFrame:

    def __init__(self, master, tracker, scroll_frame, char_1="L'Arachel", char_2='Duessel'):
        self.frame = tk.Frame(master, width=900, height=80)
        self.tracker = tracker
        self.scroll_frame = scroll_frame
        self.images = []  # prevent garbage collecting
        self.buttons = {}  # prevent garbage collecting
        self.root = master
        # place items
        self.char_1 = char_1
        self.char_2 = char_2
        self.place_name_label(char_1, 148)
        self.place_name_label(char_2, 375)
        self.place_image(char_1, 48)
        self.place_image(char_2, 275)
        self.place_button(" ", 500)
        self.place_button("C", 575)
        self.place_button("B", 650)
        self.place_button("A", 725)
        if self.tracker.get_in_progress(char_1, char_2):
            self.place_button("X", 825)
        else:
            self.place_button("+", 825)
        self.chosen_button = None

    def destroy(self):
        self.frame.destroy()

    def grid_me(self, row, col, pady=5):
        self.frame.grid(row=row, column=col, pady=pady)

    def place_name_label(self, char_name, x_pos, y_pos=40):
        label = tk.Label(self.frame, text=custom_caps(char_name), font=("courier", 20))
        label.place(x=x_pos, y=y_pos, anchor='center')

    def place_image(self, char_name, x_pos, y_pos=80):
        try:
            filename = os.path.join('img', f'fe8{char_name}.gif')
            img = Image.open(filename)
        except FileNotFoundError:  # handles l'arachel case
            filename = os.path.join('img', f'fe8larachel.gif')
            img = Image.open(filename)

        img = img.convert("RGBA")
        pimg = ImageTk.PhotoImage(img)
        self.images.append(pimg)
        label = tk.Label(self.frame, image=pimg, borderwidth=0, compound="center", highlightthickness=0)
        label.place(x=x_pos, y=y_pos, anchor='s')

    def place_button(self, title, x_pos, y_pos=40, ):
        commands_dict = {" ": self.process_space_button,
                         "C": self.process_c_button,
                         "B": self.process_b_button,
                         "A": self.process_a_button,
                         "X": self.process_x_button,
                         "+": self.process_plus_button
                         }
        color = "black"
        if self.tracker.get_rank(self.char_1, self.char_2) in ["C", "B", "A"] and title == "C":
            color = "green"
        elif self.tracker.get_rank(self.char_1, self.char_2) in ["B", "A"] and title == "B":
            color = "green"
        elif self.tracker.get_rank(self.char_1, self.char_2) in ["A"] and title == "A":
            color = "green"
        button = tk.Button(self.frame, font=('courier', 50), command=commands_dict[title], text=title, fg=color)
        self.buttons[title] = button
        button.place(x=x_pos, y=y_pos, anchor='center')

    def process_button(self):
        if self.chosen_button == " ":
            self.tracker.update_pair(self.char_1, self.char_2, "N/A")
        if self.chosen_button in ["C", "B", "A"]:
            self.tracker.update_pair(self.char_1, self.char_2, self.chosen_button)
        elif self.chosen_button == "X":
            self.tracker.set_current(self.char_1, self.char_2, False)
        elif self.chosen_button == "+":
            self.tracker.set_current(self.char_1, self.char_2)
        self.scroll_frame.update()

    def process_c_button(self):
        self.chosen_button = "C"
        self.process_button()

    def process_b_button(self):
        self.chosen_button = "B"
        self.process_button()

    def process_a_button(self):
        self.chosen_button = "A"
        self.process_button()

    def process_x_button(self):
        self.chosen_button = "X"
        self.process_button()

    def process_plus_button(self):
        self.chosen_button = "+"
        self.process_button()

    def process_space_button(self):
        self.chosen_button = " "
        self.process_button()


if __name__ == "__main__":
    root = tk.Tk()
    f1 = SupportFrame(root, None, None)
    f1.frame.pack()
    f2 = SupportFrame(root, None, None, 'Myrrh', 'Ephraim')
    f2.frame.pack()
    f3 = SupportFrame(root, None, None, 'Dozla', 'Ross')
    f3.frame.pack()
    root.mainloop()
