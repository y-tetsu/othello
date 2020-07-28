"""RandomOpening strategy
"""

from reversi.strategies.common import Measure, AbstractStrategy
from reversi.strategies.easy import Random


class RandomOpening(AbstractStrategy):
    """RandomOpening
    """
    def __init__(self, depth=None, base=None):
        self.depth = depth
        self.random = Random()
        self.base = base

    @Measure.time
    def next_move(self, color, board):
        """next_move
        """
        depth = board._black_score + board._white_score - 4

        if depth < self.depth:
            return self.random.next_move(color, board)

        return self.base.next_move(color, board)
