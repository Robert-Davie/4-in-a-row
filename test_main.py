import main


def test_is_pattern_present():
    theoretical_board = [
        ["", "", "", "H", "C", "", "H"],
        ["", "", "", "", "C", "", ""],
        ["", "", "", "", "", "", ""],
        ["", "", "", "", "", "", ""],
        ["", "", "", "", "", "", ""],
        ["", "", "", "", "", "", ""],
        ["", "", "", "", "", "", ""],
    ]
    current_heights = [0, 0, 0, 1, 2, 0, 1]
    result = main.is_pattern_present(
        6, [[0, -2, "C"]], theoretical_board, current_heights
    )
    assert result


def test_estimated_tile_value():
    current_heights = [0, 2, 0, 0, 0, 0, 0]
    result = main.estimated_tile_value(1, current_heights)
    assert result == 8


def test_is_human_one_away_in_given_sequence():
    sequence = ["", "H", "H", "H", "", "", ""]
    assert main.is_human_one_away_in_given_sequence(sequence, 4)