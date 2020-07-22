"""Tests of board.py
"""

import unittest

from reversi.board import AbstractBoard, BoardSizeError, Board, BitBoard
from reversi.game import Game
from reversi.player import Player
from reversi.strategies import Random
from reversi.display import NoneDisplay


class TestBoard(unittest.TestCase):
    """board
    """
    def test_board_size(self):
        with self.assertRaises(BoardSizeError):
            Board(-1)

        for size in range(4):
            with self.assertRaises(BoardSizeError):
                Board(size)

        for size in range(5, 28, 2):
            with self.assertRaises(BoardSizeError):
                Board(size)

        with self.assertRaises(BoardSizeError):
            Board(28)

    def test_bitboard_size(self):
        with self.assertRaises(BoardSizeError):
            BitBoard(-1)

        for size in range(4):
            with self.assertRaises(BoardSizeError):
                BitBoard(size)

        for size in range(5, 28, 2):
            with self.assertRaises(BoardSizeError):
                BitBoard(size)

        with self.assertRaises(BoardSizeError):
            BitBoard(28)

    def test_board_size_default(self):
        board = Board()
        self.assertEqual(board.size, 8)

    def test_bitboard_size_default(self):
        board = BitBoard()
        self.assertEqual(board.size, 8)

    def test_board_initial(self):
        for size in range(4, 26+1, 2):
            center1, center2 = size // 2, (size // 2) - 1
            board = Board(size)
            board_ini = [[board.disc['blank'] for _ in range(size)] for _ in range(size)]
            board_ini[center1][center2] = board.disc['black']
            board_ini[center2][center1] = board.disc['black']
            board_ini[center1][center1] = board.disc['white']
            board_ini[center2][center2] = board.disc['white']

            self.assertEqual(board._board, board_ini)

    def test_bitboard_initial(self):
        for size in range(4, 26+1, 2):
            board = BitBoard(size)
            black_bitboard = (0x1 << ((size * (size//2) + (size//2) - 1))) + (0x1 << ((size * (size//2-1) + (size//2))))
            white_bitboard = (0x1 << ((size * (size//2) + (size//2)))) + (0x1 << ((size * (size//2-1) + (size//2-1))))
            self.assertEqual(board._black_bitboard, black_bitboard)
            self.assertEqual(board._white_bitboard, white_bitboard)

    def test_board_size_4_put_disc(self):
        board = Board(4)

        self.assertEqual(board.put_disc('black', 0, 0), [])  # can not flippable
        board.undo()

        self.assertEqual(board.put_disc('black', 3, 5), [])  # out of range

        self.assertEqual(board.put_disc('black', 1, 0), [(1, 1)])
        self.assertEqual(board.put_disc('white', 0, 0), [(1, 1)])
        self.assertEqual(board.put_disc('black', 0, 1), [(1, 1)])
        self.assertEqual(board.put_disc('white', 2, 0), [(2, 1), (1, 0)])
        self.assertEqual(board.put_disc('black', 3, 0), [(2, 1)])
        self.assertEqual(board.put_disc('white', 1, 3), [(1, 2), (1, 1)])
        self.assertEqual(board.put_disc('black', 0, 3), [(1, 2)])
        self.assertEqual(board.put_disc('white', 0, 2), [(1, 2), (0, 1)])
        self.assertEqual(board.put_disc('black', 2, 3), [(1, 3), (2, 2)])
        self.assertEqual(board.put_disc('white', 3, 2), [(2, 2), (2, 1)])
        self.assertEqual(board.put_disc('black', 3, 1), [(2, 2)])
        self.assertEqual(board.put_disc('white', 3, 3), [(2, 2)])
        self.assertEqual(board.get_bitboard_info(), (4366, 61169))

    def test_bitboard_size_4_put_disc(self):
        board = BitBoard(4)

        self.assertEqual(board.put_disc('black', 0, 0), [])  # can not flippable
        board.undo()

        self.assertEqual(board.put_disc('black', 3, 5), [])  # out of range

        self.assertEqual(board.put_disc('black', 1, 0), [(1, 1)])
        self.assertEqual(board.put_disc('white', 0, 0), [(1, 1)])
        self.assertEqual(board.put_disc('black', 0, 1), [(1, 1)])
        self.assertEqual(board.put_disc('white', 2, 0), [(1, 0), (2, 1)])
        self.assertEqual(board.put_disc('black', 3, 0), [(2, 1)])
        self.assertEqual(board.put_disc('white', 1, 3), [(1, 1), (1, 2)])
        self.assertEqual(board.put_disc('black', 0, 3), [(1, 2)])
        self.assertEqual(board.put_disc('white', 0, 2), [(0, 1), (1, 2)])
        self.assertEqual(board.put_disc('black', 2, 3), [(2, 2), (1, 3)])
        self.assertEqual(board.put_disc('white', 3, 2), [(2, 1), (2, 2)])
        self.assertEqual(board.put_disc('black', 3, 1), [(2, 2)])
        self.assertEqual(board.put_disc('white', 3, 3), [(2, 2)])
        self.assertEqual(board.get_bitboard_info(), (4366, 61169))

    def test_board_size_8_play_result(self):
        board = Board()
        board.put_disc('black', 5, 4)
        board.put_disc('white', 5, 5)
        board.put_disc('black', 4, 5)
        board.put_disc('white', 3, 5)
        board.put_disc('black', 2, 6)
        board.put_disc('white', 5, 3)
        board.put_disc('black', 6, 2)
        board.put_disc('white', 3, 6)
        board.put_disc('black', 2, 2)

        board_str = """   a b c d e f g h
 1□□□□□□□□
 2□□□□□□□□
 3□□〇□□□〇□
 4□□□〇●〇□□
 5□□□●〇●□□
 6□□□●●●□□
 7□□〇●□□□□
 8□□□□□□□□
"""

        board_ret = [[board.disc['blank'] for _ in range(8)] for _ in range(8)]
        board_ret[2][2] = board.disc['black']
        board_ret[2][6] = board.disc['black']
        board_ret[3][3] = board.disc['black']
        board_ret[3][4] = board.disc['white']
        board_ret[3][5] = board.disc['black']
        board_ret[4][3] = board.disc['white']
        board_ret[4][4] = board.disc['black']
        board_ret[4][5] = board.disc['white']
        board_ret[5][3] = board.disc['white']
        board_ret[5][4] = board.disc['white']
        board_ret[5][5] = board.disc['white']
        board_ret[6][2] = board.disc['black']
        board_ret[6][3] = board.disc['white']

        board_info_ret = [[0 for _ in range(8)] for _ in range(8)]
        board_info_ret[2][2] = 1
        board_info_ret[2][6] = 1
        board_info_ret[3][3] = 1
        board_info_ret[3][4] = -1
        board_info_ret[3][5] = 1
        board_info_ret[4][3] = -1
        board_info_ret[4][4] = 1
        board_info_ret[4][5] = -1
        board_info_ret[5][3] = -1
        board_info_ret[5][4] = -1
        board_info_ret[5][5] = -1
        board_info_ret[6][2] = 1
        board_info_ret[6][3] = -1

        self.assertEqual(str(board), board_str)
        self.assertEqual(board._board, board_ret)
        self.assertEqual(board.get_board_info(), board_info_ret)
        self.assertEqual(board.get_bitboard_info(), (0x0000221408002000, 0x00000008141C1000))
        self.assertEqual(board.score['black'], 6)
        self.assertEqual(board.score['white'], 7)

    def test_board_size_update_score(self):
        board = Board(4)
        board.score['black'] = 0
        board.score['white'] = 0
        board.update_score()
        self.assertEqual(board.score, {'black': 2, 'white': 2})

        board._board[0][0] = board.disc['white']
        board.update_score()
        self.assertEqual(board.score, {'black': 2, 'white': 3})

        board = Board(8)
        board.score['black'] = 0
        board.score['white'] = 0
        board.update_score()
        self.assertEqual(board.score, {'black': 2, 'white': 2})

        board._board[0][0] = board.disc['white']
        board.update_score()
        self.assertEqual(board.score, {'black': 2, 'white': 3})

        board = Board(26)
        board.score['black'] = 0
        board.score['white'] = 0
        board.update_score()
        self.assertEqual(board.score, {'black': 2, 'white': 2})

        board._board[0][0] = board.disc['white']
        board.update_score()
        self.assertEqual(board.score, {'black': 2, 'white': 3})

    def test_bitboard_update_score(self):
        board = BitBoard(4)
        board.score['black'] = 0
        board.score['white'] = 0
        board.update_score()
        self.assertEqual(board.score, {'black': 2, 'white': 2})

        board._white_bitboard |= 1
        board.update_score()
        self.assertEqual(board.score, {'black': 2, 'white': 3})

        board = BitBoard(8)
        board.score['black'] = 0
        board.score['white'] = 0
        board.update_score()
        self.assertEqual(board.score, {'black': 2, 'white': 2})

        board._white_bitboard |= 1
        board.update_score()
        self.assertEqual(board.score, {'black': 2, 'white': 3})

        board = BitBoard(26)
        board.score['black'] = 0
        board.score['white'] = 0
        board.update_score()
        self.assertEqual(board.score, {'black': 2, 'white': 2})

        board._white_bitboard |= 1
        board.update_score()
        self.assertEqual(board.score, {'black': 2, 'white': 3})

    def test_bitboard_size_8_play_result(self):
        board = BitBoard()
        board.put_disc('black', 5, 4)
        board.put_disc('white', 5, 5)
        board.put_disc('black', 4, 5)
        board.put_disc('white', 3, 5)
        board.put_disc('black', 2, 6)
        board.put_disc('white', 5, 3)
        board.put_disc('black', 6, 2)
        board.put_disc('white', 3, 6)
        board.put_disc('black', 2, 2)

        board_str = """   a b c d e f g h
 1□□□□□□□□
 2□□□□□□□□
 3□□〇□□□〇□
 4□□□〇●〇□□
 5□□□●〇●□□
 6□□□●●●□□
 7□□〇●□□□□
 8□□□□□□□□
"""
        board_info_ret = [[0 for _ in range(8)] for _ in range(8)]
        board_info_ret[2][2] = 1
        board_info_ret[2][6] = 1
        board_info_ret[3][3] = 1
        board_info_ret[3][4] = -1
        board_info_ret[3][5] = 1
        board_info_ret[4][3] = -1
        board_info_ret[4][4] = 1
        board_info_ret[4][5] = -1
        board_info_ret[5][3] = -1
        board_info_ret[5][4] = -1
        board_info_ret[5][5] = -1
        board_info_ret[6][2] = 1
        board_info_ret[6][3] = -1

        self.assertEqual(str(board), board_str)
        self.assertEqual(board.get_board_info(), board_info_ret)
        self.assertEqual(board.get_bitboard_info(), (0x0000221408002000, 0x00000008141C1000))
        self.assertEqual(board.score['black'], 6)
        self.assertEqual(board.score['white'], 7)

    def test_board_size_8_undo(self):
        board = Board()
        board.put_disc('black', 5, 4)
        board.put_disc('white', 5, 5)
        board.put_disc('black', 4, 5)
        board.put_disc('white', 3, 5)
        board.put_disc('black', 2, 6)
        board.put_disc('white', 5, 3)
        board.put_disc('black', 6, 2)
        board.put_disc('white', 3, 6)
        board.put_disc('black', 2, 2)

        board_str = """   a b c d e f g h
 1□□□□□□□□
 2□□□□□□□□
 3□□〇□□□〇□
 4□□□〇●〇□□
 5□□□●〇●□□
 6□□□●●●□□
 7□□〇●□□□□
 8□□□□□□□□
"""
        self.assertEqual(str(board), board_str)

        board_str = """   a b c d e f g h
 1□□□□□□□□
 2□□□□□□□□
 3□□□□□□〇□
 4□□□●●〇□□
 5□□□●〇●□□
 6□□□●●●□□
 7□□〇●□□□□
 8□□□□□□□□
"""
        self.assertEqual(board.undo(), {'color': 'black', 'x': 2, 'y': 2, 'flippable_discs': [(3, 3)]})
        self.assertEqual(str(board), board_str)

    def test_bitboard_size_8_undo(self):
        board = BitBoard()
        board.put_disc('black', 5, 4)
        board.put_disc('white', 5, 5)
        board.put_disc('black', 4, 5)
        board.put_disc('white', 3, 5)
        board.put_disc('black', 2, 6)
        board.put_disc('white', 5, 3)
        board.put_disc('black', 6, 2)
        board.put_disc('white', 3, 6)
        board.put_disc('black', 2, 2)

        board_str = """   a b c d e f g h
 1□□□□□□□□
 2□□□□□□□□
 3□□〇□□□〇□
 4□□□〇●〇□□
 5□□□●〇●□□
 6□□□●●●□□
 7□□〇●□□□□
 8□□□□□□□□
"""
        self.assertEqual(str(board), board_str)

        board_str = """   a b c d e f g h
 1□□□□□□□□
 2□□□□□□□□
 3□□□□□□〇□
 4□□□●●〇□□
 5□□□●〇●□□
 6□□□●●●□□
 7□□〇●□□□□
 8□□□□□□□□
"""
        self.assertEqual(board.undo(), {'color': 'black', 'x': 2, 'y': 2, 'flippable_discs': 0x0000001000000000, 'disc_num': 1})
        self.assertEqual(str(board), board_str)

    def test_bitboard_mask(self):
        board = BitBoard(4)
        self.assertEqual(board._mask.h, 0x6666)
        self.assertEqual(board._mask.v, 0x0FF0)
        self.assertEqual(board._mask.d, 0x0660)
        self.assertEqual(board._mask.u, 0xFFF0)
        self.assertEqual(board._mask.ur, 0x7770)
        self.assertEqual(board._mask.r, 0x7777)
        self.assertEqual(board._mask.br, 0x0777)
        self.assertEqual(board._mask.b, 0x0FFF)
        self.assertEqual(board._mask.bl, 0x0EEE)
        self.assertEqual(board._mask.l, 0xEEEE)
        self.assertEqual(board._mask.ul, 0xEEE0)

        board = BitBoard(8)
        self.assertEqual(board._mask.h, 0x7E7E7E7E7E7E7E7E)
        self.assertEqual(board._mask.v, 0x00FFFFFFFFFFFF00)
        self.assertEqual(board._mask.d, 0x007E7E7E7E7E7E00)
        self.assertEqual(board._mask.u, 0xFFFFFFFFFFFFFF00)
        self.assertEqual(board._mask.ur, 0x7F7F7F7F7F7F7F00)
        self.assertEqual(board._mask.r, 0x7F7F7F7F7F7F7F7F)
        self.assertEqual(board._mask.br, 0x007F7F7F7F7F7F7F)
        self.assertEqual(board._mask.b, 0x00FFFFFFFFFFFFFF)
        self.assertEqual(board._mask.bl, 0x00FEFEFEFEFEFEFE)
        self.assertEqual(board._mask.l, 0xFEFEFEFEFEFEFEFE)
        self.assertEqual(board._mask.ul, 0xFEFEFEFEFEFEFE00)

    def test_board_size_4_get_legal_moves(self):
        board = Board(4)
        blank, black, white = board.disc['blank'], board.disc['black'], board.disc['white']

        board._board = [
            [blank, blank, blank, blank],
            [blank, black, black, blank],
            [blank, black, white, blank],
            [blank, blank, blank, blank],
        ]
        legal_moves = board.get_legal_moves('black')
        self.assertEqual(legal_moves, [(3, 2), (2, 3), (3, 3)])
        legal_moves = board.get_legal_moves('white')
        self.assertEqual(legal_moves, [(0, 0), (2, 0), (0, 2)])

        board._board = [
            [blank, blank, blank, blank],
            [blank, white, white, blank],
            [blank, black, white, blank],
            [blank, blank, blank, blank],
        ]
        legal_moves = board.get_legal_moves('black')
        self.assertEqual(legal_moves, [(1, 0), (3, 0), (3, 2)])
        legal_moves = board.get_legal_moves('white')
        self.assertEqual(legal_moves, [(0, 2), (0, 3), (1, 3)])

        board._board = [
            [blank, blank, blank, blank],
            [blank, white, black, blank],
            [blank, black, black, blank],
            [blank, blank, blank, blank],
        ]
        legal_moves = board.get_legal_moves('black')
        self.assertEqual(legal_moves, [(0, 0), (1, 0), (0, 1)])
        legal_moves = board.get_legal_moves('white')
        self.assertEqual(legal_moves, [(3, 1), (1, 3), (3, 3)])

        board._board = [
            [blank, blank, blank, blank],
            [blank, white, black, blank],
            [blank, white, white, blank],
            [blank, blank, blank, blank],
        ]
        legal_moves = board.get_legal_moves('black')
        self.assertEqual(legal_moves, [(0, 1), (0, 3), (2, 3)])
        legal_moves = board.get_legal_moves('white')
        self.assertEqual(legal_moves, [(2, 0), (3, 0), (3, 1)])

    def test_board_size_4_get_flippable_discs(self):
        board = Board(4)
        blank, black, white = board.disc['blank'], board.disc['black'], board.disc['white']

        board._board = [
            [blank, blank, blank, blank],
            [blank, black, black, blank],
            [blank, black, white, blank],
            [blank, blank, blank, blank],
        ]
        self.assertEqual(board.get_flippable_discs('black', 3, 2), [(2, 2)])
        self.assertEqual(board.get_flippable_discs('black', 2, 3), [(2, 2)])
        self.assertEqual(board.get_flippable_discs('black', 3, 3), [(2, 2)])
        self.assertEqual(board.get_flippable_discs('white', 0, 0), [(1, 1)])
        self.assertEqual(board.get_flippable_discs('white', 2, 0), [(2, 1)])
        self.assertEqual(board.get_flippable_discs('white', 0, 2), [(1, 2)])

        board._board = [
            [blank, blank, blank, blank],
            [blank, white, white, blank],
            [blank, black, white, blank],
            [blank, blank, blank, blank],
        ]
        self.assertEqual(board.get_flippable_discs('black', 1, 0), [(1, 1)])
        self.assertEqual(board.get_flippable_discs('black', 3, 0), [(2, 1)])
        self.assertEqual(board.get_flippable_discs('black', 3, 2), [(2, 2)])
        self.assertEqual(board.get_flippable_discs('white', 0, 2), [(1, 2)])
        self.assertEqual(board.get_flippable_discs('white', 0, 3), [(1, 2)])
        self.assertEqual(board.get_flippable_discs('white', 1, 3), [(1, 2)])

        board._board = [
            [blank, blank, blank, blank],
            [blank, white, black, blank],
            [blank, black, black, blank],
            [blank, blank, blank, blank],
        ]
        self.assertEqual(board.get_flippable_discs('black', 0, 0), [(1, 1)])
        self.assertEqual(board.get_flippable_discs('black', 1, 0), [(1, 1)])
        self.assertEqual(board.get_flippable_discs('black', 0, 1), [(1, 1)])
        self.assertEqual(board.get_flippable_discs('white', 3, 1), [(2, 1)])
        self.assertEqual(board.get_flippable_discs('white', 1, 3), [(1, 2)])
        self.assertEqual(board.get_flippable_discs('white', 3, 3), [(2, 2)])

        board._board = [
            [blank, blank, blank, blank],
            [blank, white, black, blank],
            [blank, white, white, blank],
            [blank, blank, blank, blank],
        ]
        self.assertEqual(board.get_flippable_discs('black', 0, 1), [(1, 1)])
        self.assertEqual(board.get_flippable_discs('black', 0, 3), [(1, 2)])
        self.assertEqual(board.get_flippable_discs('black', 2, 3), [(2, 2)])
        self.assertEqual(board.get_flippable_discs('white', 2, 0), [(2, 1)])
        self.assertEqual(board.get_flippable_discs('white', 3, 0), [(2, 1)])
        self.assertEqual(board.get_flippable_discs('white', 3, 1), [(2, 1)])

    def test_board_size_8_get_legal_moves(self):
        board = Board(8)
        blank, black, white = board.disc['blank'], board.disc['black'], board.disc['white']
        legal_moves = board.get_legal_moves('black')
        self.assertEqual(legal_moves, [(3, 2), (2, 3), (5, 4), (4, 5)])

        # pattern1
        board._board = [
            [blank, blank, blank, blank, blank, blank, blank, blank],
            [blank, white, white, white, white, white, white, blank],
            [blank, white, black, white, white, black, white, blank],
            [blank, white, white, white, white, blank, white, blank],
            [blank, white, blank, white, white, white, white, blank],
            [blank, white, black, white, white, black, white, blank],
            [blank, white, white, white, white, white, white, blank],
            [blank, blank, blank, blank, blank, blank, blank, blank],
        ]
        legal_moves = board.get_legal_moves('black')
        self.assertEqual(legal_moves, [(0, 0), (2, 0), (3, 0), (4, 0), (5, 0), (7, 0), (0, 2), (7, 2), (0, 3), (5, 3), (7, 3), (0, 4), (2, 4), (7, 4), (0, 5), (7, 5), (0, 7), (2, 7), (3, 7), (4, 7), (5, 7), (7, 7)])  # noqa: E501

        # pattern2
        board._board = [
            [blank, blank, blank, blank, blank, blank, blank, blank],
            [blank, white, white, blank, blank, white, blank, white],
            [blank, white, white, white, blank, blank, white, white],
            [blank, white, white, white, white, blank, blank, black],
            [blank, white, white, white, white, white, blank, blank],
            [blank, white, white, white, white, white, white, blank],
            [blank, white, white, white, white, white, white, white],
            [black, blank, black, black, black, black, black, black],
        ]
        legal_moves = board.get_legal_moves('black')
        self.assertEqual(legal_moves, [(0, 0), (2, 0), (4, 0), (7, 0), (0, 1), (3, 1), (0, 2), (4, 2), (5, 2), (0, 3), (5, 3), (6, 3), (0, 4), (6, 4), (7, 4), (0, 5), (7, 5)])  # noqa: E501

        # pattern3
        board._board = [
            [blank, blank, blank, blank, blank, blank, blank, blank],
            [black, blank, black, blank, blank, black, black, blank],
            [black, black, blank, blank, black, black, black, blank],
            [white, blank, blank, black, black, black, black, blank],
            [blank, blank, black, black, black, black, black, blank],
            [blank, black, black, black, black, black, black, blank],
            [black, black, black, black, black, black, black, blank],
            [white, white, white, white, white, white, blank, white],
        ]
        legal_moves = board.get_legal_moves('white')
        self.assertEqual(legal_moves, [(0, 0), (3, 0), (5, 0), (7, 0), (4, 1), (7, 1), (2, 2), (3, 2), (7, 2), (1, 3), (2, 3), (7, 3), (0, 4), (1, 4), (7, 4), (0, 5), (7, 5)])  # noqa: E501

        # pattern4
        board._board = [
            [blank, blank, blank, blank, blank, blank, blank, black],
            [blank, white, white, white, white, white, white, blank],
            [blank, white, white, white, white, white, white, black],
            [blank, blank, white, white, white, white, white, black],
            [blank, blank, blank, white, white, white, white, black],
            [blank, white, blank, blank, white, white, white, black],
            [blank, blank, white, blank, blank, white, white, black],
            [blank, white, white, black, blank, blank, white, black],
        ]
        legal_moves = board.get_legal_moves('black')
        self.assertEqual(legal_moves, [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (0, 2), (1, 3), (0, 4), (2, 4), (2, 5), (3, 5), (3, 6), (4, 6), (0, 7), (4, 7), (5, 7)])  # noqa: E501

        # pattern5
        board._board = [
            [black, blank, black, black, black, black, black, black],
            [blank, white, white, white, white, white, white, white],
            [blank, white, white, white, white, white, white, blank],
            [blank, white, white, white, white, white, blank, blank],
            [blank, white, white, white, white, blank, blank, black],
            [blank, white, white, white, blank, blank, white, white],
            [blank, white, white, blank, blank, white, blank, white],
            [blank, blank, blank, blank, blank, blank, blank, blank],
        ]
        legal_moves = board.get_legal_moves('black')
        self.assertEqual(legal_moves, [(0, 2), (7, 2), (0, 3), (6, 3), (7, 3), (0, 4), (5, 4), (6, 4), (0, 5), (4, 5), (5, 5), (0, 6), (3, 6), (0, 7), (2, 7), (4, 7), (7, 7)])  # noqa: E501

        # pattern6
        board._board = [
            [black, blank, blank, blank, blank, blank, blank, blank],
            [blank, white, white, white, white, white, white, blank],
            [black, white, white, white, white, white, white, blank],
            [black, white, white, white, white, white, blank, blank],
            [black, white, white, white, white, blank, blank, blank],
            [black, white, white, white, blank, blank, white, blank],
            [black, white, white, blank, blank, white, blank, blank],
            [black, white, blank, blank, black, white, white, blank],
        ]
        legal_moves = board.get_legal_moves('black')
        self.assertEqual(legal_moves, [(2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (7, 2), (6, 3), (5, 4), (7, 4), (4, 5), (5, 5), (3, 6), (4, 6), (2, 7), (3, 7), (7, 7)])  # noqa: E501

        # pattern7
        board._board = [
            [blank, blank, blank, blank, blank, blank, blank, blank],
            [blank, blank, blank, blank, blank, blank, blank, blank],
            [blank, blank, blank, blank, blank, blank, blank, blank],
            [blank, blank, blank, white, white, white, blank, blank],
            [blank, blank, blank, white, white, white, blank, blank],
            [blank, blank, blank, white, black, white, blank, blank],
            [blank, blank, blank, black, blank, blank, blank, blank],
            [blank, blank, blank, blank, blank, blank, blank, blank],
        ]
        legal_moves = board.get_legal_moves('black')
        self.assertEqual(legal_moves, [(3, 2), (4, 2), (2, 3), (6, 3), (2, 5), (6, 5)])

    def test_board_size_8_get_flippable_discs(self):
        board = Board(8)
        blank, black, white = board.disc['blank'], board.disc['black'], board.disc['white']

        self.assertEqual(board.get_flippable_discs('black', 3, 2), [(3, 3)])
        self.assertEqual(board.get_flippable_discs('black', 2, 3), [(3, 3)])
        self.assertEqual(board.get_flippable_discs('black', 5, 4), [(4, 4)])
        self.assertEqual(board.get_flippable_discs('black', 4, 5), [(4, 4)])

        # pattern1
        board._board = [
            [blank, blank, blank, blank, blank, blank, blank, blank],
            [blank, white, white, white, white, white, white, blank],
            [blank, white, black, white, white, black, white, blank],
            [blank, white, white, white, white, blank, white, blank],
            [blank, white, blank, white, white, white, white, blank],
            [blank, white, black, white, white, black, white, blank],
            [blank, white, white, white, white, white, white, blank],
            [blank, blank, blank, blank, blank, blank, blank, blank],
        ]
        self.assertEqual(board.get_flippable_discs('black', 0, 0), [(1, 1)])
        self.assertEqual(board.get_flippable_discs('black', 2, 0), [(2, 1)])
        self.assertEqual(board.get_flippable_discs('black', 3, 0), [(4, 1)])
        self.assertEqual(board.get_flippable_discs('black', 4, 0), [(3, 1)])
        self.assertEqual(board.get_flippable_discs('black', 5, 0), [(5, 1)])
        self.assertEqual(board.get_flippable_discs('black', 7, 0), [(6, 1)])
        self.assertEqual(board.get_flippable_discs('black', 0, 2), [(1, 2)])
        self.assertEqual(board.get_flippable_discs('black', 7, 2), [(6, 2)])
        self.assertEqual(board.get_flippable_discs('black', 0, 3), [(1, 4)])
        self.assertEqual(board.get_flippable_discs('black', 5, 3), [(5, 4)])
        self.assertEqual(board.get_flippable_discs('black', 7, 3), [(6, 4)])
        self.assertEqual(board.get_flippable_discs('black', 0, 4), [(1, 3)])
        self.assertEqual(board.get_flippable_discs('black', 2, 4), [(2, 3)])
        self.assertEqual(board.get_flippable_discs('black', 7, 4), [(6, 3)])
        self.assertEqual(board.get_flippable_discs('black', 0, 5), [(1, 5)])
        self.assertEqual(board.get_flippable_discs('black', 7, 5), [(6, 5)])
        self.assertEqual(board.get_flippable_discs('black', 0, 7), [(1, 6)])
        self.assertEqual(board.get_flippable_discs('black', 2, 7), [(2, 6)])
        self.assertEqual(board.get_flippable_discs('black', 3, 7), [(4, 6)])
        self.assertEqual(board.get_flippable_discs('black', 4, 7), [(3, 6)])
        self.assertEqual(board.get_flippable_discs('black', 5, 7), [(5, 6)])
        self.assertEqual(board.get_flippable_discs('black', 7, 7), [(6, 6)])

        # pattern2
        board._board = [
            [blank, blank, blank, blank, blank, blank, blank, blank],
            [blank, white, white, blank, blank, white, blank, white],
            [blank, white, white, white, blank, blank, white, white],
            [blank, white, white, white, white, blank, blank, black],
            [blank, white, white, white, white, white, blank, blank],
            [blank, white, white, white, white, white, white, blank],
            [blank, white, white, white, white, white, white, white],
            [black, blank, black, black, black, black, black, black],
        ]
        self.assertEqual(board.get_flippable_discs('black', 0, 0), [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)])
        self.assertEqual(board.get_flippable_discs('black', 2, 0), [(2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6)])
        self.assertEqual(board.get_flippable_discs('black', 4, 0), [(5, 1), (6, 2)])
        self.assertEqual(board.get_flippable_discs('black', 7, 0), [(7, 1), (7, 2)])
        self.assertEqual(board.get_flippable_discs('black', 0, 1), [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6)])
        self.assertEqual(board.get_flippable_discs('black', 3, 1), [(3, 2), (3, 3), (3, 4), (3, 5), (3, 6)])
        self.assertEqual(board.get_flippable_discs('black', 0, 2), [(1, 3), (2, 4), (3, 5), (4, 6)])
        self.assertEqual(board.get_flippable_discs('black', 4, 2), [(4, 3), (4, 4), (4, 5), (4, 6)])
        self.assertEqual(board.get_flippable_discs('black', 5, 2), [(4, 3), (3, 4), (2, 5), (1, 6)])
        self.assertEqual(board.get_flippable_discs('black', 0, 3), [(1, 4), (2, 5), (3, 6)])
        self.assertEqual(board.get_flippable_discs('black', 5, 3), [(5, 4), (5, 5), (5, 6)])
        self.assertEqual(board.get_flippable_discs('black', 6, 3), [(5, 4), (4, 5), (3, 6)])
        self.assertEqual(board.get_flippable_discs('black', 0, 4), [(1, 5), (2, 6)])
        self.assertEqual(board.get_flippable_discs('black', 6, 4), [(5, 5), (4, 6), (6, 5), (6, 6)])
        self.assertEqual(board.get_flippable_discs('black', 7, 4), [(6, 5), (5, 6)])
        self.assertEqual(board.get_flippable_discs('black', 0, 5), [(1, 6)])
        self.assertEqual(board.get_flippable_discs('black', 7, 5), [(6, 6), (7, 6)])

        # pattern3
        board._board = [
            [blank, blank, blank, blank, blank, blank, blank, blank],
            [black, blank, black, blank, blank, black, black, blank],
            [black, black, blank, blank, black, black, black, blank],
            [white, blank, blank, black, black, black, black, blank],
            [blank, blank, black, black, black, black, black, blank],
            [blank, black, black, black, black, black, black, blank],
            [black, black, black, black, black, black, black, blank],
            [white, white, white, white, white, white, blank, white],
        ]
        self.assertEqual(board.get_flippable_discs('white', 0, 0), [(0, 1), (0, 2)])
        self.assertEqual(board.get_flippable_discs('white', 3, 0), [(2, 1), (1, 2)])
        self.assertEqual(board.get_flippable_discs('white', 5, 0), [(5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6)])
        self.assertEqual(board.get_flippable_discs('white', 7, 0), [(6, 1), (5, 2), (4, 3), (3, 4), (2, 5), (1, 6)])
        self.assertEqual(board.get_flippable_discs('white', 4, 1), [(4, 2), (4, 3), (4, 4), (4, 5), (4, 6)])
        self.assertEqual(board.get_flippable_discs('white', 7, 1), [(6, 2), (5, 3), (4, 4), (3, 5), (2, 6)])
        self.assertEqual(board.get_flippable_discs('white', 2, 2), [(3, 3), (4, 4), (5, 5), (6, 6)])
        self.assertEqual(board.get_flippable_discs('white', 3, 2), [(3, 3), (3, 4), (3, 5), (3, 6)])
        self.assertEqual(board.get_flippable_discs('white', 7, 2), [(6, 3), (5, 4), (4, 5), (3, 6)])
        self.assertEqual(board.get_flippable_discs('white', 1, 3), [(2, 4), (3, 5), (4, 6)])
        self.assertEqual(board.get_flippable_discs('white', 2, 3), [(2, 4), (2, 5), (2, 6)])
        self.assertEqual(board.get_flippable_discs('white', 7, 3), [(6, 4), (5, 5), (4, 6)])
        self.assertEqual(board.get_flippable_discs('white', 0, 4), [(1, 5), (2, 6)])
        self.assertEqual(board.get_flippable_discs('white', 1, 4), [(1, 5), (1, 6), (2, 5), (3, 6)])
        self.assertEqual(board.get_flippable_discs('white', 7, 4), [(6, 5), (5, 6)])
        self.assertEqual(board.get_flippable_discs('white', 0, 5), [(0, 6), (1, 6)])
        self.assertEqual(board.get_flippable_discs('white', 7, 5), [(6, 6)])

        # pattern4
        board._board = [
            [blank, blank, blank, blank, blank, blank, blank, black],
            [blank, white, white, white, white, white, white, blank],
            [blank, white, white, white, white, white, white, black],
            [blank, blank, white, white, white, white, white, black],
            [blank, blank, blank, white, white, white, white, black],
            [blank, white, blank, blank, white, white, white, black],
            [blank, blank, white, blank, blank, white, white, black],
            [blank, white, white, black, blank, blank, white, black],
        ]
        self.assertEqual(board.get_flippable_discs('black', 0, 0), [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)])
        self.assertEqual(board.get_flippable_discs('black', 1, 0), [(2, 1), (3, 2), (4, 3), (5, 4), (6, 5)])
        self.assertEqual(board.get_flippable_discs('black', 2, 0), [(3, 1), (4, 2), (5, 3), (6, 4)])
        self.assertEqual(board.get_flippable_discs('black', 3, 0), [(4, 1), (5, 2), (6, 3)])
        self.assertEqual(board.get_flippable_discs('black', 4, 0), [(5, 1), (6, 2)])
        self.assertEqual(board.get_flippable_discs('black', 5, 0), [(6, 1)])
        self.assertEqual(board.get_flippable_discs('black', 0, 2), [(1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2)])
        self.assertEqual(board.get_flippable_discs('black', 1, 3), [(2, 3), (3, 3), (4, 3), (5, 3), (6, 3)])
        self.assertEqual(board.get_flippable_discs('black', 0, 4), [(1, 5), (2, 6)])
        self.assertEqual(board.get_flippable_discs('black', 2, 4), [(3, 4), (4, 4), (5, 4), (6, 4)])
        self.assertEqual(board.get_flippable_discs('black', 2, 5), [(3, 4), (4, 3), (5, 2), (6, 1)])
        self.assertEqual(board.get_flippable_discs('black', 3, 5), [(4, 5), (5, 5), (6, 5)])
        self.assertEqual(board.get_flippable_discs('black', 3, 6), [(4, 5), (5, 4), (6, 3)])
        self.assertEqual(board.get_flippable_discs('black', 4, 6), [(5, 6), (6, 6), (5, 5), (6, 4)])
        self.assertEqual(board.get_flippable_discs('black', 0, 7), [(1, 7), (2, 7)])
        self.assertEqual(board.get_flippable_discs('black', 4, 7), [(5, 6), (6, 5)])
        self.assertEqual(board.get_flippable_discs('black', 5, 7), [(6, 7), (6, 6)])

        # pattern5
        board._board = [
            [black, blank, black, black, black, black, black, black],
            [blank, white, white, white, white, white, white, white],
            [blank, white, white, white, white, white, white, blank],
            [blank, white, white, white, white, white, blank, blank],
            [blank, white, white, white, white, blank, blank, black],
            [blank, white, white, white, blank, blank, white, white],
            [blank, white, white, blank, blank, white, blank, white],
            [blank, blank, blank, blank, blank, blank, blank, blank],
        ]
        self.assertEqual(board.get_flippable_discs('black', 0, 2), [(1, 1)])
        self.assertEqual(board.get_flippable_discs('black', 7, 2), [(6, 1), (7, 1)])
        self.assertEqual(board.get_flippable_discs('black', 0, 3), [(1, 2), (2, 1)])
        self.assertEqual(board.get_flippable_discs('black', 6, 3), [(5, 2), (4, 1), (6, 2), (6, 1)])
        self.assertEqual(board.get_flippable_discs('black', 7, 3), [(6, 2), (5, 1)])
        self.assertEqual(board.get_flippable_discs('black', 0, 4), [(1, 3), (2, 2), (3, 1)])
        self.assertEqual(board.get_flippable_discs('black', 5, 4), [(5, 3), (5, 2), (5, 1)])
        self.assertEqual(board.get_flippable_discs('black', 6, 4), [(5, 3), (4, 2), (3, 1)])
        self.assertEqual(board.get_flippable_discs('black', 0, 5), [(1, 4), (2, 3), (3, 2), (4, 1)])
        self.assertEqual(board.get_flippable_discs('black', 4, 5), [(4, 4), (4, 3), (4, 2), (4, 1)])
        self.assertEqual(board.get_flippable_discs('black', 5, 5), [(4, 4), (3, 3), (2, 2), (1, 1)])
        self.assertEqual(board.get_flippable_discs('black', 0, 6), [(1, 5), (2, 4), (3, 3), (4, 2), (5, 1)])
        self.assertEqual(board.get_flippable_discs('black', 3, 6), [(3, 5), (3, 4), (3, 3), (3, 2), (3, 1)])
        self.assertEqual(board.get_flippable_discs('black', 0, 7), [(1, 6), (2, 5), (3, 4), (4, 3), (5, 2), (6, 1)])
        self.assertEqual(board.get_flippable_discs('black', 2, 7), [(2, 6), (2, 5), (2, 4), (2, 3), (2, 2), (2, 1)])
        self.assertEqual(board.get_flippable_discs('black', 4, 7), [(5, 6), (6, 5)])
        self.assertEqual(board.get_flippable_discs('black', 7, 7), [(7, 6), (7, 5)])

        # pattern6
        board._board = [
            [black, blank, blank, blank, blank, blank, blank, blank],
            [blank, white, white, white, white, white, white, blank],
            [black, white, white, white, white, white, white, blank],
            [black, white, white, white, white, white, blank, blank],
            [black, white, white, white, white, blank, blank, blank],
            [black, white, white, white, blank, blank, white, blank],
            [black, white, white, blank, blank, white, blank, blank],
            [black, white, blank, blank, black, white, white, blank],
        ]
        self.assertEqual(board.get_flippable_discs('black', 2, 0), [(1, 1)])
        self.assertEqual(board.get_flippable_discs('black', 3, 0), [(2, 1), (1, 2)])
        self.assertEqual(board.get_flippable_discs('black', 4, 0), [(3, 1), (2, 2), (1, 3)])
        self.assertEqual(board.get_flippable_discs('black', 5, 0), [(4, 1), (3, 2), (2, 3), (1, 4)])
        self.assertEqual(board.get_flippable_discs('black', 6, 0), [(5, 1), (4, 2), (3, 3), (2, 4), (1, 5)])
        self.assertEqual(board.get_flippable_discs('black', 7, 0), [(6, 1), (5, 2), (4, 3), (3, 4), (2, 5), (1, 6)])
        self.assertEqual(board.get_flippable_discs('black', 7, 2), [(6, 2), (5, 2), (4, 2), (3, 2), (2, 2), (1, 2)])
        self.assertEqual(board.get_flippable_discs('black', 6, 3), [(5, 3), (4, 3), (3, 3), (2, 3), (1, 3)])
        self.assertEqual(board.get_flippable_discs('black', 5, 4), [(4, 4), (3, 4), (2, 4), (1, 4)])
        self.assertEqual(board.get_flippable_discs('black', 7, 4), [(6, 5), (5, 6)])
        self.assertEqual(board.get_flippable_discs('black', 4, 5), [(3, 5), (2, 5), (1, 5)])
        self.assertEqual(board.get_flippable_discs('black', 5, 5), [(4, 4), (3, 3), (2, 2), (1, 1)])
        self.assertEqual(board.get_flippable_discs('black', 3, 6), [(2, 6), (1, 6), (2, 5), (1, 4)])
        self.assertEqual(board.get_flippable_discs('black', 4, 6), [(3, 5), (2, 4), (1, 3)])
        self.assertEqual(board.get_flippable_discs('black', 2, 7), [(1, 7), (1, 6)])
        self.assertEqual(board.get_flippable_discs('black', 3, 7), [(2, 6), (1, 5)])
        self.assertEqual(board.get_flippable_discs('black', 7, 7), [(6, 7), (5, 7)])

        # pattern7
        board._board = [
            [blank, blank, blank, blank, blank, blank, blank, blank],
            [blank, blank, blank, blank, blank, blank, blank, blank],
            [blank, blank, blank, blank, blank, blank, blank, blank],
            [blank, blank, blank, white, white, white, blank, blank],
            [blank, blank, blank, white, white, white, blank, blank],
            [blank, blank, blank, white, black, white, blank, blank],
            [blank, blank, blank, black, blank, blank, blank, blank],
            [blank, blank, blank, blank, blank, blank, blank, blank],
        ]
        self.assertEqual(board.get_flippable_discs('black', 3, 2), [(3, 3), (3, 4), (3, 5)])
        self.assertEqual(board.get_flippable_discs('black', 4, 2), [(4, 3), (4, 4)])
        self.assertEqual(board.get_flippable_discs('black', 2, 3), [(3, 4)])
        self.assertEqual(board.get_flippable_discs('black', 6, 3), [(5, 4)])
        self.assertEqual(board.get_flippable_discs('black', 2, 5), [(3, 5)])
        self.assertEqual(board.get_flippable_discs('black', 6, 5), [(5, 5)])

    def test_bitboard_size_4_get_legal_moves(self):
        board = BitBoard(4)

        board._black_bitboard = 0x640
        board._white_bitboard = 0x020
        legal_moves = board.get_legal_moves('black')
        self.assertEqual(legal_moves, [(3, 2), (2, 3), (3, 3)])
        legal_moves = board.get_legal_moves('white')
        self.assertEqual(legal_moves, [(0, 0), (2, 0), (0, 2)])

        board._black_bitboard = 0x040
        board._white_bitboard = 0x620
        legal_moves = board.get_legal_moves('black')
        self.assertEqual(legal_moves, [(1, 0), (3, 0), (3, 2)])
        legal_moves = board.get_legal_moves('white')
        self.assertEqual(legal_moves, [(0, 2), (0, 3), (1, 3)])

        board._black_bitboard = 0x260
        board._white_bitboard = 0x400
        legal_moves = board.get_legal_moves('black')
        self.assertEqual(legal_moves, [(0, 0), (1, 0), (0, 1)])
        legal_moves = board.get_legal_moves('white')
        self.assertEqual(legal_moves, [(3, 1), (1, 3), (3, 3)])

        board._black_bitboard = 0x200
        board._white_bitboard = 0x460
        legal_moves = board.get_legal_moves('black')
        self.assertEqual(legal_moves, [(0, 1), (0, 3), (2, 3)])
        legal_moves = board.get_legal_moves('white')
        self.assertEqual(legal_moves, [(2, 0), (3, 0), (3, 1)])

    def test_bitboard_size_4_get_flippable_discs(self):
        board = BitBoard(4)

        board._black_bitboard = 0x640
        board._white_bitboard = 0x020
        self.assertEqual(board.get_flippable_discs('black', 3, 2), [(2, 2)])
        self.assertEqual(board.get_flippable_discs('black', 2, 3), [(2, 2)])
        self.assertEqual(board.get_flippable_discs('black', 3, 3), [(2, 2)])
        self.assertEqual(board.get_flippable_discs('white', 0, 0), [(1, 1)])
        self.assertEqual(board.get_flippable_discs('white', 2, 0), [(2, 1)])
        self.assertEqual(board.get_flippable_discs('white', 0, 2), [(1, 2)])

        board._black_bitboard = 0x040
        board._white_bitboard = 0x620
        self.assertEqual(board.get_flippable_discs('black', 1, 0), [(1, 1)])
        self.assertEqual(board.get_flippable_discs('black', 3, 0), [(2, 1)])
        self.assertEqual(board.get_flippable_discs('black', 3, 2), [(2, 2)])
        self.assertEqual(board.get_flippable_discs('white', 0, 2), [(1, 2)])
        self.assertEqual(board.get_flippable_discs('white', 0, 3), [(1, 2)])
        self.assertEqual(board.get_flippable_discs('white', 1, 3), [(1, 2)])

        board._black_bitboard = 0x260
        board._white_bitboard = 0x400
        self.assertEqual(board.get_flippable_discs('black', 0, 0), [(1, 1)])
        self.assertEqual(board.get_flippable_discs('black', 1, 0), [(1, 1)])
        self.assertEqual(board.get_flippable_discs('black', 0, 1), [(1, 1)])
        self.assertEqual(board.get_flippable_discs('white', 3, 1), [(2, 1)])
        self.assertEqual(board.get_flippable_discs('white', 1, 3), [(1, 2)])
        self.assertEqual(board.get_flippable_discs('white', 3, 3), [(2, 2)])

        board._black_bitboard = 0x200
        board._white_bitboard = 0x460
        self.assertEqual(board.get_flippable_discs('black', 0, 1), [(1, 1)])
        self.assertEqual(board.get_flippable_discs('black', 0, 3), [(1, 2)])
        self.assertEqual(board.get_flippable_discs('black', 2, 3), [(2, 2)])
        self.assertEqual(board.get_flippable_discs('white', 2, 0), [(2, 1)])
        self.assertEqual(board.get_flippable_discs('white', 3, 0), [(2, 1)])
        self.assertEqual(board.get_flippable_discs('white', 3, 1), [(2, 1)])

    def test_bitboard_size_8_get_legal_moves(self):
        board = BitBoard(8)
        legal_moves = board.get_legal_moves('black')
        self.assertEqual(legal_moves, [(3, 2), (2, 3), (5, 4), (4, 5)])

        # pattern1
        board._black_bitboard = 0x0000240000240000
        board._white_bitboard = 0x007E5A7A5E5A7E00
        legal_moves = board.get_legal_moves('black')
        self.assertEqual(legal_moves, [(0, 0), (2, 0), (3, 0), (4, 0), (5, 0), (7, 0), (0, 2), (7, 2), (0, 3), (5, 3), (7, 3), (0, 4), (2, 4), (7, 4), (0, 5), (7, 5), (0, 7), (2, 7), (3, 7), (4, 7), (5, 7), (7, 7)])  # noqa: E501

        # pattern2
        board._black_bitboard = 0x00000001000000BF
        board._white_bitboard = 0x006573787C7E7F00
        legal_moves = board.get_legal_moves('black')
        self.assertEqual(legal_moves, [(0, 0), (2, 0), (4, 0), (7, 0), (0, 1), (3, 1), (0, 2), (4, 2), (5, 2), (0, 3), (5, 3), (6, 3), (0, 4), (6, 4), (7, 4), (0, 5), (7, 5)])  # noqa: E501

        # pattern3
        board._black_bitboard = 0x00A6CE1E3E7EFE00
        board._white_bitboard = 0x00000080000000FD
        legal_moves = board.get_legal_moves('white')
        self.assertEqual(legal_moves, [(0, 0), (3, 0), (5, 0), (7, 0), (4, 1), (7, 1), (2, 2), (3, 2), (7, 2), (1, 3), (2, 3), (7, 3), (0, 4), (1, 4), (7, 4), (0, 5), (7, 5)])  # noqa: E501

        # pattern4
        board._black_bitboard = 0x0100010101010111
        board._white_bitboard = 0x007E7E3E1E4E2662
        legal_moves = board.get_legal_moves('black')
        self.assertEqual(legal_moves, [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (0, 2), (1, 3), (0, 4), (2, 4), (2, 5), (3, 5), (3, 6), (4, 6), (0, 7), (4, 7), (5, 7)])  # noqa: E501

        # pattern5
        board._black_bitboard = 0xBF00000001000000
        board._white_bitboard = 0x007F7E7C78736500
        legal_moves = board.get_legal_moves('black')
        self.assertEqual(legal_moves, [(0, 2), (7, 2), (0, 3), (6, 3), (7, 3), (0, 4), (5, 4), (6, 4), (0, 5), (4, 5), (5, 5), (0, 6), (3, 6), (0, 7), (2, 7), (4, 7), (7, 7)])  # noqa: E501

        # pattern6
        board._black_bitboard = 0x8000808080808088
        board._white_bitboard = 0x007E7E7C78726446
        legal_moves = board.get_legal_moves('black')
        self.assertEqual(legal_moves, [(2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (7, 2), (6, 3), (5, 4), (7, 4), (4, 5), (5, 5), (3, 6), (4, 6), (2, 7), (3, 7), (7, 7)])  # noqa: E501

        # pattern7
        board._black_bitboard = 0x0000000000081000
        board._white_bitboard = 0x0000001C1C140000
        legal_moves = board.get_legal_moves('black')
        self.assertEqual(legal_moves, [(3, 2), (4, 2), (2, 3), (6, 3), (2, 5), (6, 5)])

    def test_bitboard_size_8_get_flippable_discs(self):
        board = BitBoard(8)
        self.assertEqual(board.get_flippable_discs('black', 3, 2), [(3, 3)])
        self.assertEqual(board.get_flippable_discs('black', 2, 3), [(3, 3)])
        self.assertEqual(board.get_flippable_discs('black', 5, 4), [(4, 4)])
        self.assertEqual(board.get_flippable_discs('black', 4, 5), [(4, 4)])

        # pattern1
        board._black_bitboard = 0x0000240000240000
        board._white_bitboard = 0x007E5A7A5E5A7E00
        self.assertEqual(board.get_flippable_discs('black', 0, 0), [(1, 1)])
        self.assertEqual(board.get_flippable_discs('black', 2, 0), [(2, 1)])
        self.assertEqual(board.get_flippable_discs('black', 3, 0), [(4, 1)])
        self.assertEqual(board.get_flippable_discs('black', 4, 0), [(3, 1)])
        self.assertEqual(board.get_flippable_discs('black', 5, 0), [(5, 1)])
        self.assertEqual(board.get_flippable_discs('black', 7, 0), [(6, 1)])
        self.assertEqual(board.get_flippable_discs('black', 0, 2), [(1, 2)])
        self.assertEqual(board.get_flippable_discs('black', 7, 2), [(6, 2)])
        self.assertEqual(board.get_flippable_discs('black', 0, 3), [(1, 4)])
        self.assertEqual(board.get_flippable_discs('black', 5, 3), [(5, 4)])
        self.assertEqual(board.get_flippable_discs('black', 7, 3), [(6, 4)])
        self.assertEqual(board.get_flippable_discs('black', 0, 4), [(1, 3)])
        self.assertEqual(board.get_flippable_discs('black', 2, 4), [(2, 3)])
        self.assertEqual(board.get_flippable_discs('black', 7, 4), [(6, 3)])
        self.assertEqual(board.get_flippable_discs('black', 0, 5), [(1, 5)])
        self.assertEqual(board.get_flippable_discs('black', 7, 5), [(6, 5)])
        self.assertEqual(board.get_flippable_discs('black', 0, 7), [(1, 6)])
        self.assertEqual(board.get_flippable_discs('black', 2, 7), [(2, 6)])
        self.assertEqual(board.get_flippable_discs('black', 3, 7), [(4, 6)])
        self.assertEqual(board.get_flippable_discs('black', 4, 7), [(3, 6)])
        self.assertEqual(board.get_flippable_discs('black', 5, 7), [(5, 6)])
        self.assertEqual(board.get_flippable_discs('black', 7, 7), [(6, 6)])

        # pattern2
        board._black_bitboard = 0x00000001000000BF
        board._white_bitboard = 0x006573787C7E7F00
        self.assertEqual(board.get_flippable_discs('black', 0, 0), [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)])
        self.assertEqual(board.get_flippable_discs('black', 2, 0), [(2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6)])
        self.assertEqual(board.get_flippable_discs('black', 4, 0), [(5, 1), (6, 2)])
        self.assertEqual(board.get_flippable_discs('black', 7, 0), [(7, 1), (7, 2)])
        self.assertEqual(board.get_flippable_discs('black', 0, 1), [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6)])
        self.assertEqual(board.get_flippable_discs('black', 3, 1), [(3, 2), (3, 3), (3, 4), (3, 5), (3, 6)])
        self.assertEqual(board.get_flippable_discs('black', 0, 2), [(1, 3), (2, 4), (3, 5), (4, 6)])
        self.assertEqual(board.get_flippable_discs('black', 4, 2), [(4, 3), (4, 4), (4, 5), (4, 6)])
        self.assertEqual(board.get_flippable_discs('black', 5, 2), [(4, 3), (3, 4), (2, 5), (1, 6)])
        self.assertEqual(board.get_flippable_discs('black', 0, 3), [(1, 4), (2, 5), (3, 6)])
        self.assertEqual(board.get_flippable_discs('black', 5, 3), [(5, 4), (5, 5), (5, 6)])
        self.assertEqual(board.get_flippable_discs('black', 6, 3), [(5, 4), (4, 5), (3, 6)])
        self.assertEqual(board.get_flippable_discs('black', 0, 4), [(1, 5), (2, 6)])
        self.assertEqual(board.get_flippable_discs('black', 6, 4), [(5, 5), (6, 5), (4, 6), (6, 6)])
        self.assertEqual(board.get_flippable_discs('black', 7, 4), [(6, 5), (5, 6)])
        self.assertEqual(board.get_flippable_discs('black', 0, 5), [(1, 6)])
        self.assertEqual(board.get_flippable_discs('black', 7, 5), [(6, 6), (7, 6)])

        # pattern3
        board._black_bitboard = 0x00A6CE1E3E7EFE00
        board._white_bitboard = 0x00000080000000FD
        self.assertEqual(board.get_flippable_discs('white', 0, 0), [(0, 1), (0, 2)])
        self.assertEqual(board.get_flippable_discs('white', 3, 0), [(2, 1), (1, 2)])
        self.assertEqual(board.get_flippable_discs('white', 5, 0), [(5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6)])
        self.assertEqual(board.get_flippable_discs('white', 7, 0), [(6, 1), (5, 2), (4, 3), (3, 4), (2, 5), (1, 6)])
        self.assertEqual(board.get_flippable_discs('white', 4, 1), [(4, 2), (4, 3), (4, 4), (4, 5), (4, 6)])
        self.assertEqual(board.get_flippable_discs('white', 7, 1), [(6, 2), (5, 3), (4, 4), (3, 5), (2, 6)])
        self.assertEqual(board.get_flippable_discs('white', 2, 2), [(3, 3), (4, 4), (5, 5), (6, 6)])
        self.assertEqual(board.get_flippable_discs('white', 3, 2), [(3, 3), (3, 4), (3, 5), (3, 6)])
        self.assertEqual(board.get_flippable_discs('white', 7, 2), [(6, 3), (5, 4), (4, 5), (3, 6)])
        self.assertEqual(board.get_flippable_discs('white', 1, 3), [(2, 4), (3, 5), (4, 6)])
        self.assertEqual(board.get_flippable_discs('white', 2, 3), [(2, 4), (2, 5), (2, 6)])
        self.assertEqual(board.get_flippable_discs('white', 7, 3), [(6, 4), (5, 5), (4, 6)])
        self.assertEqual(board.get_flippable_discs('white', 0, 4), [(1, 5), (2, 6)])
        self.assertEqual(board.get_flippable_discs('white', 1, 4), [(1, 5), (2, 5), (1, 6), (3, 6)])
        self.assertEqual(board.get_flippable_discs('white', 7, 4), [(6, 5), (5, 6)])
        self.assertEqual(board.get_flippable_discs('white', 0, 5), [(0, 6), (1, 6)])
        self.assertEqual(board.get_flippable_discs('white', 7, 5), [(6, 6)])

        # pattern4
        board._black_bitboard = 0x0100010101010111
        board._white_bitboard = 0x007E7E3E1E4E2662
        self.assertEqual(board.get_flippable_discs('black', 0, 0), [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)])
        self.assertEqual(board.get_flippable_discs('black', 1, 0), [(2, 1), (3, 2), (4, 3), (5, 4), (6, 5)])
        self.assertEqual(board.get_flippable_discs('black', 2, 0), [(3, 1), (4, 2), (5, 3), (6, 4)])
        self.assertEqual(board.get_flippable_discs('black', 3, 0), [(4, 1), (5, 2), (6, 3)])
        self.assertEqual(board.get_flippable_discs('black', 4, 0), [(5, 1), (6, 2)])
        self.assertEqual(board.get_flippable_discs('black', 5, 0), [(6, 1)])
        self.assertEqual(board.get_flippable_discs('black', 0, 2), [(1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2)])
        self.assertEqual(board.get_flippable_discs('black', 1, 3), [(2, 3), (3, 3), (4, 3), (5, 3), (6, 3)])
        self.assertEqual(board.get_flippable_discs('black', 0, 4), [(1, 5), (2, 6)])
        self.assertEqual(board.get_flippable_discs('black', 2, 4), [(3, 4), (4, 4), (5, 4), (6, 4)])
        self.assertEqual(board.get_flippable_discs('black', 2, 5), [(6, 1), (5, 2), (4, 3), (3, 4)])
        self.assertEqual(board.get_flippable_discs('black', 3, 5), [(4, 5), (5, 5), (6, 5)])
        self.assertEqual(board.get_flippable_discs('black', 3, 6), [(6, 3), (5, 4), (4, 5)])
        self.assertEqual(board.get_flippable_discs('black', 4, 6), [(6, 4), (5, 5), (5, 6), (6, 6)])
        self.assertEqual(board.get_flippable_discs('black', 0, 7), [(1, 7), (2, 7)])
        self.assertEqual(board.get_flippable_discs('black', 4, 7), [(6, 5), (5, 6)])
        self.assertEqual(board.get_flippable_discs('black', 5, 7), [(6, 6), (6, 7)])

        # pattern5
        board._black_bitboard = 0xBF00000001000000
        board._white_bitboard = 0x007F7E7C78736500
        self.assertEqual(board.get_flippable_discs('black', 0, 2), [(1, 1)])
        self.assertEqual(board.get_flippable_discs('black', 7, 2), [(6, 1), (7, 1)])
        self.assertEqual(board.get_flippable_discs('black', 0, 3), [(2, 1), (1, 2)])
        self.assertEqual(board.get_flippable_discs('black', 6, 3), [(4, 1), (6, 1), (5, 2), (6, 2)])
        self.assertEqual(board.get_flippable_discs('black', 7, 3), [(5, 1), (6, 2)])
        self.assertEqual(board.get_flippable_discs('black', 0, 4), [(3, 1), (2, 2), (1, 3)])
        self.assertEqual(board.get_flippable_discs('black', 5, 4), [(5, 1), (5, 2), (5, 3)])
        self.assertEqual(board.get_flippable_discs('black', 6, 4), [(3, 1), (4, 2), (5, 3)])
        self.assertEqual(board.get_flippable_discs('black', 0, 5), [(4, 1), (3, 2), (2, 3), (1, 4)])
        self.assertEqual(board.get_flippable_discs('black', 4, 5), [(4, 1), (4, 2), (4, 3), (4, 4)])
        self.assertEqual(board.get_flippable_discs('black', 5, 5), [(1, 1), (2, 2), (3, 3), (4, 4)])
        self.assertEqual(board.get_flippable_discs('black', 0, 6), [(5, 1), (4, 2), (3, 3), (2, 4), (1, 5)])
        self.assertEqual(board.get_flippable_discs('black', 3, 6), [(3, 1), (3, 2), (3, 3), (3, 4), (3, 5)])
        self.assertEqual(board.get_flippable_discs('black', 0, 7), [(6, 1), (5, 2), (4, 3), (3, 4), (2, 5), (1, 6)])
        self.assertEqual(board.get_flippable_discs('black', 2, 7), [(2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6)])
        self.assertEqual(board.get_flippable_discs('black', 4, 7), [(6, 5), (5, 6)])
        self.assertEqual(board.get_flippable_discs('black', 7, 7), [(7, 5), (7, 6)])

        # pattern6
        board._black_bitboard = 0x8000808080808088
        board._white_bitboard = 0x007E7E7C78726446
        self.assertEqual(board.get_flippable_discs('black', 2, 0), [(1, 1)])
        self.assertEqual(board.get_flippable_discs('black', 3, 0), [(2, 1), (1, 2)])
        self.assertEqual(board.get_flippable_discs('black', 4, 0), [(3, 1), (2, 2), (1, 3)])
        self.assertEqual(board.get_flippable_discs('black', 5, 0), [(4, 1), (3, 2), (2, 3), (1, 4)])
        self.assertEqual(board.get_flippable_discs('black', 6, 0), [(5, 1), (4, 2), (3, 3), (2, 4), (1, 5)])
        self.assertEqual(board.get_flippable_discs('black', 7, 0), [(6, 1), (5, 2), (4, 3), (3, 4), (2, 5), (1, 6)])
        self.assertEqual(board.get_flippable_discs('black', 7, 2), [(1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2)])
        self.assertEqual(board.get_flippable_discs('black', 6, 3), [(1, 3), (2, 3), (3, 3), (4, 3), (5, 3)])
        self.assertEqual(board.get_flippable_discs('black', 5, 4), [(1, 4), (2, 4), (3, 4), (4, 4)])
        self.assertEqual(board.get_flippable_discs('black', 7, 4), [(6, 5), (5, 6)])
        self.assertEqual(board.get_flippable_discs('black', 4, 5), [(1, 5), (2, 5), (3, 5)])
        self.assertEqual(board.get_flippable_discs('black', 5, 5), [(1, 1), (2, 2), (3, 3), (4, 4)])
        self.assertEqual(board.get_flippable_discs('black', 3, 6), [(1, 4), (2, 5), (1, 6), (2, 6)])
        self.assertEqual(board.get_flippable_discs('black', 4, 6), [(1, 3), (2, 4), (3, 5)])
        self.assertEqual(board.get_flippable_discs('black', 2, 7), [(1, 6), (1, 7)])
        self.assertEqual(board.get_flippable_discs('black', 3, 7), [(1, 5), (2, 6)])
        self.assertEqual(board.get_flippable_discs('black', 7, 7), [(5, 7), (6, 7)])

        # pattern7
        board._black_bitboard = 0x0000000000081000
        board._white_bitboard = 0x0000001C1C140000
        self.assertEqual(board.get_flippable_discs('black', 3, 2), [(3, 3), (3, 4), (3, 5)])
        self.assertEqual(board.get_flippable_discs('black', 4, 2), [(4, 3), (4, 4)])
        self.assertEqual(board.get_flippable_discs('black', 2, 3), [(3, 4)])
        self.assertEqual(board.get_flippable_discs('black', 6, 3), [(5, 4)])
        self.assertEqual(board.get_flippable_discs('black', 2, 5), [(3, 5)])
        self.assertEqual(board.get_flippable_discs('black', 6, 5), [(5, 5)])

    def test_board_random_play(self):
        class TestPlayer(Player):
            def put_disc(self, board, bitboard):
                self.move = self.strategy.next_move(self.color, board)
                self.captures = board.put_disc(self.color, *self.move)
                self.captures = bitboard.put_disc(self.color, *self.move)

        class TestGame(Game):
            def __init__(self, unittest, board, bitboard, black_player, white_player, display, color='black', cancel=None):
                self.unittest = unittest
                self.board = board
                self.bitboard = bitboard
                self.black_player = black_player
                self.white_player = white_player
                self.players = [self.black_player, self.white_player] if color == 'black' else [self.white_player, self.black_player]
                self.display = display
                self.cancel = cancel
                self.result = []

            def play(self):
                if not self.result:
                    self.display.progress(self.board, self.black_player, self.white_player)

                    while True:
                        playable, foul_player = 0, None

                        for player in self.players:
                            # キャンセル許可時
                            if self.cancel:
                                if self.cancel.event.is_set():
                                    # キャンセルメニュー設定時は中断
                                    break

                            legal_moves1 = self.board.get_legal_moves(player.color)
                            legal_moves2 = self.bitboard.get_legal_moves(player.color)
                            self.unittest.assertEqual(legal_moves1, legal_moves2)

                            if not legal_moves1:
                                continue

                            self.display.turn(player, legal_moves1)

                            player.put_disc(self.board, self.bitboard)

                            self.display.move(player, legal_moves1)
                            self.display.progress(self.board, self.black_player, self.white_player)

                            if not player.captures:
                                foul_player = player
                                break

                            playable += 1

                        if foul_player:
                            self._foul(foul_player)
                            break

                        if not playable:
                            self._judge()
                            break

        for _ in range(5):
            board = Board()
            bitboard = BitBoard()
            black_player = TestPlayer('black', 'Random1', Random())
            white_player = TestPlayer('white', 'Random2', Random())
            game = TestGame(self, board, bitboard, black_player, white_player, NoneDisplay())
            game.play()

    def test_board_abstract(self):
        with self.assertRaises(TypeError):
            class Test(AbstractBoard):
                pass
            test = Test()

        with self.assertRaises(TypeError):
            class Test(AbstractBoard):
                def get_flippable_discs(self, color, x, y):
                    pass

                def put_disc(self, color, x, y):
                    pass

                def update_score(self):
                    pass

                def get_board_info(self):
                    pass

                def get_bitboard_info(self):
                    pass

                def undo(self):
                    pass

            test = Test()

        with self.assertRaises(TypeError):
            class Test(AbstractBoard):
                def get_legal_moves(self, color):
                    pass

                def put_disc(self, color, x, y):
                    pass

                def update_score(self):
                    pass

                def get_board_info(self):
                    pass

                def get_bitboard_info(self):
                    pass

                def undo(self):
                    pass

            test = Test()

        with self.assertRaises(TypeError):
            class Test(AbstractBoard):
                def get_legal_moves(self, color):
                    pass

                def get_flippable_discs(self, color, x, y):
                    pass

                def update_score(self):
                    pass

                def get_board_info(self):
                    pass

                def get_bitboard_info(self):
                    pass

                def undo(self):
                    pass

            test = Test()

        with self.assertRaises(TypeError):
            class Test(AbstractBoard):
                def get_legal_moves(self, color):
                    pass

                def get_flippable_discs(self, color, x, y):
                    pass

                def put_disc(self, color, x, y):
                    pass

                def get_board_info(self):
                    pass

                def get_bitboard_info(self):
                    pass

                def undo(self):
                    pass

            test = Test()

        with self.assertRaises(TypeError):
            class Test(AbstractBoard):
                def get_legal_moves(self, color):
                    pass

                def get_flippable_discs(self, color, x, y):
                    pass

                def put_disc(self, color, x, y):
                    pass

                def update_score(self):
                    pass

                def get_bitboard_info(self):
                    pass

                def undo(self):
                    pass

            test = Test()

        with self.assertRaises(TypeError):
            class Test(AbstractBoard):
                def get_legal_moves(self, color):
                    pass

                def get_flippable_discs(self, color, x, y):
                    pass

                def put_disc(self, color, x, y):
                    pass

                def update_score(self):
                    pass

                def get_board_info(self):
                    pass

                def undo(self):
                    pass

            test = Test()

        with self.assertRaises(TypeError):
            class Test(AbstractBoard):
                def get_legal_moves(self, color):
                    pass

                def get_flippable_discs(self, color, x, y):
                    pass

                def put_disc(self, color, x, y):
                    pass

                def update_score(self):
                    pass

                def get_board_info(self):
                    pass

                def get_bitboard_info(self):
                    pass

            test = Test()

        class Test(AbstractBoard):
            def get_legal_moves(self, color):
                pass

            def get_flippable_discs(self, color, x, y):
                pass

            def put_disc(self, color, x, y):
                pass

            def update_score(self):
                pass

            def get_board_info(self):
                pass

            def get_bitboard_info(self):
                pass

            def undo(self):
                pass

        test = Test()
        self.assertIsInstance(test, Test)
