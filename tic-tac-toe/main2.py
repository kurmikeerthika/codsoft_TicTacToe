import tkinter as tk
from tkinter import messagebox
import random
import math

EMPTY = " "
HUMAN = None
AI = None

def create_board():
    """Create a new empty board"""
    return [EMPTY] * 9

def free_spots(board):
    """Return list of indexes that are still empty"""
    return [i for i, v in enumerate(board) if v == EMPTY]

def get_winner(board):
    """Check all possible winning combinations"""
    win_positions = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]
    for a, b, c in win_positions:
        if board[a] == board[b] == board[c] and board[a] != EMPTY:
            return board[a]
    return None

def is_game_over(board):
    """Return True if game is over (win or draw)"""
    return get_winner(board) is not None or all(cell != EMPTY for cell in board)

def evaluate(board):
    """Return +1 if AI wins, -1 if human wins, 0 for draw"""
    w = get_winner(board)
    if w == AI:
        return 1
    elif w == HUMAN:
        return -1
    return 0

def minimax(board, maximizing, alpha=-math.inf, beta=math.inf):
    if is_game_over(board):
        return evaluate(board), None

    best_move = None
    if maximizing:
        max_eval = -math.inf
        for move in free_spots(board):
            board[move] = AI
            val, _ = minimax(board, False, alpha, beta)
            board[move] = EMPTY
            if val > max_eval:
                max_eval = val
                best_move = move
            alpha = max(alpha, val)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = math.inf
        for move in free_spots(board):
            board[move] = HUMAN
            val, _ = minimax(board, True, alpha, beta)
            board[move] = EMPTY
            if val < min_eval:
                min_eval = val
                best_move = move
            beta = min(beta, val)
            if beta <= alpha:
                break
        return min_eval, best_move

def best_ai_move(board):
    """Choose best move for AI"""
    if board.count(EMPTY) == 9:
        return random.choice([0, 2, 6, 8])
    _, move = minimax(board, True)
    return move


class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.board = create_board()
        self.buttons = []
        self.restart_btn = None

        top = tk.Frame(root)
        top.pack(pady=8)

        tk.Label(top, text="You play as:").pack(side="left")
        self.player_side = tk.StringVar(value="X")
        tk.Radiobutton(top, text="X", variable=self.player_side, value="X").pack(side="left")
        tk.Radiobutton(top, text="O", variable=self.player_side, value="O").pack(side="left")

        tk.Label(top, text="   First move:").pack(side="left", padx=(10,0))
        self.first_turn = tk.StringVar(value="Human")
        tk.Radiobutton(top, text="You", variable=self.first_turn, value="Human").pack(side="left")
        tk.Radiobutton(top, text="AI", variable=self.first_turn, value="AI").pack(side="left")

        tk.Button(top, text="Start Game", command=self.new_game).pack(side="left", padx=10)

        grid = tk.Frame(root)
        grid.pack()

        for i in range(9):
            btn = tk.Button(grid, text=" ", font=("Arial", 28), width=3, height=1,
                            command=lambda i=i: self.player_move(i))
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.buttons.append(btn)

        self.status = tk.Label(root, text="Select options and start the game.", font=("Arial", 11))
        self.status.pack(pady=8)

    def new_game(self):
        """Start or restart a game"""
        global HUMAN, AI
        HUMAN = self.player_side.get()
        AI = "O" if HUMAN == "X" else "X"
        self.board = create_board()

        for b in self.buttons:
            b.config(text=" ", state="normal")

        if self.restart_btn:
            self.restart_btn.destroy()
            self.restart_btn = None

        turn = self.first_turn.get()
        self.status.config(text=f"You: {HUMAN} | AI: {AI} | {turn} starts")

        if turn == "AI":
            self.root.after(300, self.ai_turn)

    def player_move(self, index):
        """Handle player's click"""
        if self.board[index] != EMPTY or is_game_over(self.board):
            return
        self.make_move(index, HUMAN)
        if is_game_over(self.board):
            self.finish()
        else:
            self.root.after(200, self.ai_turn)

    def ai_turn(self):
        """AI makes its move"""
        if is_game_over(self.board):
            self.finish()
            return
        move = best_ai_move(self.board)
        if move is not None:
            self.make_move(move, AI)
        if is_game_over(self.board):
            self.finish()

    def make_move(self, index, player):
        """Mark a move on the board"""
        self.board[index] = player
        self.buttons[index].config(text=player, state="disabled")

    def finish(self):
        """Game over logic"""
        winner = get_winner(self.board)
        for b in self.buttons:
            b.config(state="disabled")

        if winner == HUMAN:
            msg = "You win! 🎉"
        elif winner == AI:
            msg = "AI wins. Try again!"
        else:
            msg = "It's a draw!"

        self.status.config(text=msg)

        if winner is None:
            self.restart_btn = tk.Button(self.root, text="Restart", command=self.new_game,
                                         font=("Arial", 11), bg="#ddd")
            self.restart_btn.pack(pady=5)
        else:
            messagebox.showinfo("Game Over", msg)

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToe(root)
    root.resizable(False, False)
    root.mainloop()
