#!/usr/bin/env python
"""
オセロゲーム
"""


class Game:
    """
    ゲームを管理する
    """
    BLACK_WIN, WHITE_WIN, DRAW = 0, 1, 2

    def __init__(self, board, black, white):
        self.board = board
        self.black = black
        self.white = white
        self.result = []

    def play(self):
        """
        ゲームを開始する
        """
        if not self.result:
            self.board.print_board()

            while True:
                cnt = 0

                for player in [self.black, self.white]:
                    if self.board.get_possibles(player.stone):
                        print("\n" + player.name + " の番です")

                        if player.put_stone(self.board):
                            move = "(" + chr(player.move[0] + 97) + ", " + str(player.move[1] + 1) + ")"
                            print(move + " に置きました")

                            self.board.print_board()
                            cnt += 1
                        else:
                            self.foul(player)
                            break

                if not cnt:
                    self.judge()
                    break

    def judge(self):
        """
        結果判定
        """
        if self.board.black_num > self.board.white_num:
            self.black_win()
        elif self.board.white_num > self.board.black_num:
            self.white_win()
        else:
            self.draw()

    def foul(self, player):
        """
        反則負け
        """
        if player.stone == self.black.stone:
            self.white_win()
        else:
            self.black_win()

    def black_win(self):
        """
        黒の勝ち
        """
        self.result = [Game.BLACK_WIN, self.board.black_num, self.board.white_num]
        print("\n" + self.black.name + " の勝ちです")

    def white_win(self):
        """
        白の勝ち
        """
        self.result = [Game.WHITE_WIN, self.board.black_num, self.board.white_num]
        print("\n" + self.white.name + " の勝ちです")

    def draw(self):
        """
        引き分け
        """
        self.result = [Game.DRAW, self.board.black_num, self.board.white_num]
        print("\n引き分けです")


if __name__ == '__main__':
    from board import Board
    from player import Player
    import strategies

    board = Board()
    black = Player(Board.BLACK, "BLACK:Max", strategies.Max())
    white = Player(Board.WHITE, "WHITE:Min", strategies.Min())

    game = Game(board, black, white)
    game.play()

    print(game.result)
