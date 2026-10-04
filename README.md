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

```
# Paste your pytest output here, e.g.:
# pytest tests/
# ========================= X passed in 0.XXs =========================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
