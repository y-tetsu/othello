#!/usr/bin/env python
"""
反復深化法
"""

import sys
sys.path.append('../')

from strategies.common import Timer, Measure, AbstractStrategy
from strategies.alphabeta import AlphaBeta_TPW, AlphaBeta_TPWE
from strategies.negascout import NegaScout_TPW, NegaScout_TPW2, NegaScout_TPWE
from strategies.coordinator import Selector, Sorter_B


class IterativeDeepning(AbstractStrategy):
    """
    反復深化法
    """
    def __init__(self, depth=None, selector=None, sorter=None, search=None):
        self.depth = depth
        self.selector = selector
        self.sorter = sorter
        self.search = search
        self.max_depth = depth

    @Measure.time
    def next_move(self, color, board):
        """
        次の一手
        """
        depth, moves, best_move, scores, = self.depth, None, None, {}

        Timer.set_deadline(self.search.__class__.__name__, self.search._MIN)  # 探索クラスのタイムアウトを設定

        while True:
            moves = self.selector.select_moves(color, board, moves, scores, depth)                      # 次の手の候補を選択
            moves = self.sorter.sort_moves(color=color, board=board, moves=moves, best_move=best_move)  # 次の手の候補を並び替え
            best_move, scores = self.search.get_best_move(color, board, moves, depth)                   # 最善手を取得

            if Timer.is_timeout(self.search):  # タイムアウト発生時、処理を抜ける
                break

            depth += 1  # 読みの深さを増やす

        self.max_depth = depth  # 読んだ深さを記録

        return best_move


class AbI_B_TPW(IterativeDeepning):
    """
    AlphaBeta法に反復深化法を適用して次の手を決める(選択的探索:なし、並び替え:B、評価関数:TPW)
    """
    def __init__(self, depth=2, selector=Selector(), sorter=Sorter_B(), search=AlphaBeta_TPW()):
        super().__init__(depth, selector, sorter, search)


class AbI_B_TPWE(IterativeDeepning):
    """
    AlphaBeta法に反復深化法を適用して次の手を決める(選択的探索:なし、並び替え:B、評価関数:TPWE)
    """
    def __init__(self, depth=2, selector=Selector(), sorter=Sorter_B(), search=AlphaBeta_TPWE()):
        super().__init__(depth, selector, sorter, search)


class NsI_B_TPW(IterativeDeepning):
    """
    NegaScout法に反復深化法を適用して次の手を決める(選択的探索:なし、並び替え:B、評価関数:TPW)
    """
    def __init__(self, depth=2, selector=Selector(), sorter=Sorter_B(), search=NegaScout_TPW()):
        super().__init__(depth, selector, sorter, search)


class NsI_B_TPWE(IterativeDeepning):
    """
    NegaScout法に反復深化法を適用して次の手を決める(選択的探索:なし、並び替え:B、評価関数:TPWE)
    """
    def __init__(self, depth=2, selector=Selector(), sorter=Sorter_B(), search=NegaScout_TPWE()):
        super().__init__(depth, selector, sorter, search)


class NsI_B_TPW2(IterativeDeepning):
    """
    NegaScout法に反復深化法を適用して次の手を決める(選択的探索:なし、並び替え:B、評価関数:TPW2)
    """
    def __init__(self, depth=2, selector=Selector(), sorter=Sorter_B(), search=NegaScout_TPW2()):
        super().__init__(depth, selector, sorter, search)


if __name__ == '__main__':
    import time
    import os
    from board import BitBoard

    bitboard8 = BitBoard()
    bitboard8.put_stone('black', 3, 2)
    bitboard8.put_stone('white', 2, 4)
    bitboard8.put_stone('black', 5, 5)
    bitboard8.put_stone('white', 4, 2)
    bitboard8.put_stone('black', 5, 2)
    bitboard8.put_stone('white', 5, 4)
    print(bitboard8)

    print('--- Test For AbI_B_TPW Strategy ---')
    key = 'AlphaBeta_TPW' + str(os.getpid())
    iterative = AbI_B_TPW()
    assert iterative.depth == 2

    Measure.count[key] = 0
    print( iterative.next_move('black', bitboard8) )
    print( 'max_depth :', iterative.max_depth )
    assert iterative.max_depth >= 5
    print( 'count     :', Measure.count[key] )
    assert Measure.count[key] >= 1000
