# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

**Bug Reproduction Log**

Document at least 2 bugs you found. Add rows as needed.

| Input                                               | Expected Behavior                    | Actual Behavior                                                                                                                                       | Console Output / Error                                                   |
| --------------------------------------------------- | ------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| Secret is 50 (from Debug Info), guess `60`          | "Too High" with the hint "Go LOWER!" | Outcome "Too High" but the hint said "📈 Go HIGHER!"                                                                                                  | None. No error, just the wrong hint                                      |
| Secret is 50, guess `40`                            | "Too Low" with the hint "Go HIGHER!" | Outcome "Too Low" but the hint said "📉 Go LOWER!"                                                                                                    | None                                                                     |
| Secret is 50, guess `9` on an even-numbered attempt | "Too Low" / "Go HIGHER!"             | Reported "Too High". On even attempts the secret was turned into the string `"50"`, so `"9" > "50"` was compared alphabetically                       | None. `check_guess` caught the `TypeError` and silently compared strings |
| Win a game, then click "New Game 🔁"                | A fresh game I can play              | Still shows "You already won. Start a new game to play again." The status is never reset, and the new secret is always 1–100, whatever the difficulty | None                                                                     |

The first time I ran the game, it looked normal: a title, a difficulty selector in the sidebar, a text box, and Submit / New Game buttons. Once I opened "Developer Debug Info" and could see the secret, it was obvious the game was unwinnable in practice. The hints pointed me the wrong way, so I kept moving away from the secret. Some guesses got the wrong "Too High" / "Too Low" result depending on which attempt I was on. I also noticed smaller problems: the message always says "Guess a number between 1 and 100" even on Easy (1–20), and Hard uses a smaller range (1–50) than Normal, which makes it easier, not harder.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

**AI tools used:** Claude Code, inside VS Code. I used it to find where things were in the app, to explain test failures, and to help draft the tests and this write-up.

**Correct suggestion: why the first three pytest tests failed.**
After I moved `check_guess` into `logic_utils.py`, `test_winning_guess`, `test_guess_too_high`, and `test_guess_too_low` failed with errors like `assert ('Win', '🎉 Correct!') == 'Win'`. I asked the AI why, and it explained that `check_guess` returns a tuple `(outcome, message)` but those tests compared the whole tuple to a single string, which can never be equal. It suggested unpacking the result in the tests (`outcome, _ = check_guess(50, 50)`) and asserting only on `outcome`. This was correct because the game logic itself was fine. Only the tests were wrong, and `app.py` depends on getting both values back (`outcome, message = check_guess(...)`). I verified it by rerunning `pytest`, which went from 3 failed / 3 passed to 6 passed (see section 3).

**Suggestion I did not accept as written: the AI's string-secret code.**

- _What the AI suggested:_ The original AI-written `app.py` converted the secret to a string on every even attempt (`secret = str(st.session_state.secret)`). It then relied on a `try/except TypeError` fallback inside `check_guess` to compare the guess as a string.
- _Why I rejected or changed it:_ It was wrong as well as harder to read. Comparing strings is alphabetical, so `"9" > "50"` is `True`, and a guess of 9 was called "Too High" even though 9 is below 50. One option was to make `check_guess` smarter about handling strings, but that would have added more complexity to hide a problem that shouldn't exist.
- _What I did instead and how I verified it:_ I removed the even/odd branch in `app.py`, so the secret is always an `int` and the comparison is always numeric. I verified it with a new test, `test_single_digit_guess_compared_as_number`, which checks that `check_guess(9, 50)` returns "Too Low" with a "HIGHER" hint. I also checked it by guessing a single-digit number on an even attempt in the game.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I counted a bug as fixed only when two things were true: a pytest test that targets that bug passed, and the game behaved correctly when I played it in the browser. I used the "Developer Debug Info" expander to see the secret, so I could choose guesses whose correct hint I already knew.

**pytest evidence**

| Test                                                              | Bug it covers                                                                                                             | Result |
| ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- | ------ |
| `test_too_high_hint_says_go_lower`                                | Hints were swapped: a guess that was too high said "Go HIGHER!"                                                           | Pass   |
| `test_too_low_hint_says_go_higher`                                | Hints were swapped: a guess that was too low said "Go LOWER!"                                                             | Pass   |
| `test_single_digit_guess_compared_as_number`                      | The secret became a string on even attempts, so `"9" > "50"` was compared alphabetically and 9 was reported as "Too High" | Pass   |
| `test_winning_guess`, `test_guess_too_high`, `test_guess_too_low` | Outcome labels are correct (the tests now unpack the `(outcome, message)` tuple)                                          | Pass   |

Before I fixed the tests, `pytest` printed:

```
FAILED tests/test_game_logic.py::test_winning_guess - AssertionError: assert ('Win', '🎉 Correct!') == 'Win'
FAILED tests/test_game_logic.py::test_guess_too_high - AssertionError: assert ('Too High', '📉 Go LOWER!') == 'Too High'
FAILED tests/test_game_logic.py::test_guess_too_low - AssertionError: assert ('Too Low', '📈 Go HIGHER!') == 'Too Low'
3 failed, 3 passed
```

After I changed those tests to unpack the tuple:

```
6 passed
```

This showed me that a failing test doesn't always mean the code is broken. Here the test was wrong about what the function returns. The AI helped me read the assertion message: the left side was a tuple and the right side was a string, which pointed straight to the cause.

**Manual check in the game:** I ran `python -m streamlit run app.py` and opened "Developer Debug Info" to see the secret. I guessed above it and got "Go LOWER!", then guessed below it and got "Go HIGHER!". On an even-numbered attempt I tried a single-digit guess to confirm the hint was still correct. Finally I typed the secret and won with balloons. While I clicked Submit, the secret in Debug Info stayed the same, which confirmed that session state was holding it between reruns.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Streamlit runs your entire Python script from top to bottom every time you interact with the page, for example by clicking a button or typing in a box. That is a "rerun". Any normal variable is therefore recreated from scratch on every click. If you wrote `secret = random.randint(1, 100)` at the top, you'd get a new secret every time you pressed Submit. `st.session_state` is like a small dictionary that survives reruns, so the app only creates the secret when it isn't already there (`if "secret" not in st.session_state`) and reuses it afterwards. The general rule I took away is that anything the game needs to "remember" (the secret, attempts, score, history, win/lose status) has to live in session state. Anything that has to change when a new game starts must be reset there explicitly.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

**A habit I want to keep:** write a small, specific pytest test for each bug before calling it fixed, and name the test after the bug (like `test_too_high_hint_says_go_lower`). I also want to keep using the debug panel, or print statements, to see the real state, so I'm checking facts and not guessing.

**What I'd do differently:** I'd ask the AI to explain what a piece of code or a failing test is doing before accepting a fix. The tuple-vs-string test failure taught me that the "obvious" fix (changing the function so the test passes) would have broken `app.py`. Next time I'll also make smaller commits after each fix, so it's easier to see what changed and to undo it if needed.

**How this project changed my thinking:** AI-generated code can look clean and still be subtly wrong, like the hidden `str()` conversion that only happened on even attempts. I now treat AI code as a first draft that I have to read, test, and verify myself, not as something that's correct because it runs.
