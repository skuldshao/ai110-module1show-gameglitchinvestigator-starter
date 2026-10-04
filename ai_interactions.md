# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I used Claude Code (an agent inside VS Code) for several multi-step tasks:
1. Show me how to open the "Developer Debug Info" panel so I could see the secret number.
2. Explain why three pytest tests were failing with `assert ('Win', '🎉 Correct!') == 'Win'`, and then fix them.
3. Help me fill in `reflection.md` and write the Demo Walkthrough in `README.md`, based on the bugs and fixes in my code.

**What did the agent do?**

- Searched `app.py` and `README.md` with `grep` to find the `st.expander("Developer Debug Info")` block and the run command (`python -m streamlit run app.py`).
- Read `logic_utils.py` and `tests/test_game_logic.py` and found the cause: `check_guess` returns a tuple `(outcome, message)`, but the tests compared it to a plain string.
- Edited `tests/test_game_logic.py` so the three tests unpack the result (`outcome, _ = check_guess(...)`), then ran `pytest`. It went from **3 failed, 3 passed** to **6 passed**.
- Read my `git diff` to see what I had already fixed (swapped hints, the even-attempt `str(secret)` bug), then drafted answers in `reflection.md` based on those changes.
- Ran a sample game (guesses 40, 70, 50 against secret 50) through my real `check_guess` and `update_score` functions, so the scores in the README walkthrough (-5, -10, 40) are real outputs and not guesses.

**What did you have to verify or fix manually?**

- **Which side to fix:** the agent fixed the *tests* instead of changing `check_guess` to return only a string. I checked this choice myself. `app.py` uses `outcome, message = check_guess(...)`, so changing the function would have broken the game.
- **Placeholders and first-person claims:** the first reflection draft left placeholders for things the agent couldn't know, like my manual browser checks. When it filled those in, I had to review them and make sure they matched what I actually did.
- **File changed under it:** my editor reformatted `reflection.md` on save, so one of the agent's edits failed to match the text. It re-read the file and redid the edit instead of overwriting my version.
- **A bug it flagged but didn't fix:** it pointed out that "New Game" never resets `status`, `history` or `score`, and always picks a secret from 1–100. That bug is still in `app.py` and needs a decision from me.

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| A guess above the secret must say "Go LOWER" (the hints used to be swapped) | "Write a test that proves a too-high guess gives the Go LOWER hint." | `test_too_high_hint_says_go_lower`: `check_guess(60, 50)` → outcome `"Too High"`, `"LOWER" in message` | Yes | Checks both the outcome label and the message text, so it would catch the swapped-hint bug coming back. |
| A guess below the secret must say "Go HIGHER" | "Now the mirror case for a too-low guess." | `test_too_low_hint_says_go_higher`: `check_guess(40, 50)` → `"Too Low"`, `"HIGHER" in message` | Yes | Covers the other half of the swapped-hint bug. |
| Single-digit guess vs. two-digit secret (`"9" > "50"` as strings) | "Write a test for the bug where the secret became a string on even attempts." | `test_single_digit_guess_compared_as_number`: `check_guess(9, 50)` → `"Too Low"`, `"HIGHER" in message` | Yes | 9 vs. 50 is exactly the case where string order and number order disagree, so it's a good regression test. |
| Original tests compared a tuple to a string | "Why does `assert result == "Win"` fail with `('Win', '🎉 Correct!') == 'Win'`?" | Unpack first: `outcome, _ = check_guess(50, 50)`, then `assert outcome == "Win"` (same for Too High / Too Low) | Yes (3 failed → 6 passed) | I accepted fixing the tests rather than the function, because `app.py` needs both return values. |

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

_Not attempted._

**Prompt used:**

```
<!-- Paste the prompt you gave the AI -->
```

**Linting output before:**

```
<!-- Paste relevant linter warnings/errors -->
```

**Changes applied:**

<!-- Describe what you changed based on the AI's suggestions -->

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

_Not attempted._

**Task given to both models:**

<!-- Describe what you asked each model to do -->

| | Model A | Model B |
|-|---------|---------|
| **Model name** | | |
| **Response summary** | | |
| **More Pythonic?** | | |
| **Clearer explanation?** | | |

**Which did you prefer and why?**

<!-- Your conclusion -->
