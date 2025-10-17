import React, { useState, useEffect } from "react";
import { Game2048 } from "./GameLogic";
import "./styles.css";

export default function GameBoard() {
  const [game, setGame] = useState(new Game2048());
  const [selected, setSelected] = useState(null);
  const [refresh, setRefresh] = useState(0);
  const [hintTile, setHintTile] = useState(null);
  const [popup, setPopup] = useState(null);

  // Handle arrow key moves
  useEffect(() => {
    const handler = (e) => {
      if (!selected) return;
      const dirMap = {
        ArrowUp: "up",
        ArrowDown: "down",
        ArrowLeft: "left",
        ArrowRight: "right",
      };
      const dir = dirMap[e.key];
      if (dir) {
        const res = game.moveTile(selected[0], selected[1], dir);
        if (res) {
          setSelected(null);
          if (game.filledRatio() < 0.7) game.addRandomTiles();
          if (!game.canMove()) {
            showTemporaryPopup("😢 Game Over - No moves left!");
          }
        }
        setRefresh((x) => x + 1);
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [selected, game]);

  // Hint after 8 seconds
  useEffect(() => {
    const timer = setTimeout(() => showHint(), 8000);
    return () => clearTimeout(timer);
  }, [refresh]);

  // Helper: Show popup for 2 seconds
  const showTemporaryPopup = (message) => {
    setPopup(message);
    setTimeout(() => setPopup(null), 2000);
  };

  const showHint = () => {
    const moves = [];
    for (let r = 0; r < game.size; r++) {
      for (let c = 0; c < game.size; c++) {
        const v = game.board[r][c];
        if (!v) continue;
        const dirs = [
          [1, 0],
          [-1, 0],
          [0, 1],
          [0, -1],
        ];
        for (let [dr, dc] of dirs) {
          let nr = r + dr,
            nc = c + dc;
          while (nr >= 0 && nr < game.size && nc >= 0 && nc < game.size) {
            const nv = game.board[nr][nc];
            if (nv === 0) {
              nr += dr;
              nc += dc;
              continue;
            }
            if (nv === v) moves.push([r, c]);
            break;
          }
        }
      }
    }
    if (moves.length) {
      setHintTile(moves[Math.floor(Math.random() * moves.length)]);
      showTemporaryPopup("💡 Hint: Try the highlighted tile!");
    }
  };

  const tileColor = (val) => {
    const map = {
      0: "#cdc1b4",
      2: "#eee4da",
      4: "#ede0c8",
      8: "#f2b179",
      16: "#f59563",
      32: "#f67c5f",
      64: "#f65e3b",
      128: "#edcf72",
      256: "#edcc61",
      512: "#edc850",
      1024: "#edc53f",
      2048: "#edc22e",
    };
    return map[val] || "#3c3a32";
  };

  const tileTextColor = (val) => (val <= 4 ? "#776e65" : "#f9f6f2");

  return (
    <div className="outer">
      <div className="container">
        <h1>2048 – Single Tile Merge</h1>
        <div className="score">Score: {game.score}</div>
        <div
          className="board"
          style={{ gridTemplateColumns: `repeat(${game.size}, 1fr)` }}
        >
          {game.board.map((row, i) =>
            row.map((val, j) => {
              const key = `${i}-${j}`;
              const isSelected = selected && selected[0] === i && selected[1] === j;
              const isHint = hintTile && hintTile[0] === i && hintTile[1] === j;
              return (
                <div
                  key={key}
                  className={`cell ${isSelected ? "selected" : ""} ${
                    isHint ? "hint" : ""
                  }`}
                  style={{
                    backgroundColor: tileColor(val),
                    color: tileTextColor(val),
                  }}
                  onClick={() => {
                    setSelected([i, j]);
                    setHintTile(null);
                    setPopup(null);
                  }}
                >
                  {val || ""}
                </div>
              );
            })
          )}
        </div>
        <button
          onClick={() => {
            setGame(new Game2048());
            setSelected(null);
            setHintTile(null);
            setPopup(null);
          }}
        >
          Restart
        </button>
      </div>

      {/* Auto disappearing popup */}
      {popup && (
        <div className="popup fade-in">
          <div className="popup-box">
            <p>{popup}</p>
          </div>
        </div>
      )}
    </div>
  );
}
