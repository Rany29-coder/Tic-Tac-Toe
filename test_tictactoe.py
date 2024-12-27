import unittest
from app import TicTacToe

class TestTicTacToe(unittest.TestCase):

    def test_is_valid_move(self):
        game = TicTacToe(3)
        # Test a valid move
        self.assertTrue(game.is_valid_move(0, 0))
        # Test an invalid move (outside the board)
        self.assertFalse(game.is_valid_move(3, 3))
        # Make a move and then test the same spot (should be invalid now)
        game.make_move(0, 0, 'X')
        self.assertFalse(game.is_valid_move(0, 0))
    
    def test_make_move(self):
        game = TicTacToe(3)
        # Test a successful move
        self.assertTrue(game.make_move(1, 1, 'X'))
        self.assertEqual(game.board[1][1], 'X')
        # Test an invalid move
        self.assertFalse(game.make_move(1, 1, 'O'))
        
    def test_check_win(self):
        game = TicTacToe(3)
        # Setup a winning scenario
        for i in range(3):
            game.make_move(i, i, 'X')
        self.assertTrue(game.check_win('X'))
        # Setup a non-winning scenario
        game = TicTacToe(3)
        self.assertFalse(game.check_win('X'))
        
    def test_check_draw(self):
        game = TicTacToe(3)
        moves = ['X', 'O'] * 4 + ['X']
        for i, move in enumerate(moves):
            row, col = divmod(i, 3)
            game.make_move(row, col, move)
        self.assertTrue(game.check_draw())
    def test_evaluate_board_line(self):
        game = TicTacToe(3)
        # Setup a board with a winning line for 'X'
        for i in range(3):
            game.make_move(i, i, 'X')
        self.assertEqual(game.evaluate_board(), 100)
        self.assertEqual(game.evaluate_line(['X', 'X', 'X']), 100)


if __name__ == '__main__':
    unittest.main()




