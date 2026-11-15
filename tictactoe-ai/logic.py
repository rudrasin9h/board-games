import ui
import numpy as np

ini_board = np.zeros((3, 3), dtype=int)
board = ini_board.copy()

winner = None

def update_board(row: int, col: int, player: str) -> bool:
    if board[row, col] != 0 and row in range(3) and col in range(3):
        return False

    board[row, col] = 1 if player == "p1" else -1
    return True

def check_win(arr: np.ndarray) -> str | None:
    lines = list(arr) + list(arr.T)
    lines.extend((np.diag(arr), np.diag(np.fliplr(arr))))

    for line in lines:
        if line[0] != 0 and line[0] == line[1] == line[2]:
            return "Player 1" if line[0] == 1 else "Player 2"

    return None
