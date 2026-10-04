from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


def test_too_high_hint_says_go_lower():
    # Bug fix: a guess above the secret used to say "Go HIGHER!"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message


def test_too_low_hint_says_go_higher():
    # Bug fix: a guess below the secret used to say "Go LOWER!"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message


def test_single_digit_guess_compared_as_number():
    # Bug fix: the secret used to become a string on even attempts, so "9" > "50"
    # alphabetically and 9 was reported as "Too High". Numbers must compare numerically.
    outcome, message = check_guess(9, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message

def test_boundary_guesses_compare_numerically():
    # Edge of the range: 1 vs 100 and 100 vs 99 must use number order, not string order
    assert check_guess(1, 100)[0] == "Too Low"
    assert check_guess(100, 99)[0] == "Too High"
    assert check_guess(10, 9)[0] == "Too High"

def test_parse_guess_valid_integer():
    assert parse_guess("42") == (True, 42, None)

def test_parse_guess_decimal_is_truncated():
    ok, value, err = parse_guess("3.7")
    assert ok and value == 3 and err is None

def test_parse_guess_empty_or_missing():
    assert parse_guess("") == (False, None, "Enter a guess.")
    assert parse_guess(None) == (False, None, "Enter a guess.")

def test_parse_guess_not_a_number():
    assert parse_guess("abc") == (False, None, "That is not a number.")

def test_range_for_difficulty():
    assert get_range_for_difficulty("Easy") == (1, 20)
    assert get_range_for_difficulty("Normal") == (1, 100)
    assert get_range_for_difficulty("Unknown") == (1, 100)

def test_score_win_has_minimum_of_10_points():
    # A very late win would compute negative points; it must be floored at 10
    assert update_score(0, "Win", 20) == 10

def test_score_too_low_subtracts_5():
    assert update_score(10, "Too Low", 3) == 5
