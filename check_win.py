from tkinter import messagebox
from setup_GUI import *

theoretical_board = [
    [""] * 7,
    [""] * 7,
    [""] * 7,
    [""] * 7,
    [""] * 7,
    [""] * 7,
    [""] * 7,
]
current_heights = [0, 0, 0, 0, 0, 0, 0]
moves = []
labels = []


def undo_move():
    if len(moves) >= 2:
        # remove computer move
        for z in range(2):
            last_move = moves.pop()
            theoretical_board[current_heights[last_move]][last_move] = ""
            current_heights[last_move] += -1
            if current_heights[last_move] == 5:
                choices.buttons[last_move]["state"] = "normal"
                choices.buttons_by_state[last_move] = "normal"
                choices.buttons[last_move]["background"] = "white"
            labels[current_heights[last_move]][last_move]["background"] = "white"


undo_button = tk.Button(
    master=other_button_frame, text="undo human move", command=undo_move, width=18
)
undo_button.grid(row=0, column=0)


def start_new_game():
    for i in labels:
        for j in i:
            j["background"] = "white"
    for i in range(len(moves)):
        last_move = moves.pop()
        theoretical_board[current_heights[last_move]][last_move] = ""
        current_heights[last_move] += -1
        labels[current_heights[last_move]][last_move]["background"] = "white"
    game_over.set(False)
    for i in choices.buttons:
        i["state"] = "normal"
        i["background"] = "white"
    choices.buttons_by_state = ["normal"] * 7
    for i in range(7):
        current_heights[i] = 0
        theoretical_board[i] = [""] * 7
    computer_on.set(True)
    turn_computer_off_button["state"] = "normal"
    undo_button["state"] = "normal"
    current_player.set("HUMAN")
    choices.disabled_buttons = 0
    print("*****   NEW GAME   *****")


new_game_button = tk.Button(
    master=other_button_frame,
    text="start new game",
    background="white",
    width=18,
    command=start_new_game,
)
new_game_button.grid(row=2, column=0)


def player_win(win_type):
    messagebox.showinfo(
        title="game over", message=f"{current_player.get()} wins by {win_type}"
    )
    close_game()


def close_game():
    game_over.set(True)
    with open("replays.txt", "w") as f:
        f.write("".join([str(i) for i in moves]))
    for button in choices.buttons:
        button["state"] = "disabled"
        button["background"] = "gray"
    choices.buttons_by_state = ["disabled"] * 7
    computer_on.set(False)
    undo_button["state"] = "disabled"
    turn_computer_off_button["state"] = "disabled"


def check_win(column, row):
    target = theoretical_board[row][column]
    win_types = set()
    # check vertical
    if row >= 3:
        if all(
            [
                theoretical_board[row - 1][column] == target,
                theoretical_board[row - 2][column] == target,
                theoretical_board[row - 3][column] == target,
            ]
        ):
            win_types.add("vertical")

    # check horizontal
    current_row = theoretical_board[row]
    current_run = 0
    for i in current_row:
        if i == target:
            current_run += 1
        else:
            current_run = 0
        if current_run >= 4:
            win_types.add("horizontal")

    if check_up_diagonal(target, row, column):
        win_types.add("up diagonal")
    if check_down_diagonal(target, row, column):
        win_types.add("down diagonal")
    if len(win_types) > 0:
        player_win(win_type=(" and ".join(win_types)))
        return True
    else:
        return False


def get_up_diagonal(row, column):
    res = []
    m, n = row, column
    while m > 0 and n > 0:
        m -= 1
        n -= 1
    while m < 6 and n < 6:
        res.append(theoretical_board[m][n])
        m += 1
        n += 1
    res.append(theoretical_board[m][n])
    return res


def get_down_diagonal(row, column):
    res = []
    m, n = row, column
    while m > 0 and n < 6:
        m -= 1
        n += 1
    while m < 6 and n > 0:
        res.append(theoretical_board[m][n])
        m += 1
        n -= 1
    res.append(theoretical_board[m][n])
    return res


def check_up_diagonal(target, row, column):
    current_up_diagonal = get_up_diagonal(row, column)
    current_run = 0
    for i in current_up_diagonal:
        if i == target:
            current_run += 1
        else:
            current_run = 0
        if current_run >= 4:
            return True
    return False


def check_down_diagonal(target, row, column):
    current_down_diagonal = get_down_diagonal(row, column)
    current_run = 0
    for i in current_down_diagonal:
        if i == target:
            current_run += 1
        else:
            current_run = 0
        if current_run >= 4:
            return True
    return False
