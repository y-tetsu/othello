#!/usr/bin/env python
"""
定石打ち
"""

import sys
sys.path.append('../')

from strategies.common import CPU_TIME, AbstractStrategy
from strategies.timer import Timer
from strategies.measure import Measure
from strategies.fullreading import AbIF11_B_TPW, MultiNsF11


# ===== 定石リスト =====
# 兎定石
RABBIT = {
    #---------------------------------------------------------------------
    # 1手目
    # □□□□□□□□
    # □□□□□□□□
    # □□□□□□□□
    # □□□●〇□□□
    # □□□〇●◎□□
    # □□□□□□□□
    # □□□□□□□□
    # □□□□□□□□
    ('black', 0x0000000810000000, 0x0000001008000000): (5, 4),
    #---------------------------------------------------------------------
    # 2手目
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    # □□□□□□□□ □□□□◎□□□ □□□□□□□□ □□□〇□□□□
    # □□□●〇□□□ □□〇〇〇□□□ □□□●〇◎□□ □□□〇〇□□□
    # □□□〇〇〇□□ □□□〇●□□□ □□□〇〇□□□ □□◎〇●□□□
    # □□□◎□□□□ □□□□□□□□ □□□□〇□□□ □□□□□□□□
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    ('white', 0x000000081C000000, 0x0000001000000000): (3, 5),
    ('white', 0x0000003810000000, 0x0000000008000000): (4, 2),
    ('white', 0x0000000818080000, 0x0000001000000000): (5, 3),
    ('white', 0x0000101810000000, 0x0000000008000000): (2, 4),
    #---------------------------------------------------------------------
    # 3手目
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    # □□□□□□□□ □□□□●□□□ □□□□◎□□□ □□□〇□□□□
    # □□□●〇□□□ □□〇〇●◎□□ □□□●●●□□ □□□〇〇□□□
    # □□◎●〇〇□□ □□□〇●□□□ □□□〇〇□□□ □□●●●□□□
    # □□□●□□□□ □□□□□□□□ □□□□〇□□□ □□□◎□□□□
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    ('black', 0x000000080C000000, 0x0000001010100000): (2, 4),
    ('black', 0x0000003010000000, 0x0000080808000000): (5, 3),
    ('black', 0x0000000018080000, 0x0000001C00000000): (4, 2),
    ('black', 0x0000101800000000, 0x0000000038000000): (3, 5),
    #---------------------------------------------------------------------
    # 4手目
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    # □□□□□□□□ □□□□●□□□ □□□□〇□□□ □□□〇◎□□□
    # □□□●〇◎□□ □□〇〇〇〇□□ □□□●〇●□□ □□□〇〇□□□
    # □□〇〇〇〇□□ □□◎〇●□□□ □□□〇〇□□□ □□●〇●□□□
    # □□□●□□□□ □□□□□□□□ □□□◎〇□□□ □□□〇□□□□
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    ('white', 0x000000083C000000, 0x0000001000100000): (5, 3),
    ('white', 0x0000003C10000000, 0x0000080008000000): (2, 4),
    ('white', 0x0000080818080000, 0x0000001400000000): (3, 5),
    ('white', 0x0000101810100000, 0x0000000028000000): (4, 2),
    #---------------------------------------------------------------------
    # 5手目
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    # □□□□◎□□□ □□□□●□□□ □□□□〇□□□ □□□〇●□□□
    # □□□●●●□□ □□〇●〇〇□□ □□□●〇●□□ □□□●●◎□□
    # □□〇〇●〇□□ □□●●●□□□ □□◎●●□□□ □□●〇●□□□
    # □□□●□□□□ □□□◎□□□□ □□□●〇□□□ □□□〇□□□□
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    ('black', 0x0000000034000000, 0x0000001C08100000): (4, 2),
    ('black', 0x0000002C00000000, 0x0000081038000000): (3, 5),
    ('black', 0x0000080800080000, 0x0000001418100000): (2, 4),
    ('black', 0x0000100010100000, 0x0000081828000000): (5, 3),
}

# Sローズ基本形
SROSE = {
    #---------------------------------------------------------------------
    # 6手目
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    # □□□□〇□□□ □□□□●◎□□ □□□□〇◎□□ □□□〇●□□□
    # □□□〇●●□□ □□〇●〇〇□□ □□□〇〇●□□ □□□●●〇□□
    # □□〇〇●〇□□ □□●●〇□□□ □□〇●●□□□ □□●〇〇□□□
    # □□◎●□□□□ □□□〇□□□□ □□□●〇□□□ □□◎〇□□□□
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    ('white', 0x0000081034000000, 0x0000000C08100000): (2, 5),
    ('white', 0x0000002C08100000, 0x0000081030000000): (5, 2),
    ('white', 0x0000081820080000, 0x0000000418100000): (5, 2),
    ('white', 0x0000100418100000, 0x0000081820000000): (2, 5),
    #---------------------------------------------------------------------
    # 7手目
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    # □□□◎〇□□□ □□□□●●□□ □□□□〇●□□ □□□〇●□□□
    # □□□〇●●□□ □□〇●●〇□□ □□◎〇●●□□ □□□●●〇□□
    # □□〇●●〇□□ □□●●〇□□□ □□〇●●□□□ □□●●〇◎□□
    # □□●●□□□□ □□□〇◎□□□ □□□●〇□□□ □□●〇□□□□
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    ('black', 0x0000081024000000, 0x0000000C18300000): (3, 2),
    ('black', 0x0000002408100000, 0x00000C1830000000): (4, 5),
    ('black', 0x0000081020080000, 0x0000040C18100000): (2, 3),
    ('black', 0x0000100408100000, 0x0000081830200000): (5, 4),
    #---------------------------------------------------------------------
    # 8手目
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    # □□□〇〇□□□ □□◎□●●□□ □□□□〇●□□ □□◎〇●□□□
    # □□□〇〇●□□ □□〇●●〇□□ □□〇〇●●□□ □□□●〇〇□□
    # □□〇●●〇□□ □□●〇〇□□□ □□〇〇●□□□ □□●●〇〇□□
    # □□●●□◎□□ □□□〇〇□□□ □□□●〇◎□□ □□●〇□□□□
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    ('white', 0x0000181824000000, 0x0000000418300000): (5, 5),
    ('white', 0x0000002418180000, 0x00000C1820000000): (2, 2),
    ('white', 0x0000083030080000, 0x0000040C08100000): (5, 5),
    ('white', 0x0000100C0C100000, 0x0000081030200000): (2, 2),
    #---------------------------------------------------------------------
    # 9手目
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    # □□□〇〇□□□ □□●◎●●□□ □□□□〇●□□ □□●●●□□□
    # □□□〇〇●□□ □□●●●〇□□ □□〇〇●●□□ □□◎●〇〇□□
    # □□〇●●●□□ □□●〇〇□□□ □□〇〇●◎□□ □□●●〇〇□□
    # □□●●◎●□□ □□□〇〇□□□ □□□●●●□□ □□●〇□□□□
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    ('black', 0x0000181820000000, 0x000000041C340000): (4, 5),
    ('black', 0x0000000418180000, 0x00002C3820000000): (3, 2),
    ('black', 0x0000083030000000, 0x0000040C081C0000): (5, 4),
    ('black', 0x0000000C0C100000, 0x0000381030200000): (2, 3),
    #---------------------------------------------------------------------
    # 10手目
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    # □□□□□□□□ □□□□◎□□□ □□□□□□□□ □□□□□□□□
    # □□□〇〇□□□ □□●〇●●□□ □□□□〇●□□ □□●●●□□□
    # □□□〇〇●□□ □□●〇●〇□□ □□〇〇●●◎□ □□〇〇〇〇□□
    # □□〇●〇●□□ □□●〇〇□□□ □□〇〇〇〇□□ □◎●●〇〇□□
    # □□●●〇●□□ □□□〇〇□□□ □□□●●●□□ □□●〇□□□□
    # □□□◎□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    ('white', 0x0000181828080000, 0x0000000414340000): (3, 6),
    ('white', 0x0000101418180000, 0x00002C2820000000): (4, 1),
    ('white', 0x000008303C000000, 0x0000040C001C0000): (6, 3),
    ('white', 0x0000003C0C100000, 0x0000380030200000): (1, 4),
    #---------------------------------------------------------------------
    # 11手目
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    # □□□□□□□□ □□□□●□□□ □□□□□□□□ □□□□□◎□□
    # □□□〇〇□◎□ □□●●●●□□ □□□□〇●□□ □□●●●□□□
    # □□□〇〇●□□ □□●〇●〇□□ □□〇〇●●●□ □□●〇〇〇□□
    # □□〇●〇●□□ □□●〇〇□□□ □□〇〇〇●□□ □●●●〇〇□□
    # □□●●●●□□ □◎□〇〇□□□ □□□●●●□□ □□●〇□□□□
    # □□□●□□□□ □□□□□□□□ □□◎□□□□□ □□□□□□□□
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    ('black', 0x0000181828000000, 0x00000004143C1000): (6, 2),
    ('black', 0x0000001418180000, 0x00083C2820000000): (1, 5),
    ('black', 0x0000083038000000, 0x0000040E041C0000): (2, 6),
    ('black', 0x0000001C0C100000, 0x0000382070200000): (5, 1),
    #---------------------------------------------------------------------
    # 12手目
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    # □□□□□□□□ □□□□●□□□ □□□□□□□□ □□□□□〇□□
    # □□□〇〇□〇□ □□●●●●□□ □□□◎〇●□□ □□●●〇□□□
    # □□◎〇〇〇□□ □□●〇●〇□□ □□〇〇●●●□ □□●〇〇〇□□
    # □□〇●〇●□□ □□〇〇〇◎□□ □□〇〇〇●□□ □●●●〇〇□□
    # □□●●●●□□ □〇□〇〇□□□ □□□〇●●□□ □□●〇◎□□□
    # □□□●□□□□ □□□□□□□□ □□〇□□□□□ □□□□□□□□
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    ('white', 0x00001A1C28000000, 0x00000000143C1000): (2, 3),
    ('white', 0x0000001438580000, 0x00083C2800000000): (5, 4),
    ('white', 0x0000083038102000, 0x0000040E040C0000): (3, 2),
    ('white', 0x0004081C0C100000, 0x0000302070200000): (4, 5),
}

# 虎定石
TIGER = {
    #---------------------------------------------------------------------
    # 3手目
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    # □□◎□□□□□ □□□□●□□□ □□◎□□□□□ □□□〇□□□□
    # □□□●〇□□□ □□〇〇●□□□ □□□●●●□□ □□□〇〇□□□
    # □□□●〇〇□□ □□□〇●□□□ □□□〇〇□□□ □□●●●□□□
    # □□□●□□□□ □□□□□◎□□ □□□□〇□□□ □□□□□◎□□
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    # □□□□□□□□ □□□□□□□□ □□□□□□□□ □□□□□□□□
    ('black', 0x000000080C000000, 0x0000001010100000): (2, 2),
    ('black', 0x0000003010000000, 0x0000080808000000): (5, 5),
    ('black', 0x0000000018080000, 0x0000001C00000000): (2, 2),
    ('black', 0x0000101800000000, 0x0000000038000000): (5, 5),
}
# ===== 定石リスト =====


class Joseki(AbstractStrategy):
    """
    定石通りに打つ(8x8限定)
    """
    def __init__(self, base):
        self.joseki = {}
        self.base = base

        # 定石のロード
        self.joseki.update(RABBIT)  # 兎定石
        self.joseki.update(SROSE)   # Sローズ基本形
        self.joseki.update(TIGER)   # 虎定石

    @Measure.time
    def next_move(self, color, board):
        """
        次の一手
        """
        if board.size == 8:
            bitboard_b, bitboard_w = board.get_bitboard_info()
            key = (color, bitboard_b, bitboard_w)

            # 定石リストに手が含まれる場合
            if key in self.joseki:
                return self.joseki[key]

        return self.base.next_move(color, board)


class AbIF11J_B_TPW(Joseki):
    """
    AlphaBeta法に反復深化法を適用して次の手を決める+定石打ち
    (選択的探索:なし、並べ替え:B、評価関数:TPW, 完全読み開始:残り11手)
    """
    def __init__(self, base=AbIF11_B_TPW()):
        super().__init__(base)


class MultiNsF11J(Joseki):
    """
    MultiNegaScout+定石打ち
    (選択的探索:なし、並べ替え:B、評価関数:TPW, 完全読み開始:残り11手)
    """
    def __init__(self, base=MultiNsF11()):
        super().__init__(base)


if __name__ == '__main__':
    from board import BitBoard

    def rotate_180(bbits, wbits, move): # 180°回転
        bbits_tmp = [['0' for i in range(8)] for j in range(8)]
        wbits_tmp = [['0' for i in range(8)] for j in range(8)]

        check = 1 << 63
        for y in range(8):
            for x in range(8):
                if bbits & check:
                    bbits_tmp[y][x] = '1'
                if wbits & check:
                    wbits_tmp[y][x] = '1'
                check >>= 1

        import numpy as np

        bbits_tmp = np.rot90(np.rot90(np.array(bbits_tmp)))
        wbits_tmp = np.rot90(np.rot90(np.array(wbits_tmp)))
        bbits = int(''.join(bbits_tmp.flatten()), 2)
        wbits = int(''.join(wbits_tmp.flatten()), 2)
        move = 7 - move[0], 7 - move[1]

        return bbits, wbits, move

    def delta_swap(bits, mask, delta):
        x = (bits ^ (bits >> delta)) & mask
        return bits ^ x ^ (x << delta)

    def flip_diag(bbits, wbits, move): # 対角線を軸に反転
        bbits = delta_swap(bbits, 0x00000000F0F0F0F0, 28)
        bbits = delta_swap(bbits, 0x0000CCCC0000CCCC, 14)
        bbits = delta_swap(bbits, 0x00AA00AA00AA00AA,  7)
        wbits = delta_swap(wbits, 0x00000000F0F0F0F0, 28)
        wbits = delta_swap(wbits, 0x0000CCCC0000CCCC, 14)
        wbits = delta_swap(wbits, 0x00AA00AA00AA00AA,  7)
        move = move[1], move[0]
        return bbits, wbits, move

    def rotate_flip(color, b, w, move):
        print(f"    ('{color}', 0x{b:016X}, 0x{w:016X}): {move},")
        b2, w2, move2 = rotate_180(b, w, move)
        print(f"    ('{color}', 0x{b2:016X}, 0x{w2:016X}): {move2},")
        b3, w3, move3 = flip_diag(b, w, move)
        print(f"    ('{color}', 0x{b3:016X}, 0x{w3:016X}): {move3},")
        b4, w4, move4 = flip_diag(b2, w2, move2)
        print(f"    ('{color}', 0x{b4:016X}, 0x{w4:016X}): {move4},")


    print('--- Test For AbIF11J_B_TPW Strategy ---')
    joseki = AbIF11J_B_TPW()

    # 兎基本形
    bitboard8 = BitBoard()
    print(bitboard8)

    # 1手目
    move = joseki.next_move('black', bitboard8)
    print(move)
    bitboard8.put_stone('black', *move)
    print(bitboard8)

    # 2手目
    move = joseki.next_move('white', bitboard8)
    print(move)
    bitboard8.put_stone('white', *move)
    print(bitboard8)

    # 3手目
    move = joseki.next_move('black', bitboard8)
    print(move)
    bitboard8.put_stone('black', *move)
    print(bitboard8)

    # 4手目
    move = joseki.next_move('white', bitboard8)
    print(move)
    bitboard8.put_stone('white', *move)
    print(bitboard8)

    # 5手目
    move = joseki.next_move('black', bitboard8)
    print(move)
    bitboard8.put_stone('black', *move)
    print(bitboard8)

    # Sローズ基本形
    # 6手目
    move = joseki.next_move('white', bitboard8)
    print(move)
    bitboard8.put_stone('white', *move)
    print(bitboard8)

    # 7手目
    move = joseki.next_move('black', bitboard8)
    print(move)
    bitboard8.put_stone('black', *move)
    print(bitboard8)

    # 8手目
    move = joseki.next_move('white', bitboard8)
    print(move)
    bitboard8.put_stone('white', *move)
    print(bitboard8)

    # 9手目
    move = joseki.next_move('black', bitboard8)
    print(move)
    bitboard8.put_stone('black', *move)
    print(bitboard8)

    # 10手目
    move = joseki.next_move('white', bitboard8)
    print(move)
    bitboard8.put_stone('white', *move)
    print(bitboard8)

    # 11手目
    move = joseki.next_move('black', bitboard8)
    print(move)
    bitboard8.put_stone('black', *move)
    print(bitboard8)

    # 12手目
    move = joseki.next_move('white', bitboard8)
    print(move)
    bitboard8.put_stone('white', *move)
    print(bitboard8)

    # 虎基本形
    bitboard8 = BitBoard()
    print(bitboard8)

    # 1手目
    move = joseki.next_move('black', bitboard8)
    print(move)
    bitboard8.put_stone('black', *move)
    print(bitboard8)

    # 2手目
    move = joseki.next_move('white', bitboard8)
    print(move)
    bitboard8.put_stone('white', *move)
    print(bitboard8)

    # 3手目
    move = joseki.next_move('black', bitboard8)
    print(move)
    bitboard8.put_stone('black', *move)
    print(bitboard8)

    #-----------------------------------#
    #color, move = 'black', (2, 2)
    #b, w =  bitboard8.get_bitboard_info()
    #rotate_flip(color, b, w, move)
    #-----------------------------------#
