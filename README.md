# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable.

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: _"How do I keep a variable from resetting in Streamlit when I click a button?"_
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] Describe the game's purpose.
- [x] Detail which bugs you found.
- [x] Explain what fixes you applied.

### Game purpose

Glitchy Guesser is a number guessing game built with Streamlit. The game picks a secret number in a range that depends on the difficulty (Easy 1–20, Normal 1–100, Hard 1–50). The player guesses until they find it or run out of attempts. After each guess the game says whether it was too high or too low, and the score changes based on how many attempts it took.

### Bugs found

| # | Bug | Where | Symptom |
|---|-----|-------|---------|
| 1 | Hint messages were swapped | `check_guess` | A guess above the secret said "📈 Go HIGHER!", and a guess below said "📉 Go LOWER!", so following the hints led away from the secret. |
| 2 | Secret turned into a string on even attempts | `app.py` submit handler | `secret = str(st.session_state.secret)` on every 2nd attempt made the comparison alphabetical, so `"9" > "50"` and a guess of 9 was called "Too High". |
| 3 | Original tests compared a tuple to a string | `tests/test_game_logic.py` | `check_guess` returns `(outcome, message)`, but the tests asserted `result == "Win"`, so 3 tests failed even though the logic was right. |
| 4 | "New Game" doesn't fully reset the game | `app.py` New Game button | `status`, `history` and `score` are never reset, so after a win the game stays stuck on "You already won", and the new secret is always 1–100 whatever the difficulty. **Not fixed yet.** |

### Fixes applied

- **Swapped hints:** a too-high guess now returns "📉 Go LOWER!" and a too-low guess returns "📈 Go HIGHER!". The same fix is applied in the `except TypeError` branch.
- **String comparison:** removed the even/odd branch, so the secret always stays an `int` and every comparison is numeric.
- **Refactor:** moved `get_range_for_difficulty`, `parse_guess`, `check_guess` and `update_score` out of `app.py` into `logic_utils.py`. `app.py` now imports them, so the logic can be tested without Streamlit.
- **Tests:** fixed the three original tests to unpack `(outcome, message)`, and added regression and edge-case tests (14 total). Added `pytest.ini` with `pythonpath = .` so the tests can import `logic_utils`.

### Project structure

```
app.py                    # Streamlit UI and session state
logic_utils.py            # Game logic (pure functions, tested)
tests/test_game_logic.py  # pytest suite (14 tests)
pytest.ini                # Lets tests import logic_utils
architecture.mmd          # Mermaid diagram of the app flow
reflection.md             # Reflection on bugs, fixes, and AI use
ai_interactions.md        # Stretch: agent workflow and test generation log
test_results.txt          # Saved pytest output
```

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

A sample game on **Normal** difficulty (range 1–100, 8 attempts), where the secret number is **50**:

1. The user runs `python -m streamlit run app.py`, keeps the default "Normal" difficulty, and opens **Developer Debug Info**. It shows `Secret: 50`, `Score: 0`, and an empty history.
2. The user enters a guess of **40** and clicks **Submit Guess 🚀**.
3. The game returns **"Too Low"** and shows the hint **"📈 Go HIGHER!"**. The score drops by 5 to **-5**.
4. The user enters a guess of **70**, and the game shows **"Too High"** with the hint **"📉 Go LOWER!"**. The score drops by 5 again, to **-10**.
5. Throughout, the secret in Debug Info stays at **50**. It no longer changes on each Submit, and the hints are now based on comparing numbers, never strings.
6. The user enters a guess of **50**. The game shows **"🎉 Correct!"**, balloons appear, and the message reads **"You won! The secret was 50. Final score: 40"**. The win adds 100 − 10 × (attempt number + 1) = 50 points.
7. The game ends. Further guesses show "You already won. Start a new game to play again." The history in Debug Info reads `[40, 70, 50]`.

**Screenshot** _(optional)_: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

Run with `python -m pytest -v` (full output saved in `test_results.txt`):

```
tests/test_game_logic.py::test_winning_guess PASSED
tests/test_game_logic.py::test_guess_too_high PASSED
tests/test_game_logic.py::test_guess_too_low PASSED
tests/test_game_logic.py::test_too_high_hint_says_go_lower PASSED
tests/test_game_logic.py::test_too_low_hint_says_go_higher PASSED
tests/test_game_logic.py::test_single_digit_guess_compared_as_number PASSED
tests/test_game_logic.py::test_boundary_guesses_compare_numerically PASSED
tests/test_game_logic.py::test_parse_guess_valid_integer PASSED
tests/test_game_logic.py::test_parse_guess_decimal_is_truncated PASSED
tests/test_game_logic.py::test_parse_guess_empty_or_missing PASSED
tests/test_game_logic.py::test_parse_guess_not_a_number PASSED
tests/test_game_logic.py::test_range_for_difficulty PASSED
tests/test_game_logic.py::test_score_win_has_minimum_of_10_points PASSED
tests/test_game_logic.py::test_score_too_low_subtracts_5 PASSED

============================== 14 passed in 0.02s ==============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
- [x] **Agent Workflow (SF8):** used Claude Code to diagnose and fix failing tests, run pytest, and draft the docs. See `ai_interactions.md`.
- [x] **Test Generation (SF7):** used AI to help write the regression and edge-case tests. See `ai_interactions.md`.
- [x] **Architecture diagram:** `architecture.mmd` shows how `app.py`, `logic_utils.py`, session state and the tests fit together.
