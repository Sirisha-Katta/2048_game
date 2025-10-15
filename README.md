# 🧩 2048 – Single Tile Merge Game

### Overview

This is a customized version of the 2048 game built using **Python (Tkinter)**.
Unlike the classic version where all tiles move, here you **select one tile** and move it in a direction to merge only if another tile of the same number exists in that line.
The game includes dynamic tile addition, board expansion, hints, and a smooth glow animation for better user experience.

---

### 🎮 How to Play

1. Click on any tile to **select** it.
2. Use your **arrow keys (↑ ↓ ← →)** to move the selected tile.
3. A move is successful only if there is another tile with the **same number** in that direction (it can skip over empty tiles).
4. After merging, new tiles appear only when the board is **less than 70% filled**.
5. If you stay idle for **8 seconds**, the game gives you a **hint** by glowing a tile that has a possible move.
6. The goal is to keep merging and reach **2048**.
7. You can restart the game anytime using the **Restart 🔁 button**.

---

### ⚙️ Features

* **Single tile movement:** You can control one tile at a time.
* **Skip empty cells:** Merging works even if there are empty spaces between tiles.
* **Smart tile generation:** New tiles are added based on your highest tile (for example, if you reach 16, new tiles can be 2, 4, or 8).
* **Dynamic board size:** The board expands automatically as you progress (4x4 → 5x5 → 6x6, etc.).
* **70% fill rule:** New tiles are only added when less than 70% of the board is filled.
* **Hint system:** Shows a valid move after 8 seconds of no action.
* **Smooth glow animation:** The selected or hint tile glows softly (no bright colors).
* **Game over alert:** If no moves are possible, you get a popup message.

---

### 🧠 Design Summary

* The game is designed to make users **stay engaged** rather than lose early.
* It ensures there is always **at least one possible move** at the start.
* The dynamic rules keep gameplay balanced and interesting.
* The UI is kept simple, clean, and similar to the **classic 2048 look**.

---

### 🧩 Controls

| Action      | Description                              |
| ----------- | ---------------------------------------- |
| 🖱️ Click   | Select a tile                            |
| ⬆️ ⬇️ ⬅️ ➡️ | Move selected tile                       |
| 🔁 Restart  | Reset the game                           |
| 💡 Hint     | Shown automatically after 8 seconds idle |

---

### 🧪 How to Run

1. Make sure Python 3 is installed.
2. Install Tkinter if not already installed.

   * On macOS (Homebrew):

     ```bash
     brew install tcl-tk
     ```
3. Run the game:

   ```bash
   python3 main.py
   ```

---

### 📂 File Structure

```
2048_game/
└── main.py
```

---

### 🏁 Summary

A redesigned version of 2048 focused on **strategy, engagement, and simplicity**.
Players merge single tiles instead of shifting the entire grid, with smart tile generation, hints, and a soft glow animation to enhance the experience.
