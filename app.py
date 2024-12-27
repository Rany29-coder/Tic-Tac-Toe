import time

class TicTacToe:
    def __init__(self, size=4):
        self.size = size
        self.board = [[' ' for _ in range(size)] for _ in range(size)]
        self.memoization = {}
        self.nodes_explored = 0
        

    def display_board(self):
        for row in self.board:
            print('| ' + ' | '.join(row) + ' |')
            print('-' * (self.size * 4 + 1))

    def is_valid_move(self, row, col):
        return 0 <= row < self.size and 0 <= col < self.size and self.board[row][col] == ' '

    def make_move(self, row, col, player):
        if self.is_valid_move(row, col):
            self.board[row][col] = player
            return True
        return False

    def check_win(self, player):
        for i in range(self.size):
            if all(self.board[i][j] == player for j in range(self.size)) or \
               all(self.board[j][i] == player for j in range(self.size)):
                return True

        if all(self.board[i][i] == player for i in range(self.size)) or \
           all(self.board[i][self.size - i - 1] == player for i in range(self.size)):
            return True

        return False

    def check_draw(self):
        return all(self.board[row][col] != ' ' for row in range(self.size) for col in range(self.size))

    def evaluate_board(self):
        score = 0
        for i in range(self.size):
            row = [self.board[i][j] for j in range(self.size)]
            col = [self.board[j][i] for j in range(self.size)]
            score += self.evaluate_line(row)
            score += self.evaluate_line(col)

        diag1 = [self.board[i][i] for i in range(self.size)]
        diag2 = [self.board[i][self.size - i - 1] for i in range(self.size)]
        score += self.evaluate_line(diag1)
        score += self.evaluate_line(diag2)

        return score

    def evaluate_line(self, line):
        x_count = line.count('X')
        o_count = line.count('O')
        if x_count == self.size and o_count == 0:
            return 100
        elif x_count == 0 and o_count == self.size:
            return -100
        return 0

    def get_board_key(self, is_maximizing, depth):
        return ''.join([''.join(row) for row in self.board]) + ('X' if is_maximizing else 'O') + str(depth)

    def minimax(self, is_maximizing, alpha, beta, depth, max_depth=3):
        self.nodes_explored += 1 
        board_key = self.get_board_key(is_maximizing, depth)
        if board_key in self.memoization:
            return self.memoization[board_key]

        if depth == max_depth or self.check_win('X') or self.check_win('O') or self.check_draw():
            score = self.evaluate_board()
            self.memoization[board_key] = score
            return score

        if is_maximizing:
            best_score = float('-inf')
            for row in range(self.size):
                for col in range(self.size):
                    if self.board[row][col] == ' ':
                        self.board[row][col] = 'X'
                        score = self.minimax(False, alpha, beta, depth + 1, max_depth)
                        self.board[row][col] = ' '
                        best_score = max(best_score, score)
                        alpha = max(alpha, best_score)
                        if beta <= alpha:
                            break
            self.memoization[board_key] = best_score
            return best_score
        else:
            best_score = float('inf')
            for row in range(self.size):
                for col in range(self.size):
                    if self.board[row][col] == ' ':
                        self.board[row][col] = 'O'
                        score = self.minimax(True, alpha, beta, depth + 1, max_depth)
                        self.board[row][col] = ' '
                        best_score = min(best_score, score)
                        beta = min(beta, best_score)
                        if beta <= alpha:
                            break
            self.memoization[board_key] = best_score
            return best_score

    def play_game(self):
        # Prompting the player to choose the board size
        while True:
            try:
                size = int(input("Enter the size of the Tic-Tac-Toe board (e.g., 3 for a 3x3 board): "))
                if size < 3:
                    print("The board size must be at least 3.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a numerical value.")
        
        # Initialize the board with the chosen size
        self.__init__(size)
        
        current_player = 'X'  # AI is 'X', player is 'O'
        while True:
            self.display_board()
            if current_player == 'X':
                print("AI's Turn.")
                row, col = self.find_best_move()
            else:
                print("Your Turn. Enter your move as 'row col': ")
                try:
                    row, col = map(int, input().split())
                    row -= 1
                    col -= 1
                    if not self.is_valid_move(row, col):
                        print("Invalid move. Please try again.")
                        continue
                except ValueError:
                    print("Invalid input. Please enter row and column numbers.")
                    continue

            self.make_move(row, col, current_player)
            if self.check_win(current_player):
                self.display_board()
                print(f"{'AI' if current_player == 'X' else 'Player'} wins!")
                break
            elif self.check_draw():
                self.display_board()
                print("It's a draw!")
                break

            current_player = 'O' if current_player == 'X' else 'X'

        if input("Play again? (y/n): ").lower() == 'y':
            self.__init__(self.size)  # Reset the board
            self.play_game()
            
            
    def count_empty_spaces(self):
        return sum(row.count(' ') for row in self.board)

    def find_best_move(self):
        self.nodes_explored = 0  # Reset the counter at the start of the turn
        start_time = time.time()

        # Adjust depth based on the number of empty spaces
        empty_spaces = self.count_empty_spaces()
        if empty_spaces > 6:
            max_depth = 2  # Shallower depth for early game
        elif empty_spaces > 3:
            max_depth = 3  # Medium depth
        else:
            max_depth = 4  # Deeper exploration for late game

        best_score = float('-inf')
        best_move = None

        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == ' ':
                    self.board[row][col] = 'X'
                    score = self.minimax(False, float('-inf'), float('inf'), 0, max_depth)
                    self.board[row][col] = ' '
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)

        end_time = time.time()
        decision_time = end_time - start_time
        print(f"AI Decision Time: {decision_time} seconds")
        print(f"Nodes Explored: {self.nodes_explored}")

        return best_move
# Example usage
if __name__ == '__main__':
    game = TicTacToe()
    game.play_game()