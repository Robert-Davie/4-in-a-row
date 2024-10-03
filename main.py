from check_win import *
import random
import time
import tkinter as tk


computer_wait_time = 1
replay_next_frame_var = tk.BooleanVar(value=False)


def replay():
    replay_moves = moves
    replay_button["state"] = "disabled"
    if not game_over.get():
        with open("replays.txt") as f:
            replay_moves = [int(i) for i in f.read()]
    start_new_game()
    for i in choices.buttons:
        i["state"] = "disabled"
    computer_on.set(False)
    replay_next_frame_button["state"] = "normal"
    root.update()
    for i in replay_moves:
        root.waitvar(replay_next_frame_var)
        replay_next_frame_var.set(False)
        replay_next_frame_button["state"] = "disabled"
        root.update()
        current_row = current_heights[i]
        if current_player.get() == "HUMAN":
            labels[current_row][i]["background"] = "red"
        else:
            labels[current_row][i]["background"] = "yellow"
        next_player(current_player)
        current_heights[i] += 1
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


def one_step_win_vertical():
    for i in range(7):
        if theoretical_board[6][i] != "":
            continue
        column_values = []
        for j in range(7):
            column_values.append(theoretical_board[j][i])
        current_run = 0
        for j in range(7):
            if column_values[j] == "C":
                current_run += 1
            elif column_values[j] == "H":
                current_run = 0
        if current_run == 3:
            print("one step win vertical")
            root.update()
            time.sleep(computer_wait_time)
            make_choice(i)


def one_step_win_horizontal():
    for current_column in range(7):
        current_column_height = current_heights[current_column]
        if current_column_height >= 6:
            continue
        current_row = theoretical_board[current_column_height]
        current_run = 0
        for i in range(7):
            if current_row[i] == "C" or i == current_column:
                current_run += 1
            else:
                if current_run >= 4:
                    print("one step win horizontal")
                    root.update()
                    time.sleep(computer_wait_time)
                    make_choice(current_column)
                    return
                else:
                    current_run = 0
        if current_run >= 4:
            print("one step win horizontal end")
            root.update()
            time.sleep(computer_wait_time)
            make_choice(current_column)
            return


def one_step_up_diagonal_win():
    for current_column in range(7):
        current_column_height = current_heights[current_column]
        if current_column_height >= 6:
            continue
        current_diagonal = get_up_diagonal(current_column_height, current_column)
        position_in_diagonal = min(current_column, current_column_height)
        current_run = 0
        for i0, i in enumerate(current_diagonal):
            if i == "C" or i0 == position_in_diagonal:
                current_run += 1
            else:
                if current_run >= 4:
                    print("one step win up diagonal")
                    root.update()
                    time.sleep(computer_wait_time)
                    make_choice(current_column)
                    return
                else:
                    current_run = 0
        if current_run >= 4:
            print("one step win up diagonal end")
            root.update()
            time.sleep(computer_wait_time)
            make_choice(current_column)
            return


def one_step_down_diagonal_win():
    for current_column in range(7):
        current_column_height = current_heights[current_column]
        if current_column_height >= 6:
            continue
        current_diagonal = get_down_diagonal(current_column_height, current_column)[
            ::-1
        ]
        position_in_diagonal = min(current_column, 6-current_column_height)
        current_run = 0
        for i0, i in enumerate(current_diagonal):
            if i == "C" or i0 == position_in_diagonal:
                current_run += 1
            else:
                if current_run >= 4:
                    print("one step win down diagonal")
                    root.update()
                    time.sleep(computer_wait_time)
                    make_choice(current_column)
                    return
                else:
                    current_run = 0
        if current_run >= 4:
            print("one step win down diagonal end")
            root.update()
            time.sleep(computer_wait_time)
            make_choice(current_column)
            return


def try_one_step_win():
    one_step_win_vertical()
    one_step_win_horizontal()
    one_step_up_diagonal_win()
    one_step_down_diagonal_win()


def try_block_human_win_vertical(choice_mode=True):
    for i in range(7):
        if theoretical_board[6][i] != "":
            continue
        column_values = []
        for j in range(7):
            column_values.append(theoretical_board[j][i])
        current_run = 0
        for j in range(7):
            if column_values[j] == "H":
                current_run += 1
            elif column_values[j] == "C":
                current_run = 0
        if current_run == 3:
            if choice_mode:
                print("blocked vertical")
                root.update()
                time.sleep(computer_wait_time)
                make_choice(i)
            return True
    return False


def try_block_human_horizontal():
    for current_column in range(7):
        current_column_height = current_heights[current_column]
        if current_column_height >= 6:
            continue
        current_row = theoretical_board[current_column_height]

        if longest_human_one_away(current_row, current_column):
            print("blocked human win horizontal")
            root.update()
            time.sleep(computer_wait_time)
            make_choice(current_column)
            return True
    return False


def longest_human_one_away(sequence, skip_column):
    current_run = 0
    for i0, i in enumerate(sequence):
        if i == "H" or i0 == skip_column:
            current_run += 1
        else:
            if current_run >= 4:
                return True
            else:
                current_run = 0
    if current_run >= 4:
        return True
    else:
        return False


def try_block_up_diagonal():
    for current_column in range(7):
        current_column_height = current_heights[current_column]
        if current_column_height >= 6:
            continue
        current_diagonal = get_up_diagonal(current_column_height, current_column)
        position_in_diagonal = min(current_column, current_column_height)

        if longest_human_one_away(current_diagonal, position_in_diagonal):
            print("blocked up diagonal")
            root.update()
            time.sleep(computer_wait_time)
            make_choice(current_column)
            return True
    return False


def try_block_down_diagonal_win():
    for current_column in range(7):

        current_column_height = current_heights[current_column]
        if current_column_height >= 6:
            continue
        current_diagonal = get_down_diagonal(current_column_height, current_column)[
            ::-1
        ]
        position_in_diagonal = min(current_column, 6 - current_column_height)

        if longest_human_one_away(current_diagonal, position_in_diagonal):
            print("blocked down diagonal")
            root.update()
            time.sleep(computer_wait_time)
            make_choice(current_column)
            return True
    return False


def try_block_human_win():
    if try_block_human_win_vertical():
        return True
    if try_block_human_horizontal():
        return True
    if try_block_up_diagonal():
        return True
    if try_block_down_diagonal_win():
        return True
    return False


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


def estimated_tile_value(column):
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


def smart_order():
    start_numbers = [0, 1, 2, 3, 4, 5, 6]
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
    row = current_heights[column]
    arch_present = False
    if row == 0:
        return False
    if 1 <= column <= 3:
        # check right arch
        if all(
            [
                theoretical_board[row - 1][column - 1] == "",
                theoretical_board[row][column + 1] == "H",
                theoretical_board[row][column + 2] == "H",
                theoretical_board[row - 1][column + 3] == "",
            ]
        ):
            arch_present = True
    if 3 <= column <= 5:
        # check left arch
        if all(
            [
                theoretical_board[row - 1][column + 1] == "",
                theoretical_board[row][column - 1] == "H",
                theoretical_board[row][column - 2] == "H",
                theoretical_board[row - 1][column - 3] == "",
            ]
        ):
            arch_present = True
    if arch_present:
        print("blocked arch")
        root.update()
        time.sleep(computer_wait_time)
        make_choice(column)
        return True
    return False


def cross_sequence(column):
    row = current_heights[column]
    cross_present = False
    if row < 2:
        return False
    if 2 <= column <= 5:
        # check right cross
        if all(
            [
                theoretical_board[row][column - 2] == "H",
                theoretical_board[row][column - 1] == "H",
                theoretical_board[row - 1][column] == "H",
                theoretical_board[row - 2][column] == "H",
                theoretical_board[row][column + 1] == "",
            ]
        ):
            cross_present = True
    if 1 <= column <= 4:
        # check left cross
        if all(
            [
                theoretical_board[row][column + 2] == "H",
                theoretical_board[row][column + 1] == "H",
                theoretical_board[row - 1][column] == "H",
                theoretical_board[row - 2][column] == "H",
                theoretical_board[row][column - 1] == "",
            ]
        ):
            cross_present = True
    if cross_present:
        print("blocked cross")
        root.update()
        time.sleep(computer_wait_time)
        make_choice(column)
        return True
    return False


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
        time.sleep(computer_wait_time)
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
        time.sleep(computer_wait_time)
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
        time.sleep(computer_wait_time)
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
        time.sleep(computer_wait_time)
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

def is_pattern_present(column, column_min, column_max, row_min, row_max, pattern):
    row = current_heights[column]
    pattern_present = False
    if row_min <= row < row_max:
        if column_min <= column <= column_max:
            if all(
                [theoretical_board[row + i[0]][column + i[1]] == i[2] for i in pattern]
            ):
                pattern_present = True
        if 6 - column_max <= column <= 6 - column_min:
            if all(
                [theoretical_board[row + i[0]][column - i[1]] == i[2] for i in pattern]
            ):
                pattern_present = True
    if pattern_present:
        return True
    return False


def is_pattern_present_simple(column, pattern):
    row = current_heights[column]
    pattern_rows = [i[0] for i in pattern]
    pattern_columns = [i[1] for i in pattern]
    row_min = 0 - min(pattern_rows)
    row_max = 6 - max(pattern_rows)
    column_min = 0 - min(pattern_columns)
    column_max = 6 - max(pattern_columns)
    pattern_present = False
    if row_min <= row < row_max:
        if column_min <= column <= column_max:
            if all(
                [theoretical_board[row + i[0]][column + i[1]] == i[2] for i in pattern]
            ):
                pattern_present = True
        if 6 - column_max <= column <= 6 - column_min:
            if all(
                [theoretical_board[row + i[0]][column - i[1]] == i[2] for i in pattern]
            ):
                pattern_present = True
    if pattern_present:
        return True
    return False


def above_cell_causes_human_win(column):
    row_number_above_cell = current_heights[column] + 1
    win_type = ""
    if row_number_above_cell >= 7:
        return False

    row_above = theoretical_board[row_number_above_cell]
    up_diagonal_above = get_up_diagonal(
        row_number_above_cell, column
    )
    down_diagonal_above = get_down_diagonal(
        row_number_above_cell, column
    )[::-1]

    if longest_human_one_away(row_above, column):
        win_type = "horizontal"
    up_diagonal_skip_cell = min(column, row_number_above_cell)
    if longest_human_one_away(up_diagonal_above, up_diagonal_skip_cell):
        win_type = "up diagonal"
    down_diagonal_skip_cell = min(column, 6-row_number_above_cell)
    if longest_human_one_away(down_diagonal_above, down_diagonal_skip_cell):
        win_type = "down diagonal"
    if win_type == "":
        return False
    else:
        print(f"avoiding column {column} to prevent human {win_type} win")
        return True


def pre_make_choice(this_choice, message):
    print(f"choosing column {this_choice} {message}")
    root.update()
    time.sleep(computer_wait_time)
    make_choice(this_choice)


def make_computer_move():
    try_one_step_win()
    if game_over.get():
        return
    if try_block_human_win():
        return
    computer_choice_order = smart_order()
    to_remove = []
    for k in computer_choice_order:
        if choices.buttons_by_state[k] == "disabled":
            to_remove.append(k)
    computer_choice_order = [i for i in computer_choice_order if i not in to_remove]
    for temp_choice in computer_choice_order:
        if not above_cell_causes_human_win(temp_choice):
            if arch_sequence(temp_choice):
                return
            if cross_sequence(temp_choice):
                return
            if turrets_sequence(temp_choice):
                return
            if slug_sequence(temp_choice):
                return
            if cliff_sequence(temp_choice):
                return
            if arrowhead_attack(temp_choice):
                return
            if is_pattern_present_simple(
                column=temp_choice,
                pattern=[[0, 1, "H"], [0, 2, ""], [0, 3, "H"], [2, 3, "H"], [3, 4, "H"]]
            ):
                pre_make_choice(temp_choice, message="to avoid dustpan attack")
                return
            if is_pattern_present_simple(
                column=temp_choice,
                pattern=[[-1, -1, "H"], [-1, 1, "H"], [1, -1, "H"], [1, 1, "H"]]
            ):
                pre_make_choice(temp_choice, message="to avoid x attack")
                return
            if is_pattern_present_simple(
                column=temp_choice,
                pattern=[[-1, -1, ""], [-1, 0, "H"], [-2, 0, "H"], [0, 1, "H"], [-1, 2, "H"], [0, 2, ""], [-1, 3, ""]]
            ):
                pre_make_choice(temp_choice, message="to avoid hidden arch 1 attack")
                return
            if is_pattern_present_simple(
                column=temp_choice,
                pattern=[[-1, -1, ""], [-1, 0, "H"], [-2, 0, "H"], [0, 1, "H"], [-1, 2, "C"], [0, 2, ""], [-1, 3, ""]]
            ):
                pre_make_choice(temp_choice, message="to avoid hidden arch 2 attack")
                return
    last_choice = computer_choice_order[-1]
    while len(computer_choice_order) > 1:
        if above_cell_causes_human_win(last_choice):
            computer_choice_order.pop()
            last_choice = computer_choice_order[-1]
        else:
            break
    print(computer_choice_order, "computer choice order...")

    for computer_choice in computer_choice_order:
        if computer_choice == last_choice:
            pre_make_choice(computer_choice, "as no other options available")
            break

        if len(moves) == 1 and computer_choice in [0, 6]:
            print("avoiding corner move as first COMPUTER move")
            continue

        if above_cell_causes_human_win(computer_choice):
            continue

        if is_pattern_present_simple(
            column=computer_choice,
            pattern=[[0, -1, ""], [1, 1, "H"], [1, 2, "H"]]
        ):
            print(f"skipping column {computer_choice} as would allow cliff")
            continue
        if is_pattern_present_simple(
            column=computer_choice,
            pattern=[[0, -3, ""], [1, -2, "H"], [1, -1, "H"]]
        ):
            print(f"skipping column {computer_choice} as would allow cliff")
            continue
        if is_pattern_present_simple(
            column=computer_choice,
            pattern=[[0, -2, ""], [1, -1, "H"], [1, 1, "H"]]
        ):
            print(f"skipping column {computer_choice} as would allow cliff")
            continue
        if is_pattern_present_simple(
            column=computer_choice,
            pattern=[[1, 1, "H"], [2, 2, "H"], [2, 3, ""]]
        ):
            print(f"skipping column {computer_choice} as would allow spear")
            continue
        if would_allow_arch(computer_choice):
            continue
        if would_allow_turret(computer_choice):
            continue

        pre_make_choice(computer_choice, "which COMPUTER has chosen RANDOMLY")
        break


def poisoned_rows_total(copies_h, copies_c):
    res = 0
    for i in range(7):
        for j in range(4):
            board_row = [
                theoretical_board[i][j],
                theoretical_board[i][j + 1],
                theoretical_board[i][j + 2],
                theoretical_board[i][j + 3],
            ]
            if board_row.count("H") == copies_h and board_row.count("C") == copies_c:
                res += 1
    for i in range(4):
        for j in range(7):
            board_column = [
                theoretical_board[i][j],
                theoretical_board[i + 1][j],
                theoretical_board[i + 2][j],
                theoretical_board[i + 3][j],
            ]
            if board_column.count("H") == copies_h and board_column.count("C") == copies_c:
                res += 1
    for i in range(4):
        for j in range(4):
            board_up_diagonal = [
                theoretical_board[i][j],
                theoretical_board[i + 1][j + 1],
                theoretical_board[i + 2][j + 2],
                theoretical_board[i + 3][j + 3],
            ]
            if board_up_diagonal.count("H") == copies_h and board_up_diagonal.count("C") == copies_c:
                res += 1
    for i in range(4):
        for j in range(4):
            board_down_diagonal = [
                theoretical_board[i][6 - j],
                theoretical_board[i + 1][5 - j],
                theoretical_board[i + 2][4 - j],
                theoretical_board[i + 3][3 - j],
            ]
            if board_down_diagonal.count("H") == copies_h and board_down_diagonal.count("C") == copies_c:
                res += 1
    return res


def make_choice(column):
    if current_player.get() == "HUMAN":
        print("----- ----- ----- ----- -----")
    print(f"{current_player.get()} has made choice {column}")
    if game_over.get():
        return
    row = current_heights[column]
    label = labels[row][column]
    theoretical_board[row][column] = current_player.get()[0]
    if current_player.get() == "HUMAN":
        colour = "red"
    else:
        colour = "yellow"
    label.config(background=colour)
    if current_heights[column] == 6:
        disable_choice_button(column)
    else:
        current_heights[column] += 1

    moves.append(column)
    check_win(column, row)
    next_player(current_player)
    root.update()


def next_player(current_player):
    if current_player.get() == "HUMAN":
        current_player.set("COMPUTER")
        if computer_on.get():
            make_computer_move()
    else:
        current_player.set("HUMAN")
        p1, p2, p3 = poisoned_rows_total(1, 0), poisoned_rows_total(2, 0), poisoned_rows_total(3, 0)
        p4, p5, p6 = poisoned_rows_total(0, 1), poisoned_rows_total(0, 2), poisoned_rows_total(0, 3)
        print(f"HUMAN {p1} {p2} {p3} tot={p1 + p2 * 2 + p3 * 4}")
        print(f"COMPUTER {p4} {p5} {p6} tot={p4 + p5 * 2 + p6 * 4}")
        current_estimate_score = (p1 + p2 * 2 + p3 * 4) - (p4 + p5 * 2 + p6 * 4)
        print(f"overall = {current_estimate_score}")
        overall_estimate.append(current_estimate_score)

root.mainloop()
