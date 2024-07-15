import time
from tkinter import Tk, Frame, Label, Entry, Button
from tkinter.ttk import Combobox

import pyautogui

from clicker import Clicker


class SetAmountUI:
    def __init__(self, master, clicker):
        default_color = "#4A148C"
        self.frame = Frame(master)
        self.frame.configure(bg=default_color)

        self.clicker = clicker

        self.x_label = Label(self.frame, text="X coordinate:")
        self.x_label.pack()
        self.x_entry = Entry(self.frame)
        self.x_entry.pack()

        self.y_label = Label(self.frame, text="Y coordinate:")
        self.y_label.pack()
        self.y_entry = Entry(self.frame)
        self.y_entry.pack()

        self.amount_label = Label(self.frame, text="Number of clicks:")
        self.amount_label.pack()
        self.amount_entry = Entry(self.frame)
        self.amount_entry.pack()

        self.set_amount_button = Button(self.frame, text="Start Clicking", command=self.start_clicking)
        self.set_amount_button.pack(pady=10)

    def start_clicking(self):
        try:
            x = int(self.x_entry.get())
            y = int(self.y_entry.get())
            amount = int(self.amount_entry.get())
            self.clicker.click_many(x, y, amount)
            print(f"Clicking {amount} times at ({x}, {y})")
        except ValueError:
            print("Please enter valid integer values for coordinates and number of clicks.")

    def show(self):
        self.frame.pack(expand=True, fill='both')

    def hide(self):
        self.frame.pack_forget()


class SingleClickUI:
    def __init__(self, master, clicker):
        default_color = "#4A148C"
        default_text_color = "#D1C4E9"

        self.frame = Frame(master)
        self.frame.configure(bg=default_color)
        self.clicker = clicker

        self.x_label = Label(self.frame, text="X coordinate:")
        self.x_label.configure(bg=default_color, fg=default_text_color)
        self.x_label.pack()
        self.x_entry = Entry(self.frame)
        self.x_entry.pack()

        self.y_label = Label(self.frame, text="Y coordinate:")
        self.y_label.pack()
        self.y_entry = Entry(self.frame)
        self.y_entry.pack()

        self.single_click_button = Button(self.frame, text="Single Click", command=self.start_clicking)
        self.single_click_button.pack(pady=10)

    def start_clicking(self):
        try:
            x = int(self.x_entry.get())
            y = int(self.y_entry.get())
            self.clicker.click(x, y)
            print(f"Single click at ({x}, {y})")
        except ValueError:
            print("Please enter valid integer coordinates.")

    def show(self):
        self.frame.pack(expand=True, fill='both')

    def hide(self):
        self.frame.pack_forget()


class SpamClickUI:
    def __init__(self, master):
        default_color = "#4A148C"

        self.frame = Frame(master)
        self.frame.configure(bg=default_color)

        # Section for delay in milliseconds
        self.delay_label = Label(self.frame, text="Delay in milliseconds:")
        self.delay_label.pack()
        self.delay_entry = Entry(self.frame)
        self.delay_entry.insert(0, "100")
        self.delay_entry.pack()
        self.spam_click_button = Button(self.frame, text="Start Spamming", command=self.start_spamming)
        self.spam_click_button.pack(pady=10)

    def start_spamming(self):
        print("Spamming everywhere!")
        # Use clicker class to spam click everywhere
        while True:
            pyautogui.click()
            delay = int(self.delay_entry.get())
            if delay > 0:
                time.sleep(delay / 1000)

    def show(self):
        self.frame.pack(expand=True, fill='both')

    def hide(self):
        self.frame.pack_forget()


class GUI:
    def __init__(self):
        self.window = Tk()
        self.window.title("Fluffy's Auto Clicker :3")
        self.window.geometry("500x500")

        # Set window background color to hex code
        color = "#4A148C"
        self.window.configure(bg=color)

        self.clicker = Clicker(delay=0.1)

        title_label = Label(self.window, text="Fluffy's Auto Clicker :3", font=("Arial", 24))
        text_color = "#D1C4E9"
        title_label.configure(bg=color, fg=text_color)
        title_label.configure(disabledforeground=title_label.cget("foreground"))
        title_label.configure(state="disabled")
        title_label.pack(pady=20)

        # Combobox menu for different click modes
        self.option_dropdown = Combobox(self.window, state="readonly",
                                        values=["Single Click", "Set amount of clicks", "Spam Click Everywhere"])
        self.option_dropdown.current(0)
        self.option_dropdown.pack(pady=10)
        self.option_dropdown.bind("<<ComboboxSelected>>", self.on_mode_change)

        # Frame to hold the current UI
        self.ui_frame = Frame(self.window)
        self.ui_frame.pack(pady=20, expand=True, fill='both')

        # Different UI's for different click modes
        self.single_click_ui = SingleClickUI(self.ui_frame, self.clicker)
        self.set_amount_ui = SetAmountUI(self.ui_frame, self.clicker)
        self.spam_click_ui = SpamClickUI(self.ui_frame)

        # Initially show the single click UI
        self.current_ui = self.single_click_ui
        self.current_ui.show()

        self.window.mainloop()

    # noinspection PyUnusedLocal
    def on_mode_change(self, event):
        # Hide the current UI
        self.current_ui.hide()

        # Show the new UI based on the selected option
        selected_option = self.option_dropdown.get()
        if selected_option == "Single Click":
            self.current_ui = self.single_click_ui
        elif selected_option == "Set amount of clicks":
            self.current_ui = self.set_amount_ui
        elif selected_option == "Spam Click Everywhere":
            self.current_ui = self.spam_click_ui

        self.current_ui.show()
