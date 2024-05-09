import tkinter as tk


root = tk.Tk()
root.geometry("500x500")
root.config(background="gold")
root.title("4 in a row by Robert Davie")
current_player = tk.StringVar(master=root, value="HUMAN")
computer_on = tk.BooleanVar(value=True)
game_over = tk.BooleanVar(value=False)
replay_frame_by_frame_on = tk.BooleanVar(value=False)


def toggle_computer_off():
    if computer_on.get():
        computer_on.set(False)
        turn_computer_off_button.config(
            background="azure3", text="turn computer back on"
        )
    else:
        computer_on.set(True)
        turn_computer_off_button.config(background="white", text="turn computer off")


board = tk.Frame(master=root)
board.grid(row=1, column=1, padx=20, pady=20)

other_button_frame = tk.Frame(master=root, background="gold")
other_button_frame.grid(row=1, column=2)

turn_computer_off_button = tk.Button(
    master=other_button_frame,
    text="turn computer off",
    background="white",
    command=lambda: toggle_computer_off(),
    width=18,
    justify="left",
    anchor="w",
)
turn_computer_off_button.grid(column=0, row=1)


class Choices:
    def __init__(self):
        self.buttons = []
        self.disabled_buttons = 0
        self.buttons_by_state = ["normal"] * 7


choices = Choices()
choice_frame = tk.Frame(master=root)
choice_frame.grid(row=0, column=1, pady=10)
