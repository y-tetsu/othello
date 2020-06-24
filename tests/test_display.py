"""Tests of display.py
"""

import unittest
from test.support import captured_stdout

from reversi.board import Board
from reversi.player import Player
from reversi.display import ConsoleDisplay
from reversi.strategies import ConsoleUserInput


class TestDisplay(unittest.TestCase):
    """display
    """
    def test_console_progress(self):
        board8x8 = Board()

        class Test():
            def next_move(self, disc, board):
                return (3, 2)

        black_player = Player('black', 'Test', Test())
        white_player = Player('white', 'User', ConsoleUserInput())

        display = ConsoleDisplay()

        with captured_stdout() as stdout:
            display.progress(board8x8, black_player, white_player)
            legal_moves = board8x8.get_legal_moves('black')
            display.turn(black_player, legal_moves)
            black_player.put_disc(board8x8)
            display.move(black_player, legal_moves)
            display.progress(board8x8, black_player, white_player)
            display.foul(black_player)
            display.win(black_player)
            display.draw()

            lines = stdout.getvalue().splitlines()
            self.assertEqual(lines[0], "〇Test:2 ●User:2")
            self.assertEqual(lines[1], "   a b c d e f g h")
            self.assertEqual(lines[2], " 1□□□□□□□□")
            self.assertEqual(lines[3], " 2□□□□□□□□")
            self.assertEqual(lines[4], " 3□□□□□□□□")
            self.assertEqual(lines[5], " 4□□□●〇□□□")
            self.assertEqual(lines[6], " 5□□□〇●□□□")
            self.assertEqual(lines[7], " 6□□□□□□□□")
            self.assertEqual(lines[8], " 7□□□□□□□□")
            self.assertEqual(lines[9], " 8□□□□□□□□")
            self.assertEqual(lines[10], "")
            self.assertEqual(lines[11], "〇Test's turn")
            self.assertEqual(lines[12], " 1: ('d', '3')")
            self.assertEqual(lines[13], " 2: ('c', '4')")
            self.assertEqual(lines[14], " 3: ('f', '5')")
            self.assertEqual(lines[15], " 4: ('e', '6')")
            self.assertEqual(lines[16], "putted on ('d', '3') ")
            self.assertEqual(lines[17], "")
            self.assertEqual(lines[18], "〇Test:4 ●User:1")
            self.assertEqual(lines[19], "   a b c d e f g h")
            self.assertEqual(lines[20], " 1□□□□□□□□")
            self.assertEqual(lines[21], " 2□□□□□□□□")
            self.assertEqual(lines[22], " 3□□□〇□□□□")
            self.assertEqual(lines[23], " 4□□□〇〇□□□")
            self.assertEqual(lines[24], " 5□□□〇●□□□")
            self.assertEqual(lines[25], " 6□□□□□□□□")
            self.assertEqual(lines[26], " 7□□□□□□□□")
            self.assertEqual(lines[27], " 8□□□□□□□□")
            self.assertEqual(lines[28], "")
            self.assertEqual(lines[29], "〇Test foul")
            self.assertEqual(lines[30], "〇Test win")
            self.assertEqual(lines[31], "draw")
