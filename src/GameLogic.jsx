export class Game2048 {
  constructor(size = 4) {
    this.size = size;
    this.score = 0;
    this.board = this.createBoard();
    this.initBoard();
  }

  createBoard() {
    return Array.from({ length: this.size }, () => Array(this.size).fill(0));
  }

  highestTile() {
    return Math.max(...this.board.flat());
  }

  possibleNewTiles() {
    const h = this.highestTile();
    if (h < 8) return [2, 4];
    const vals = [];
    for (let v = 2; v < h; v *= 2) vals.push(v);
    return vals;
  }

  filledRatio() {
    const filled = this.board.flat().filter(v => v !== 0).length;
    return filled / (this.size * this.size);
  }

  initBoard() {
    while (true) {
      this.board = this.createBoard();
      const cells = [];
      for (let i = 0; i < this.size; i++)
        for (let j = 0; j < this.size; j++) cells.push([i, j]);
      const fillCount = Math.floor(0.7 * cells.length);
      for (let [r, c] of this.shuffle(cells).slice(0, fillCount))
        this.board[r][c] = [2, 4][Math.floor(Math.random() * 2)];
      if (this.canMove()) break;
    }
  }

  shuffle(arr) {
    return arr.sort(() => Math.random() - 0.5);
  }

  canMove() {
    for (let r = 0; r < this.size; r++) {
      for (let c = 0; c < this.size; c++) {
        const v = this.board[r][c];
        if (v === 0) continue;
        const dirs = [[1,0],[-1,0],[0,1],[0,-1]];
        for (let [dr, dc] of dirs) {
          let nr = r + dr, nc = c + dc;
          while (nr >= 0 && nr < this.size && nc >= 0 && nc < this.size) {
            const nv = this.board[nr][nc];
            if (nv === 0) { nr += dr; nc += dc; continue; }
            if (nv === v) return true;
            break;
          }
        }
      }
    }
    return false;
  }

  moveTile(row, col, dir) {
    const dirs = { up: [-1,0], down: [1,0], left: [0,-1], right: [0,1] };
    const [dr, dc] = dirs[dir];
    const val = this.board[row][col];
    if (!val) return null;
    let nr = row + dr, nc = col + dc;
    while (nr >= 0 && nr < this.size && nc >= 0 && nc < this.size) {
      const neighbor = this.board[nr][nc];
      if (neighbor === 0) { nr += dr; nc += dc; continue; }
      if (neighbor === val) {
        this.board[nr][nc] = val * 2;
        this.board[row][col] = 0;
        this.score += val * 2;
        return [nr, nc];
      }
      break;
    }
    return false;
  }

  addRandomTiles(count = 2) {
    const empty = [];
    for (let i = 0; i < this.size; i++)
      for (let j = 0; j < this.size; j++)
        if (this.board[i][j] === 0) empty.push([i, j]);
    if (!empty.length) return;
    const choices = this.possibleNewTiles();
    for (let k = 0; k < Math.min(count, empty.length); k++) {
      const [r, c] = empty.splice(Math.floor(Math.random() * empty.length), 1)[0];
      this.board[r][c] = choices[Math.floor(Math.random() * choices.length)];
    }
  }
}
