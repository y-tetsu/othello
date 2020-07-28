"""MonteCarlo
"""

import random
import copy

from reversi.game import Game
from reversi.player import Player
from reversi.display import NoneDisplay

from reversi.strategies.common import Timer, Measure, CPU_TIME, AbstractStrategy
from reversi.strategies.easy import Random


class MonteCarlo(AbstractStrategy):
    """
    MonteCarlo法で次の手を決める
    """
    def __init__(self, count=100, remain=60):
        self.count = count
        self.remain = remain  # モンテカルロ法開始手数
        self._black_player = Player('black', 'Random_B', Random())
        self._white_player = Player('white', 'Random_W', Random())

    @Measure.time
    @Timer.start(CPU_TIME, -10000000)
    def next_move(self, color, board):
        """
        次の一手
        """
        moves = board.get_legal_moves(color)              # 手の候補を取得
        scores = [0 for _ in range(len(moves))]           # スコアの初期化

        for _ in range(self.count):
            for i, move in enumerate(moves):
                scores[i] += self._playout(color, board, move)  # この手を選んだ時の勝敗を取得

                if Timer.is_timeout(self):
                    break
            if Timer.is_timeout(self):
                break

        best_score = max(scores)  # ベストスコアを取得
        best_moves = [move for i, move in enumerate(moves) if scores[i] == best_score]  # ベストスコアの手を選ぶ

        return random.choice(best_moves)  # 複数ある場合はランダムに選ぶ

    @Measure.countup
    @Timer.timeout
    def _playout(self, color, board, move):
        """
        終了までゲームを進めて勝敗を返す
        """
        remain = board.size * board.size - (board._black_score + board._white_score)

        if remain <= self.remain:
            playout_board = copy.deepcopy(board)  # 現在の盤面をコピー
            playout_board.put_disc(color, *move)  # 調べたい手を打つ

            # 勝敗が決まるまでゲームを進める
            next_color = 'white' if color == 'black' else 'black'  # 相手の色を調べる
            game = Game(playout_board, self._black_player, self._white_player, NoneDisplay(), next_color)
            game.play()

            # 結果を返す
            win, ret = Game.BLACK_WIN if color == 'black' else Game.WHITE_WIN, -1

            if game.result.winlose == win:
                ret = 1  # 勝った場合
            elif game.result.winlose == Game.DRAW:
                ret = 0  # 引き分けた場合
        else:
            ret = 0  # 盤面サイズが大きい場合は残り手数が減るまでしばらくランダムに打つ

        return ret
