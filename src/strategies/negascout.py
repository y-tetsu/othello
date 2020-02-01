#!/usr/bin/env python
"""
ネガスカウト法
"""

import sys
sys.path.append('../')

from strategies.common import Timer, Measure, CPU_TIME
from strategies.alphabeta import AlphaBeta
from strategies.coordinator import Evaluator_TPW, Evaluator_TPOW


class NegaScout(AlphaBeta):
    """
    NegaScout法で次の手を決める
    """
    @Measure.countup
    @Timer.timeout
    def _get_score(self, color, board, alpha, beta, depth):
        """
        評価値の取得
        """
        # ゲーム終了 or 最大深さに到達
        possibles_b = board.get_possibles('black', True)
        possibles_w = board.get_possibles('white', True)
        is_game_end =  True if not possibles_b and not possibles_w else False

        if is_game_end or depth <= 0:
            sign = 1 if color == 'black' else -1
            return self.evaluator.evaluate(color=color, board=board, possibles_b=possibles_b, possibles_w=possibles_w) * sign

        # パスの場合
        possibles = possibles_b if color == 'black' else possibles_w
        next_color = 'white' if color == 'black' else 'black'

        if not possibles:
            return -self._get_score(next_color, board, -beta, -alpha, depth)

        # 手の候補
        moves = list(board.get_possibles(color).keys())

        # NegaScout法
        tmp, null_window = None, beta
        for i, move in enumerate(moves):
            if alpha < beta:
                board.put_stone(color, *move)
                tmp = -self._get_score(next_color, board, -null_window, -alpha, depth-1)
                board.undo()

                if alpha < tmp:
                    if tmp <= null_window and i:
                        board.put_stone(color, *move)
                        alpha = -self._get_score(next_color, board, -beta, -tmp, depth-1)
                        board.undo()

                        if Timer.is_timeout(self):
                            return alpha
                    else:
                        alpha = tmp

                null_window = alpha + 1
            else:
                break

        return alpha


class NegaScout_TPW(NegaScout):
    """
    NegaScout法でEvaluator_TPWにより次の手を決める
    """
    def __init__(self, evaluator=Evaluator_TPW()):
        super().__init__(evaluator=evaluator)


class NegaScout3_TPW(NegaScout):
    """
    NegaScout法でEvaluator_TPWにより次の手を決める(3手読み)
    """
    def __init__(self, depth=3, evaluator=Evaluator_TPW()):
        super().__init__(depth, evaluator)


class NegaScout3_TPOW(NegaScout):
    """
    NegaScout法でEvaluator_TPOWにより次の手を決める(3手読み)
    """
    def __init__(self, depth=3, evaluator=Evaluator_TPOW()):
        super().__init__(depth, evaluator)


class NegaScout4_TPW(NegaScout):
    """
    NegaScout法でEvaluator_TPWにより次の手を決める(4手読み)
    """
    def __init__(self, depth=4, evaluator=Evaluator_TPW()):
        super().__init__(depth, evaluator)


class NegaScout4_TPOW(NegaScout):
    """
    NegaScout法でEvaluator_TPOWにより次の手を決める(4手読み)
    """
    def __init__(self, depth=4, evaluator=Evaluator_TPOW()):
        super().__init__(depth, evaluator)


if __name__ == '__main__':
    import time
    import os
    from board import BitBoard

    # NegaScout
    print('--- Test For NegaScout Strategy ---')
    negascout = NegaScout4_TPW()

    assert negascout.depth == 4

    bitboard8 = BitBoard(8)
    bitboard8.put_stone('black', 3, 2)

    key = negascout.__class__.__name__ + str(os.getpid())

    Measure.count[key] = 0
    Timer.timeout_flag[key] = False
    Timer.deadline[key] = time.time() + CPU_TIME
    score = negascout._get_score('white', bitboard8, -10000000, 10000000, 2)
    print(score)
    print(Measure.count[key])
    assert score == -13
    assert Measure.count[key] == 22

    Measure.count[key] = 0
    Timer.timeout_flag[key] = False
    Timer.deadline[key] = time.time() + CPU_TIME
    score = negascout._get_score('white', bitboard8, -10000000, 10000000, 3)
    print(score)
    print(Measure.count[key])
    assert score == 4
    assert Measure.count[key] == 114

    Measure.count[key] = 0
    Timer.timeout_flag[key] = False
    Timer.deadline[key] = time.time() + CPU_TIME
    score = negascout._get_score('white', bitboard8, -10000000, 10000000, 4)
    print(score)
    print(Measure.count[key])
    assert score == -9
    assert Measure.count[key] == 534

    Measure.count[key] = 0
    Timer.timeout_flag[key] = False
    Timer.deadline[key] = time.time() + 1
    score = negascout._get_score('white', bitboard8, -10000000, 10000000, 5)
    print(score)
    print(Measure.count[key])
    assert score == 1
    assert Measure.count[key] == 641

    Measure.count[key] = 0
    Timer.timeout_flag[key] = False
    Timer.deadline[key] = time.time() + 3
    score = negascout._get_score('white', bitboard8, -10000000, 10000000, 6)
    print(score)
    print(Measure.count[key])
    assert score == -5
    assert Measure.count[key] == 2273

    print(bitboard8)
    assert negascout.next_move('white', bitboard8) == (2, 4)

    print('* black check')
    bitboard8.put_stone('white', 2, 4)
    bitboard8.put_stone('black', 5, 5)
    bitboard8.put_stone('white', 4, 2)
    bitboard8.put_stone('black', 5, 2)
    bitboard8.put_stone('white', 5, 4)
    print(bitboard8)

    Measure.count[key] = 0
    Timer.timeout_flag[key] = False
    Timer.deadline[key] = time.time() + 3
    assert negascout.next_move('black', bitboard8) == (5, 3)
    print(Measure.count[key])
    assert Measure.count[key] == 1043

    Measure.count[key] = 0
    negascout.depth = 2
    Timer.timeout_flag[key] = False
    Timer.deadline[key] = time.time() + 3
    assert negascout.next_move('black', bitboard8) == (2, 2)
    print(Measure.count[key])
    assert Measure.count[key] == 27

    Timer.timeout_flag[key] = False
    Timer.deadline[key] = time.time() + 3
    Measure.count[key] = 0
    moves = bitboard8.get_possibles('black').keys()  # 手の候補
    best_move = negascout.get_best_move('black', bitboard8, moves, 5)
    print( best_move )
    print( Measure.count[key] )
    assert best_move == ((2, 2), {(2, 2): 8, (2, 3): 8, (5, 3): 8, (1, 5): 8, (2, 5): 8, (3, 5): 8, (4, 5): 8, (6, 5): 8})

    Timer.timeout_flag[key] = False
    Timer.deadline[key] = time.time() + 0.5
    Measure.count[key] = 0
    moves = bitboard8.get_possibles('black').keys()  # 手の候補
    best_move = negascout.get_best_move('black', bitboard8, moves, 4)
    print( best_move )
    print( Measure.count[key] )
    assert best_move == ((5, 3), {(2, 2): -2, (2, 3): 0, (5, 3): 2, (1, 5): 2, (2, 5): 2, (3, 5): 2, (4, 5): 2, (6, 5): 2})
