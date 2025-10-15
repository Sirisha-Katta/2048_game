import tkinter as tk
import random

# ---------------- Core Game Logic ----------------
class Game2048SingleTile:
    def __init__(self, size=4):
        self.size = size
        self.board = [[0]*size for _ in range(size)]
        self.score = 0
        self.initialize_board()

    def initialize_board(self):
        """Fill ~70% of cells and ensure at least one move."""
        while True:
            self.board = [[0]*self.size for _ in range(self.size)]
            cells = [(i, j) for i in range(self.size) for j in range(self.size)]
            fill_count = int(0.7 * len(cells))
            for (i, j) in random.sample(cells, fill_count):
                self.board[i][j] = random.choice([2, 4])
            if self.can_move():
                break

    def highest_tile(self):
        return max(max(row) for row in self.board)

    def possible_new_tiles(self):
        highest = self.highest_tile()
        if highest < 8:
            return [2, 4]
        vals = []
        v = 2
        while v < highest:
            vals.append(v)
            v *= 2
        return vals

    def filled_ratio(self):
        """Return how full the board is (0–1)."""
        total = self.size * self.size
        filled = sum(1 for row in self.board for val in row if val != 0)
        return filled / total

    def add_random_tiles(self, count=2):
        """Add a few tiles after successful merge if needed."""
        empty = [(i, j) for i in range(self.size) for j in range(self.size) if self.board[i][j] == 0]
        if not empty:
            return
        choices = self.possible_new_tiles() or [2, 4]
        for _ in range(min(count, len(empty))):
            i, j = random.choice(empty)
            empty.remove((i, j))
            self.board[i][j] = random.choice(choices)

    def move_tile(self, row, col, direction):
        """Move only if same number exists along direction."""
        if not (0 <= row < self.size and 0 <= col < self.size):
            return False
        current = self.board[row][col]
        if current == 0:
            return None
        dirs = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}
        drow, dcol = dirs[direction]
        nr, nc = row + drow, col + dcol

        while 0 <= nr < self.size and 0 <= nc < self.size:
            neighbor = self.board[nr][nc]
            if neighbor == 0:
                nr += drow
                nc += dcol
                continue
            elif neighbor == current:
                self.board[nr][nc] = current * 2
                self.board[row][col] = 0
                self.score += current * 2
                return (nr, nc)
            else:
                return False
        return False

    def can_move(self):
        """Check if any merges are possible."""
        for i in range(self.size):
            for j in range(self.size):
                val = self.board[i][j]
                if val == 0:
                    continue
                for drow, dcol in [(-1,0),(1,0),(0,-1),(0,1)]:
                    ni, nj = i + drow, j + dcol
                    while 0 <= ni < self.size and 0 <= nj < self.size:
                        nval = self.board[ni][nj]
                        if nval == 0:
                            ni += drow; nj += dcol; continue
                        if nval == val:
                            return True
                        break
        return False

    def maybe_expand_board(self):
        """Increase board size dynamically based on progress."""
        high = self.highest_tile()
        new_size = self.size
        if high >= 64 and self.size < 5:
            new_size = 5
        elif high >= 512 and self.size < 6:
            new_size = 6
        elif high >= 2048 and self.size < 7:
            new_size = 7

        if new_size > self.size:
            old = self.board
            self.size = new_size
            self.board = [[0]*new_size for _ in range(new_size)]
            for i in range(len(old)):
                for j in range(len(old[0])):
                    self.board[i][j] = old[i][j]
            self.add_random_tiles(count=4)


# ---------------- GUI ----------------
class Game2048GUI:
    COLORS = {
        0: ("#cdc1b4", "#776e65"),
        2: ("#eee4da", "#776e65"),
        4: ("#ede0c8", "#776e65"),
        8: ("#f2b179", "#f9f6f2"),
        16: ("#f59563", "#f9f6f2"),
        32: ("#f67c5f", "#f9f6f2"),
        64: ("#f65e3b", "#f9f6f2"),
        128: ("#edcf72", "#f9f6f2"),
        256: ("#edcc61", "#f9f6f2"),
        512: ("#edc850", "#f9f6f2"),
        1024: ("#edc53f", "#f9f6f2"),
        2048: ("#edc22e", "#f9f6f2"),
    }

    def __init__(self, root, size=4):
        self.root = root
        self.root.title("🧩 Strategic 2048 - Smart Merge Edition")
        self.game = Game2048SingleTile(size)
        self.selected = None
        self.hint_timer = None
        self.pulse_active = False
        self.build_UI()
        self.update_board()

        self.root.bind("<Up>", lambda e: self.move("up"))
        self.root.bind("<Down>", lambda e: self.move("down"))
        self.root.bind("<Left>", lambda e: self.move("left"))
        self.root.bind("<Right>", lambda e: self.move("right"))

    def build_UI(self):
        self.frame = tk.Frame(self.root, bg="#bbada0")
        self.frame.pack(padx=10, pady=10)
        top = tk.Frame(self.root, bg="#bbada0")
        top.pack()
        self.score_label = tk.Label(top, text="Score: 0", bg="#bbada0", fg="white", font=("Verdana", 18, "bold"))
        self.score_label.pack(side="left", padx=10)
        tk.Button(top, text="Restart 🔁", bg="#8f7a66", fg="white", font=("Verdana", 14, "bold"), command=self.restart).pack(side="right", padx=10)
        self.cells = []
        self.create_cells()

    def create_cells(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.cells = []
        for i in range(self.game.size):
            row = []
            for j in range(self.game.size):
                cell = tk.Label(self.frame, text="", width=5, height=2, font=("Helvetica", 20, "bold"), borderwidth=2, relief="ridge")
                cell.grid(row=i, column=j, padx=4, pady=4)
                cell.bind("<Button-1>", lambda e, r=i, c=j: self.select_tile(r, c))
                row.append(cell)
            self.cells.append(row)

    def select_tile(self, r, c):
        self.selected = (r, c)
        self.update_board()
        self.start_pulse_animation()
        self.reset_hint_timer()

    def move(self, direction):
        if not self.selected:
            return
        r, c = self.selected
        res = self.game.move_tile(r, c, direction)
        if res:
            self.selected = res
            if self.game.filled_ratio() < 0.7:   # 70% rule
                self.game.add_random_tiles(count=2)
            self.game.maybe_expand_board()
            self.create_cells()
        elif res is False:
            self.show_popup("Move not possible!")
        elif res is None:
            self.show_popup("Please select a tile with a number.")
        
        # ✅ Only update board, don't re-trigger glow here
        self.update_board()
        
        # Reset hint timer only (no glow)
        self.reset_hint_timer()

        # End game check
        if not self.game.can_move():
            self.show_popup("😢 Game Over - No moves left!")


    def update_board(self):
        for i in range(self.game.size):
            for j in range(self.game.size):
                val = self.game.board[i][j]
                bg, fg = self.COLORS.get(val, ("#3c3a32", "#f9f6f2"))
                text = str(val) if val != 0 else ""
                self.cells[i][j].config(text=text, bg=bg, fg=fg)
        self.score_label.config(text=f"Score: {self.game.score}")
        self.root.update_idletasks()

    def restart(self):
        self.game = Game2048SingleTile()
        self.create_cells()
        self.selected = None
        self.update_board()

    def show_popup(self, msg):
        win = tk.Toplevel(self.root)
        win.title("Message")
        tk.Label(win, text=msg, font=("Verdana", 16, "bold")).pack(padx=20, pady=20)
        tk.Button(win, text="OK", command=win.destroy, font=("Verdana", 12)).pack(pady=10)

    # ---------------- Hint System ----------------
    def reset_hint_timer(self):
        if self.hint_timer:
            self.root.after_cancel(self.hint_timer)
        # ⏱ hint after 8 seconds
        self.hint_timer = self.root.after(8000, self.show_hint)

    def show_hint(self):
        moves = []
        for i in range(self.game.size):
            for j in range(self.game.size):
                v = self.game.board[i][j]
                if v == 0:
                    continue
                for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                    ni, nj = i + dr, j + dc
                    while 0 <= ni < self.game.size and 0 <= nj < self.game.size:
                        nv = self.game.board[ni][nj]
                        if nv == 0:
                            ni += dr; nj += dc; continue
                        if nv == v:
                            moves.append((i,j))
                        break
        if moves:
            self.selected = random.choice(moves)
            self.update_board()
            self.start_pulse_animation()
            self.show_popup("💡 Hint: Try the glowing tile!")

    # ---------------- Glowing Animation ----------------
    def start_pulse_animation(self):
        """Soft neutral glow animation on selected tile."""
        if not self.selected:
            return
        r, c = self.selected
        cell = self.cells[r][c]
        base_color = cell.cget("bg")
        self.pulse_active = True

        def pulse(step=0):
            if not self.selected or (r, c) != self.selected:
                self.pulse_active = False
                return
            intensity = abs((step % 30) - 10) / 10
            # Blend between lighter/darker shade of current bg
            factor = 1 + 0.4 * (0.5 - intensity)
            try:
                r_bg = int(base_color[1:3], 16)
                g_bg = int(base_color[3:5], 16)
                b_bg = int(base_color[5:7], 16)
                r_new = min(255, int(r_bg * factor))
                g_new = min(255, int(g_bg * factor))
                b_new = min(255, int(b_bg * factor))
                color = f"#{r_new:02x}{g_new:02x}{b_new:02x}"
            except:
                color = base_color
            cell.config(bg=color)
            self.root.after(100, lambda: pulse(step + 1))

        pulse()

# ---------------- Run ----------------
if __name__ == "__main__":
    root = tk.Tk()
    Game2048GUI(root)
    root.mainloop()
