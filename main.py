import random
import time
import tkinter as tk
from tkinter import messagebox

NUMBER_OF_ROWS = 7
NUMBER_OF_COLUMNS = 7

theoretical_board = [[""] * 7 for _ in range(7)]

current_heights = [0] * 7
moves = []
labels = []
overall_estimate = []


root = tk.Tk()
root.geometry("500x500")
root.config(background="gold")
root.title("4 in a row by Robert Davie")
current_player = tk.StringVar(master=root, value="HUMAN")
computer_on = tk.BooleanVar(value=True)
game_over = tk.BooleanVar(value=False)
replay_frame_by_frame_on = tk.BooleanVar(value=False)


replay_next_frame_var = tk.BooleanVar(value=False)


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
    overall_estimate.clear()
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
    command=lambda: start_new_game(),
)
new_game_button.grid(row=2, column=0)


def player_win(win_type):
    message = f"{current_player.get()} wins by {win_type}"
    print(message)
    messagebox.showinfo(
        title="game over", message=message
    )
    close_game()


def close_game():
    game_over.set(True)
    print(f"game trajectory {overall_estimate}")
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
    if is_down_diagonal_won(target, row, column):
        win_types.add("down diagonal")
    if len(win_types) > 0:
        player_win(win_type=(" and ".join(win_types)))
        return True
    else:
        return False


def is_down_diagonal_won(target_cell, row, column):
    current_down_diagonal = get_down_diagonal(row, column)
    current_run = 0
    for cell in current_down_diagonal:
        if cell == target_cell:
            current_run += 1
        else:
            current_run = 0
        if current_run >= 4:
            return True
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



# time delay until computer makes a move
COMPUTER_WAIT_TIME = 1


def get_replay_moves():
    with open("replays.txt") as f:
        return [int(i) for i in f.read()]


def replay():
    replay_moves = moves
    replay_button["state"] = "disabled"
    if not game_over.get():
        replay_moves = get_replay_moves()
    start_new_game()
    for button in choices.buttons:
        button["state"] = "disabled"
    computer_on.set(False)
    replay_next_frame_button["state"] = "normal"
    root.update()
    for move in replay_moves:
        root.waitvar(replay_next_frame_var)
        replay_next_frame_var.set(False)
        replay_next_frame_button["state"] = "disabled"
        root.update()
        current_row = current_heights[move]
        labels[current_row][move]["background"] = (
            "red" if current_player.get() == "HUMAN" else "yellow"
        )
        next_player()
        current_heights[move] += 1
        replay_next_frame_button["state"] = "normal"
        root.update()
    replay_button["state"] = "normal"
    replay_next_frame_button["state"] = "disabled"


replay_button = tk.Button(
    master=other_button_frame,
    text="replay mode",
    background="white",
    width=18,
    command=replay,
)
replay_button.grid(row=3, column=0)


replay_next_frame_button = tk.Button(
    master=other_button_frame,
    text="next replay frame",
    background="white",
    width=18,
    state="disabled",
    command=lambda: replay_next_frame_var.set(True),
)
replay_next_frame_button.grid(row=4, column=0)


for i in range(7):
    button = tk.Button(
        master=choice_frame,
        width=5,
        height=2,
        background="white",
        text=i,
        command=lambda this_column=i: make_choice(this_column),
    )
    button.grid(column=i, row=0)
    choices.buttons.append(button)

for i in range(7):
    row = []
    for j in range(7):
        label = tk.Label(
            master=board,
            width=5,
            height=2,
            background="white",
            highlightbackground="black",
            highlightthickness=1,
        )
        label.grid(row=7 - i, column=j, padx=1, pady=1)
        row.append(label)
    labels.append(row)


def computer_choice_clean_up(message, choice):
    print(message)
    root.update()
    time.sleep(COMPUTER_WAIT_TIME)
    make_choice(choice)


def one_step_win_vertical():
    for current_column in range(7):
        if is_column_full(current_column):
            continue
        column_values = []
        for j in range(7):
            column_values.append(theoretical_board[j][current_column])
        current_run = 0
        for j in range(7):
            if column_values[j] == "C":
                current_run += 1
            elif column_values[j] == "H":
                current_run = 0
        if current_run == 3:
            computer_choice_clean_up("one step win vertical", current_column)


def one_step_win_horizontal():
    for current_column in range(7):
        current_column_height = current_heights[current_column]
        if is_column_full(current_column):
            continue
        current_row = theoretical_board[current_column_height]
        current_run = 0
        for i in range(7):
            if current_row[i] == "C" or i == current_column:
                current_run += 1
            else:
                if current_run >= 4:
                    computer_choice_clean_up("one step win horizontal", current_column)
                    return
                else:
                    current_run = 0
        if current_run >= 4:
            computer_choice_clean_up("one step win horizontal end", current_column)
            return


def one_step_up_diagonal_win():
    for current_column in range(7):
        current_column_height = current_heights[current_column]
        if is_column_full(current_column):
            continue
        current_diagonal = get_up_diagonal(current_column_height, current_column)
        position_in_diagonal = min(current_column, current_column_height)
        current_run = 0
        for i0, i in enumerate(current_diagonal):
            if i == "C" or i0 == position_in_diagonal:
                current_run += 1
            else:
                if current_run >= 4:
                    computer_choice_clean_up("one step win up diagonal", current_column)
                    return
                else:
                    current_run = 0
        if current_run >= 4:
            computer_choice_clean_up("one step win up diagonal end", current_column)
            return


def one_step_down_diagonal_win():
    for current_column in range(7):
        current_column_height = current_heights[current_column]
        if is_column_full(current_column):
            continue
        current_diagonal = get_down_diagonal(current_column_height, current_column)[
            ::-1
        ]
        position_in_diagonal = min(current_column, 6 - current_column_height)
        current_run = 0
        for i0, i in enumerate(current_diagonal):
            if i == "C" or i0 == position_in_diagonal:
                current_run += 1
            else:
                if current_run >= 4:
                    computer_choice_clean_up(
                        "one step win down diagonal", current_column
                    )
                    return
                else:
                    current_run = 0
        if current_run >= 4:
            computer_choice_clean_up("one step win down diagonal end", current_column)
            return


def try_block_human_win_vertical(choice_mode=True):
    for column in range(7):
        column_values = [theoretical_board[row][column] for row in range(7)]
        if column_values[-1] == "":
            # column is full so can be skipped
            continue
        if len(column_values) >= 3 and column_values[-3:] == ["H", "H", "H"]:
            if choice_mode:
                computer_choice_clean_up("blocked vertical", column)
            return True
    return False


def try_block_human_horizontal():
    for current_column in range(7):
        current_column_height = current_heights[current_column]
        if is_column_full(current_column):
            continue
        current_row = theoretical_board[current_column_height]

        if is_human_one_away_in_given_sequence(current_row, current_column):
            computer_choice_clean_up("blocked human win horizontal", current_column)
            return True
    return False


def is_human_one_away_in_given_sequence(sequence, skip_column):
    current_run_length = 0
    for value in sequence:
        if value in ("H", skip_column):
            current_run_length += 1
        elif current_run_length >= 4:
            return True
        else:
            current_run_length = 0
    return False


def try_block_up_diagonal():
    for current_column in range(7):
        current_column_height = current_heights[current_column]
        if is_column_full(current_column):
            continue
        current_diagonal = get_up_diagonal(current_column_height, current_column)
        position_in_diagonal = min(current_column, current_column_height)

        if is_human_one_away_in_given_sequence(current_diagonal, position_in_diagonal):
            computer_choice_clean_up("blocked up diagonal", current_column)
            return True
    return False


def try_block_down_diagonal_win():
    for current_column in range(7):
        current_column_height = current_heights[current_column]
        if is_column_full(current_column):
            continue
        current_diagonal = get_down_diagonal(current_column_height, current_column)[
            ::-1
        ]
        position_in_diagonal = min(current_column, 6 - current_column_height)

        if is_human_one_away_in_given_sequence(current_diagonal, position_in_diagonal):
            computer_choice_clean_up("blocked down diagonal", current_column)
            return True
    return False


def try_block_human_win():
    return any(
        [
            try_block_human_win_vertical(),
            try_block_human_horizontal(),
            try_block_up_diagonal(),
            try_block_down_diagonal_win(),
        ]
    )


def disable_choice_button(column):
    if choices.buttons_by_state[column] == "disabled":
        raise Exception(f"button {column} is already disabled")
    choices.buttons[column]["state"] = "disabled"
    choices.buttons_by_state[column] = "disabled"
    choices.buttons[column]["background"] = "gray"
    choices.disabled_buttons += 1
    print(f"there are now {choices.disabled_buttons} disabled buttons")
    if choices.disabled_buttons == 7:
        messagebox.showinfo(title="game over", message="draw - no spaces left")
        close_game()


def estimated_tile_value(column, current_heights=current_heights):
    row = current_heights[column]
    row = 3 - abs(3 - row)
    column = 3 - abs(3 - column)
    m = max(column, row)
    n = min(column, row)
    return {
        (0, 0): 1,  # decreased this value to 2 to reduce going in corners
        (0, 1): 4,
        (0, 2): 5,
        (0, 3): 7,
        (1, 1): 6,
        (1, 2): 8,
        (1, 3): 10,
        (2, 2): 11,
        (2, 3): 13,
        (3, 3): 16,
    }[(n, m)]


def smart_order() -> list:
    start_numbers = list(range(7))
    final_order = []
    for j in range(7):
        values = [estimated_tile_value(i) for i in start_numbers]
        picked = random.randint(1, sum(values))
        values = [sum(values[0 : i + 1]) for i in range(len(values))]
        for i0, i in enumerate(values):
            if i >= picked:
                final_order.append(start_numbers[i0])
                start_numbers.pop(i0)
                break
    return final_order


def arch_sequence(column):
    pattern = [[-1, -1, ""], [0, 1, "H"], [0, 2, "H"], [-1, 3, ""]]
    result = is_pattern_present(column, pattern)
    if result:
        computer_choice_clean_up("blocked arch", column)
    return result


def cross_sequence(column):
    pattern = [[0, -2, "H"], [0, -1, "H"], [-1, 0, "H"], [-2, 0, "H"], [0, 1, ""]]
    result = is_pattern_present(column, pattern)
    if result:
        computer_choice_clean_up("blocked cross", column)
    return result


def turrets_sequence(column):
    row = current_heights[column]
    pattern_present = False
    if row == 0:
        return False
    if 0 <= column <= 3:
        # check right pattern
        if all(
            [
                theoretical_board[row][column + 1] == "H",
                theoretical_board[row - 1][column + 2] == "",
                theoretical_board[row][column + 3] == "H",
            ]
        ):
            pattern_present = True
        if all(
            [
                theoretical_board[row - 1][column + 1] == "",
                theoretical_board[row][column + 2] == "H",
                theoretical_board[row][column + 3] == "H",
            ]
        ):
            pattern_present = True
    if 3 <= column <= 6:
        # check left pattern
        if all(
            [
                theoretical_board[row][column - 1] == "H",
                theoretical_board[row - 1][column - 2] == "",
                theoretical_board[row][column - 3] == "H",
            ]
        ):
            pattern_present = True
        if all(
            [
                theoretical_board[row - 1][column - 1] == "",
                theoretical_board[row][column - 2] == "H",
                theoretical_board[row][column - 3] == "H",
            ]
        ):
            pattern_present = True
    if pattern_present:
        print("blocked turrets")
        root.update()
        time.sleep(COMPUTER_WAIT_TIME)
        make_choice(column)
        return True
    return False


def cliff_sequence(column):
    row = current_heights[column]
    pattern_present = False
    if row == 0:
        return False
    if 2 <= column <= 5:
        # check right pattern
        if all(
            [
                theoretical_board[row][column - 2] == "H",
                theoretical_board[row][column - 1] == "H",
                theoretical_board[row - 1][column + 1] == "H",
            ]
        ):
            pattern_present = True
    if 1 <= column <= 4:
        # check left pattern
        if all(
            [
                theoretical_board[row][column + 2] == "H",
                theoretical_board[row][column + 1] == "H",
                theoretical_board[row - 1][column - 1] == "H",
            ]
        ):
            pattern_present = True
    if pattern_present:
        print("blocked cliff")
        root.update()
        time.sleep(COMPUTER_WAIT_TIME)
        make_choice(column)
        return True
    return False


def slug_sequence(column):
    row = current_heights[column]
    pattern_present = False
    if row > 0:
        return False
    if 3 <= column <= 5:
        # check right pattern
        if all(
            [
                theoretical_board[row][column - 3] == "",
                theoretical_board[row][column - 2] == "H",
                theoretical_board[row][column - 1] == "H",
                theoretical_board[row][column + 1] == "",
            ]
        ):
            pattern_present = True
    if 1 <= column <= 3:
        # check left pattern
        if all(
            [
                theoretical_board[row][column + 3] == "",
                theoretical_board[row][column + 2] == "H",
                theoretical_board[row][column + 1] == "H",
                theoretical_board[row][column - 1] == "",
            ]
        ):
            pattern_present = True
    if 2 <= column <= 4:
        # check left pattern
        if all(
            [
                theoretical_board[row][column - 2] == "",
                theoretical_board[row][column - 1] == "H",
                theoretical_board[row][column + 1] == "H",
                theoretical_board[row][column + 2] == "",
            ]
        ):
            pattern_present = True
    if pattern_present:
        print("blocked slug sequence")
        root.update()
        time.sleep(COMPUTER_WAIT_TIME)
        make_choice(column)
        return True
    return False


def arrowhead_attack(column):
    row = current_heights[column]
    pattern_present = False
    if row < 3:
        return False
    if 0 <= column <= 3:
        # check right pattern
        if all(
            [
                theoretical_board[row - 1][column] == "H",
                theoretical_board[row - 2][column] == "H",
                theoretical_board[row - 1][column + 1] == "H",
                theoretical_board[row - 2][column + 2] == "H",
                theoretical_board[row - 3][column + 3] == "",
            ]
        ):
            pattern_present = True
    if 3 <= column <= 6:
        # check left pattern
        if all(
            [
                theoretical_board[row - 1][column] == "H",
                theoretical_board[row - 2][column] == "H",
                theoretical_board[row - 1][column - 1] == "H",
                theoretical_board[row - 2][column - 2] == "H",
                theoretical_board[row - 3][column - 3] == "",
            ]
        ):
            pattern_present = True
    if pattern_present:
        print("blocked arrowhead attack")
        root.update()
        time.sleep(COMPUTER_WAIT_TIME)
        make_choice(column)
        return True
    return False


def would_allow_arch(column):
    row = current_heights[column]
    pattern_present = False
    if row == 6:
        return False
    if 1 <= column <= 3:
        # check right pattern
        if all(
            [
                theoretical_board[row][column - 1] == "",
                theoretical_board[row + 1][column + 1] == "H",
                theoretical_board[row + 1][column + 2] == "H",
                theoretical_board[row][column + 3] == "",
            ]
        ):
            pattern_present = True
    if 3 <= column <= 5:
        # check left pattern
        if all(
            [
                theoretical_board[row][column + 1] == "",
                theoretical_board[row + 1][column - 1] == "H",
                theoretical_board[row + 1][column - 2] == "H",
                theoretical_board[row][column - 3] == "",
            ]
        ):
            pattern_present = True
    if pattern_present:
        print(f"picking column {column} would allow arch so skipping")
        return True
    return False


def would_allow_turret(column):
    row = current_heights[column]
    pattern_present = False
    if row == 6:
        return False
    if 0 <= column <= 3:
        # check right pattern
        if all(
            [
                theoretical_board[row + 1][column + 1] == "H",
                theoretical_board[row][column + 2] == "",
                theoretical_board[row + 1][column + 3] == "H",
            ]
        ):
            pattern_present = True
        if all(
            [
                theoretical_board[row][column + 1] == "",
                theoretical_board[row + 1][column + 2] == "H",
                theoretical_board[row + 1][column + 3] == "H",
            ]
        ):
            pattern_present = True
    if 1 <= column <= 4:
        if all(
            [
                theoretical_board[row + 1][column - 1] == "H",
                theoretical_board[row][column + 1] == "",
                theoretical_board[row + 1][column + 2] == "H",
            ]
        ):
            pattern_present = True
    if 2 <= column <= 5:
        if all(
            [
                theoretical_board[row + 1][column + 1] == "H",
                theoretical_board[row][column - 1] == "",
                theoretical_board[row + 1][column - 2] == "H",
            ]
        ):
            pattern_present = True
    if 3 <= column <= 6:
        # check left pattern
        if all(
            [
                theoretical_board[row + 1][column - 1] == "H",
                theoretical_board[row][column - 2] == "",
                theoretical_board[row + 1][column - 3] == "H",
            ]
        ):
            pattern_present = True
        if all(
            [
                theoretical_board[row][column - 1] == "",
                theoretical_board[row + 1][column - 2] == "H",
                theoretical_board[row + 1][column - 3] == "H",
            ]
        ):
            pattern_present = True
    if pattern_present:
        print(f"picking column {column} would allow turrets so skipping")
        return True
    return False


def would_allow_cliff(column):
    row = current_heights[column]
    pattern_present = False
    if row == 6:
        return False
    if 1 <= column <= 4:
        # check right pattern
        if all(
            [
                theoretical_board[row][column - 1] == "",
                theoretical_board[row + 1][column + 1] == "H",
                theoretical_board[row + 1][column + 2] == "H",
            ]
        ):
            pattern_present = True
    if 2 <= column <= 5:
        # check left pattern
        if all(
            [
                theoretical_board[row][column + 1] == "",
                theoretical_board[row + 1][column - 1] == "H",
                theoretical_board[row + 1][column - 2] == "H",
            ]
        ):
            pattern_present = True
    if pattern_present:
        print(f"picking column {column} would allow cliff so skipping")
        return True
    return False


def is_pattern_present(
    column,
    pattern,
    theoretical_board=theoretical_board,
    current_heights=current_heights,
):
    row = current_heights[column]
    pattern_rows = [i[0] for i in pattern]
    pattern_columns = [i[1] for i in pattern]
    row_min = 0 - min(pattern_rows)
    row_max = 6 - max(pattern_rows)
    column_min = 0 - min(pattern_columns)
    column_max = 6 - max(pattern_columns)
    if row_min <= row < row_max:
        if column_min <= column <= column_max:
            conditions = [
                theoretical_board[row + i[0]][column + i[1]] == i[2] for i in pattern
            ]
            if all(conditions):
                return True
        if 6 - column_max <= column <= 6 - column_min:
            conditions = [
                theoretical_board[row + i[0]][column - i[1]] == i[2] for i in pattern
            ]
            if all(conditions):
                return True
    return False


def above_cell_causes_human_win(column: int) -> bool:
    row_number_above_cell = current_heights[column] + 1
    if row_number_above_cell >= 7:
        return False

    row_above = theoretical_board[row_number_above_cell]

    up_diagonal_above = get_up_diagonal(row_number_above_cell, column)
    up_diagonal_skip_cell = min(column, row_number_above_cell)
    down_diagonal_above = get_down_diagonal(row_number_above_cell, column)[::-1]
    down_diagonal_skip_cell = min(column, 6 - row_number_above_cell)

    if is_human_one_away_in_given_sequence(row_above, column):
        win_type = "horizontal"

    elif is_human_one_away_in_given_sequence(up_diagonal_above, up_diagonal_skip_cell):
        win_type = "up diagonal"

    elif is_human_one_away_in_given_sequence(down_diagonal_above, down_diagonal_skip_cell):
        win_type = "down diagonal"

    else:
        return False

    print(f"avoiding column {column} to prevent human {win_type} win")
    return True


def try_one_step_win():
    one_step_win_vertical()
    one_step_win_horizontal()
    one_step_up_diagonal_win()
    one_step_down_diagonal_win()


def is_column_full(column):
    return theoretical_board[6][column] != ""


def make_computer_move():
    if not computer_on.get():
        return
    try_one_step_win()
    if game_over.get() or try_block_human_win():
        return

    computer_choice_order = [choice for choice in smart_order() if not is_column_full(choice)]

    for temp_choice in computer_choice_order:
        if not above_cell_causes_human_win(temp_choice):
            if any(
                [
                    arch_sequence(temp_choice),
                    cross_sequence(temp_choice),
                    turrets_sequence(temp_choice),
                    slug_sequence(temp_choice),
                    cliff_sequence(temp_choice),
                    arrowhead_attack(temp_choice),
                ]
            ):
                return
            if is_pattern_present(
                column=temp_choice,
                pattern=[
                    [0, 1, "H"],
                    [0, 2, ""],
                    [0, 3, "H"],
                    [2, 3, "H"],
                    [3, 4, "H"],
                ],
            ):
                computer_choice_clean_up("to avoid dustpan attack", temp_choice)
                return
            if is_pattern_present(
                column=temp_choice,
                pattern=[[-1, -1, "H"], [-1, 1, "H"], [1, -1, "H"], [1, 1, "H"]],
            ):
                computer_choice_clean_up("to avoid x attack", temp_choice)
                return
            arch_1_pattern = [
                [-1, -1, ""],
                [-1, 0, "H"],
                [-2, 0, "H"],
                [0, 1, "H"],
                [-1, 2, "H"],
                [0, 2, ""],
                [-1, 3, ""],
            ]
            if is_pattern_present(column=temp_choice, pattern=arch_1_pattern):
                computer_choice_clean_up("to avoid hidden arch 1 attack", temp_choice)
                return
            if is_pattern_present(
                column=temp_choice,
                pattern=[
                    [-1, -1, ""],
                    [-1, 0, "H"],
                    [-2, 0, "H"],
                    [0, 1, "H"],
                    [-1, 2, "C"],
                    [0, 2, ""],
                    [-1, 3, ""],
                ],
            ):
                computer_choice_clean_up("to avoid hidden arch 2 attack", temp_choice)
                return

    print(f"computer choice order: {computer_choice_order}")
    last_choice = computer_choice_order.pop()

    for computer_choice in computer_choice_order:
        if not should_computer_choice_be_skipped(computer_choice):
            computer_choice_clean_up("which COMPUTER has chosen RANDOMLY", computer_choice)
            return
        print(f"skipping column {computer_choice}")

    computer_choice_clean_up("as no other options available", last_choice)


def should_computer_choice_be_skipped(computer_choice):
    is_first_move_corner_move = len(moves) == 1 and computer_choice in [0, 6]
    patterns = [
        [[0, -1, ""], [1, 1, "H"], [1, 2, "H"]],
        [[0, -3, ""], [1, -2, "H"], [1, -1, "H"]],
        [[0, -2, ""], [1, -1, "H"], [1, 1, "H"]],
        [[1, 1, "H"], [2, 2, "H"], [2, 3, ""]]
    ]
    any_pattern_is_present = any(
        [is_pattern_present(computer_choice, pattern) for pattern in patterns]
    )
    return any([
        is_first_move_corner_move,
        above_cell_causes_human_win(computer_choice),
        any_pattern_is_present,
        would_allow_arch(computer_choice),
        would_allow_turret(computer_choice),
    ])


def get_cells_from_board(cells):
    return [theoretical_board[a][b] for a, b in cells]


def poisoned_rows_total(target_h_copies, target_c_copies):
    res = 0
    runs = []
    for i in range(7):
        for j in range(4):
            board_row = get_cells_from_board(
                ((i, j + k) for k in range(4))
            )
            runs.append(board_row)
    for i in range(4):
        for j in range(7):
            board_column = get_cells_from_board(
                ((i + k, j) for k in range(4))
            )
            runs.append(board_column)
    for i in range(4):
        for j in range(4):
            board_up_diagonal = get_cells_from_board(
                ((i + k, j + k) for k in range(4))
            )
            runs.append(board_up_diagonal)
            board_down_diagonal = get_cells_from_board(
                ((i + k, 6 - j - k) for k in range(4))
            )
            runs.append(board_down_diagonal)
    for run in runs:
        if run.count("H") == target_h_copies and run.count("C") == target_c_copies:
            res += 1
    return res


def make_choice(column):
    if current_player.get() == "HUMAN":
        print("-" * 30)
    print(f"{current_player.get()} has made choice {column}")
    if game_over.get():
        return
    row = current_heights[column]

    label = labels[row][column]
    background = "red" if current_player.get() == "HUMAN" else "yellow"
    label.config(background=background)

    theoretical_board[row][column] = current_player.get()[0]

    if is_column_full(column):
        disable_choice_button(column)
    else:
        current_heights[column] += 1

    moves.append(column)
    check_win(column, row)
    next_player()


def next_player():
    player = current_player.get()
    if player == "HUMAN":
        current_player.set("COMPUTER")
        make_computer_move()
    else:
        current_player.set("HUMAN")
        estimate_current_score()
    root.update()


def estimate_current_score():
    def get_score_estimate(x, y, z):
        return x + 2 * y + 4 * z

    p1, p2, p3 = (poisoned_rows_total(i, 0) for i in (1, 2, 3))
    c1, c2, c3 = (poisoned_rows_total(0, i) for i in (1, 2, 3))

    human_score = get_score_estimate(p1, p2, p3)
    computer_score = get_score_estimate(c1, c2, c3)

    print(
        f"ESTIMATED SCORE: {human_score - computer_score} (H: {human_score}, C: {computer_score})"
    )
    overall_estimate.append(human_score - computer_score)


if __name__ == "__main__":
    root.mainloop()
