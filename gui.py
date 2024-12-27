import tkinter as tk
import tkinter.simpledialog
import tkinter.messagebox
import time
from app import TicTacToe  # Ensure this correctly imports your TicTacToe class

class TicTacToeGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic-Tac-Toe")
        self.initialize_game()
        

    def initialize_game(self):
        # Ask for board size
        self.size = self.ask_board_size()
        self.game = TicTacToe(self.size)

        # Frame for the game board
        self.board_frame = tk.Frame(self.window)
        self.board_frame.pack()

        # Initialize buttons for the Tic-Tac-Toe board
        self.buttons = [[None for _ in range(self.size)] for _ in range(self.size)]
        self.create_board()

        # Label for displaying AI thinking time
        self.ai_thinking_label = tk.Label(self.window, text="AI Thinking Time: 0.0s")
        self.ai_thinking_label.pack()

    def ask_board_size(self):
        size = tkinter.simpledialog.askinteger("Board Size",
                                               "Enter the size of the Tic-Tac-Toe board (e.g., 3 for a 3x3 board):",
                                               minvalue=3, maxvalue=10)
        return size if size is not None else 3  # Default to 3x3 if no input

    def create_board(self):
        for row in range(self.size):
            for col in range(self.size):
                button = tk.Button(self.board_frame, text='', font=('normal', 40), height=2, width=5,
                                   command=lambda r=row, c=col: self.on_click(r, c))
                button.grid(row=row, column=col)
                self.buttons[row][col] = button

    def on_click(self, row, col):
        if self.game.make_move(row, col, 'O') and not self.check_game_over():
            self.buttons[row][col].config(text='O', state='disabled')
            self.window.after(100, self.ai_move)  # Short delay before AI move

    def ai_move(self):
        start_time = time.time()
        row, col = self.game.find_best_move()
        end_time = time.time()

        ai_thinking_time = round(end_time - start_time, 2)
        nodes_explored = self.game.nodes_explored  # Get the number of nodes explored

        # Update the AI thinking time label to include nodes explored
        self.ai_thinking_label.config(text=f"AI Thinking Time: {ai_thinking_time}s, Nodes Explored: {nodes_explored}")

        self.game.make_move(row, col, 'X')
        self.buttons[row][col].config(text='X', state='disabled')
        self.check_game_over()

    def check_game_over(self):
        winner = None
        if self.game.check_win('X'):
            winner = 'AI'
        elif self.game.check_win('O'):
            winner = 'Player'
        elif self.game.check_draw():
            winner = 'Draw'

        if winner:
            message = f"{winner} wins!" if winner != 'Draw' else "It's a draw!"
            tk.messagebox.showinfo("Game Over", message)
            self.ask_replay()

    def ask_replay(self):
        answer = tk.messagebox.askyesno("Play Again", "Do you want to play again?")
        if answer:
            self.reset_game()

    def reset_game(self):
        self.board_frame.destroy()
        self.ai_thinking_label.destroy()
        self.initialize_game()

    def start_game(self):
        self.window.mainloop()

# To play the game with a GUI
game_gui = TicTacToeGUI()
game_gui.start_game()
# To play the game with a GUI
game_gui = TicTacToeGUI()
game_gui.start_game()