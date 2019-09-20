#!/usr/bin/env python
"""
GUIウィンドウ
"""

import time
import tkinter as tk
import threading

from stone import StoneFactory
import board
from board import Board
import strategies


WINDOW_TITLE = 'othello'
WINDOW_WIDTH = 1360
WINDOW_HEIGHT = 680

TEXT_OFFSET_X = {'black': 200, 'white': 1150}
TEXT_OFFSET_Y = {'name': 80, 'score': 250, 'winlose': 400, 'turn': 500, 'move': 600}

OFFSET_START_X = 680
OFFSET_START_Y = 620

OFFSET_SQUARE_Y = 40
OFFSET_SQUARE_HEADER = 15

COLOR_GREEN = 'green'
COLOR_BLACK = 'black'
COLOR_WHITE = 'white'
COLOR_ORANGE = 'orange'
COLOR_YELLOW = 'yellow'
COLOR_RED = 'red'

TEXT_COLOR = {
    'name':    {'black': COLOR_BLACK,  'white': COLOR_WHITE},
    'score':   {'black': COLOR_BLACK,  'white': COLOR_WHITE},
    'winlose': {'black': COLOR_BLACK,  'white': COLOR_WHITE},
    'turn':    {'black': COLOR_ORANGE, 'white': COLOR_ORANGE},
    'move':    {'black': COLOR_BLACK,  'white': COLOR_WHITE},
}
TEXT_FONT_SIZE = {'name': 32, 'score': 140, 'winlose': 32, 'turn': 32, 'move': 32, 'start': 32}
SQUARE_HEADER_FONT_SIZE = 20

SQUARE_BOTTOM_MARGIN = 120
OVAL_SIZE_RATIO = 0.8
TURNOVAL_SIZE_DIVISOR = 10

MENU_NAME = {'size': 'Size', 'black': 'Black', 'white': 'White'}

START_TEXT = 'クリックでスタート'
STONE_MARK = '●'

TURN_STONE_WAIT = 0.1

DEFAULT_BOARD_SIZE = 8
DEFAULT_BLACK_NUM = "2"
DEFAULT_WHITE_NUM = "2"

DEFAULT_TEXT = {
    'name':    {'black': lambda s: STONE_MARK + s.player['black'], 'white': lambda s: STONE_MARK + s.player['white']},
    'score':   {'black': lambda s: '2',                            'white': lambda s: '2'                           },
    'winlose': {'black': lambda s: '',                             'white': lambda s: ''                            },
    'turn':    {'black': lambda s: '',                             'white': lambda s: ''                            },
    'move':    {'black': lambda s: '',                             'white': lambda s: ''                            },
}


class Window(tk.Frame):
    """
    ウィンドウ
    """
    def __init__(self, root=None, black_players=None, white_players=None):
        super().__init__(root)
        self.pack()

        # 初期設定
        self.size = DEFAULT_BOARD_SIZE
        self.player = {'black': black_players[0], 'white': white_players[0]}

        # ウィンドウ設定
        root.title(WINDOW_TITLE)                   # タイトル
        root.minsize(WINDOW_WIDTH, WINDOW_HEIGHT)  # 最小サイズ

        # メニューを配置
        self.menu = Menu(root, black_players, white_players)
        root.configure(menu=self.menu)

        # キャンバスを配置
        self.canvas = tk.Canvas(self, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg=COLOR_GREEN)
        self.canvas.grid(row=0, column=0)

    def init_screen(self):
        """
        ゲーム画面の初期化
        """
        self.canvas.delete('all')                         # 全オブジェクト削除
        self.board = ScreenBoard(self.size, self.canvas)  # ボード配置
        self.info = ScreenInfo(self.canvas, self.player)  # 情報表示テキスト配置
        self.start = ScreenStart(self.canvas)             # スタートテキスト配置

    def set_state(self, state):
        """
        ウィンドウを有効化/無効化
        """
        self.start.set_state(state)
        self.menu.set_state(state)


class ScreenBoard:
    """
    盤面表示
    """
    def __init__(self, size, canvas):
        self.size = size
        self.canvas = canvas
        self._squares = []
        self._xlines = []
        self._ylines = []
        self.move = None

        # イベント生成
        self.event = threading.Event()

        # 石情報
        self.stone ={}
        factory = StoneFactory()

        for color in ('black', 'white'):
            self.stone[color] = factory.create(color)

        self._calc_size()        # 変更後の石やマス目のサイズを計算
        self._draw_squares()     # マス目の描画
        self._put_init_stones()  # 初期位置に石を置く

    def _calc_size(self):
        """
        サイズ計算
        """
        self.square_y_ini = OFFSET_SQUARE_Y
        self.square_w = (WINDOW_HEIGHT - self.square_y_ini - SQUARE_BOTTOM_MARGIN) // self.size
        self.square_x_ini = WINDOW_WIDTH // 2 - (self.square_w * self.size) // 2

        self.oval_w1 = int(self.square_w * OVAL_SIZE_RATIO)
        self.oval_w2 = int(self.square_w // TURNOVAL_SIZE_DIVISOR)

    def _draw_squares(self):
        """
        マス目を描画
        """
        self._squares = [[None for _ in range(self.size)] for _ in range(self.size)]

        # 縦の番地
        x1, y1 = self.square_x_ini, self.square_y_ini
        for num in range(self.size):
            xlabel = chr(num + 97)
            x2 = x1 + self.square_w
            self.canvas.create_text((x1+x2)//2, y1-OFFSET_SQUARE_HEADER, fill=COLOR_WHITE, text=xlabel, font=('', SQUARE_HEADER_FONT_SIZE))
            x1 = x2

        # 縦線
        y1 = self.square_y_ini
        y2 = y1 + self.square_w * self.size
        for num in range(self.size + 1):
            x1 = self.square_x_ini + self.square_w * num
            xline = self.canvas.create_line(x1, y1, x1, y2, fill=COLOR_WHITE)
            self._xlines.append(xline)

        # 横の番地
        x1, y1 = self.square_x_ini, self.square_y_ini
        for num in range(self.size):
            ylabel = str(num + 1)
            y2 = y1 + self.square_w
            self.canvas.create_text(x1-OFFSET_SQUARE_HEADER, (y1+y2)//2, fill=COLOR_WHITE, text=ylabel, font=('', SQUARE_HEADER_FONT_SIZE))
            y1 = y2

        # 横線
        x1 = self.square_x_ini
        x2 = x1 + self.square_w * self.size
        for num in range(self.size + 1):
            y1 = self.square_y_ini + self.square_w * num
            yline = self.canvas.create_line(x1, y1, x2, y1, fill=COLOR_WHITE)
            self._ylines.append(yline)

    def _put_init_stones(self):
        """
        石を初期位置に置く
        """
        center = self.size // 2
        self.put_stone('black', center, center-1)
        self.put_stone('black', center-1, center)
        self.put_stone('white', center-1, center-1)
        self.put_stone('white', center, center)

    def put_stone(self, color, index_x, index_y):
        """
        石を置く
        """
        if color == 'black':
            self.put_black(index_x, index_y)
        elif color == 'white':
            self.put_white(index_x, index_y)

    def put_black(self, index_x, index_y):
        """
        黒を置く
        """
        label = self._get_label('black', index_x, index_y)

        x, y = self._get_coordinate(index_x, index_y)

        x1 = x - self.oval_w1/2
        y1 = y - self.oval_w1/2
        x2 = x + self.oval_w1/2
        y2 = y + self.oval_w1/2

        black_id = self.canvas.create_oval(x1, y1, x2, y2, tag=label, fill=COLOR_BLACK, outline=COLOR_BLACK)

    def put_white(self, index_x, index_y):
        """
        白を置く
        """
        label = self._get_label('white', index_x, index_y)

        x, y = self._get_coordinate(index_x, index_y)

        x1 = x - self.oval_w1/2
        y1 = y - self.oval_w1/2
        x2 = x + self.oval_w1/2
        y2 = y + self.oval_w1/2

        white_id = self.canvas.create_oval(x1, y1, x2, y2, tag=label, fill=COLOR_WHITE, outline=COLOR_WHITE)

    def put_turnblack(self, index_x, index_y):
        """
        黒をひっくり返す途中
        """
        label1 = self._get_label('turnblack1', index_x, index_y)
        label2 = self._get_label('turnblack2', index_x, index_y)

        x, y = self._get_coordinate(index_x, index_y)

        x1 = x - self.oval_w2
        y1 = y - self.oval_w1/2
        x2 = x
        y2 = y + self.oval_w1/2

        white_id = self.canvas.create_rectangle(x1, y1, x2, y2, tag=label1, fill=COLOR_WHITE, outline=COLOR_WHITE)

        x1 = x
        x2 = x + self.oval_w2
        black_id = self.canvas.create_rectangle(x1, y1, x2, y2, tag=label2, fill=COLOR_BLACK, outline=COLOR_BLACK)

    def put_turnwhite(self, index_x, index_y):
        """
        白をひっくり返す途中
        """
        label1 = self._get_label('turnwhite1', index_x, index_y)
        label2 = self._get_label('turnwhite2', index_x, index_y)

        x, y = self._get_coordinate(index_x, index_y)

        x1 = x - self.oval_w2
        y1 = y - self.oval_w1/2
        x2 = x
        y2 = y + self.oval_w1/2

        black_id = self.canvas.create_rectangle(x1, y1, x2, y2, tag=label1, fill=COLOR_BLACK, outline=COLOR_BLACK)

        x1 = x
        x2 = x + self.oval_w2
        white_id = self.canvas.create_rectangle(x1, y1, x2, y2, tag=label2, fill=COLOR_WHITE, outline=COLOR_WHITE)

    def remove_stone(self, color, index_x, index_y):
        """
        石を消す
        """
        ptns = []
        if color == 'black' or color == 'white':
            ptns = [color]
        else:
            ptns = [color + str(i) for i in range(1, 3)]

        for ptn in ptns:
            label = self._get_label(ptn, index_x, index_y)
            self.canvas.delete(label)

    def _get_coordinate(self, index_x, index_y):
        """
        座標を計算する
        """
        x_ini = self.square_x_ini
        y_ini = self.square_y_ini
        w = self.square_w

        return x_ini + w * index_x + w // 2, y_ini + w * index_y + w // 2

    def _get_label(self, name, x, y):
        """
        表示ラベルを返す
        """
        return name + "_" + chr(x + 97) + str(y + 1)

    def turn_stone(self, color, captures):
        """
        石をひっくり返す
        """
        if color == 'black':
            self.turn_black_stone(captures)
        elif color == 'white':
            self.turn_white_stone(captures)

    def turn_black_stone(self, captures):
        """
        白の石を黒の石にひっくり返す
        """
        # captures座標の白の石を消す
        for x, y in captures:
            self.remove_stone('white', x, y)

        # captures座標に白をひっくり返す途中の石を置く
        for x, y in captures:
            self.put_turnwhite(x, y)
        time.sleep(TURN_STONE_WAIT)

        # captures座標の白をひっくり返す途中の石を消す
        for x, y in captures:
            self.remove_stone('turnwhite', x, y)

        # capturesの石を黒にする
        for x, y in captures:
            self.put_black(x, y)
        time.sleep(TURN_STONE_WAIT)

    def turn_white_stone(self, captures):
        """
        黒の石を白の石にひっくり返す
        """
        # captures座標の黒の石を消す
        for x, y in captures:
            self.remove_stone('black', x, y)

        # captures座標に黒をひっくり返す途中の石を置く
        for x, y in captures:
            self.put_turnblack(x, y)
        time.sleep(TURN_STONE_WAIT)

        # captures座標の黒をひっくり返す途中の石を消す
        for x, y in captures:
            self.remove_stone('turnblack', x, y)

        # capturesの石を白にする
        for x, y in captures:
            self.put_white(x, y)
        time.sleep(TURN_STONE_WAIT)

    def enable_moves(self, moves):
        """
        打てる場所をハイライトする
        """
        for x, y in moves:
            x1 = self.square_x_ini + self.square_w * x
            x2 = x1 + self.square_w
            y1 = self.square_y_ini + self.square_w * y
            y2 = y1 + self.square_w
            self._squares[y][x] = self.canvas.create_rectangle(x1, y1, x2, y2, fill=COLOR_YELLOW, outline=COLOR_WHITE, tag='moves')

    def disable_moves(self, moves):
        """
        打てる場所のハイライトを元に戻す
        """
        self.canvas.delete('moves')

    def enable_move(self, x, y):
        """
        打った場所をハイライトする
        """
        x1 = self.square_x_ini + self.square_w * x
        x2 = x1 + self.square_w
        y1 = self.square_y_ini + self.square_w * y
        y2 = y1 + self.square_w
        self._squares[y][x] = self.canvas.create_rectangle(x1, y1, x2, y2, fill=COLOR_RED, outline=COLOR_WHITE, tag='move')

    def disable_move(self, x, y):
        """
        打った場所のハイライトを元に戻す
        """
        self.canvas.delete('move')

    def selectable_moves(self, moves):
        """
        打てる場所を選択できるようにする
        """
        for x, y in moves:
            square = self._squares[y][x]
            self.canvas.tag_bind(square, '<Enter>', self._enter_selectable_moves(square))
            self.canvas.tag_bind(square, '<Leave>', self._leave_selectable_moves(square))
            self.canvas.tag_bind(square, '<ButtonPress-1>', self._press_selectable_moves(x, y))

    def unselectable_moves(self, moves):
        """
        打てる場所を選択できないようにする
        """
        for x, y in moves:
            square = self._squares[y][x]
            self.canvas.tag_bind(square, '<Enter>', lambda *args: None)
            self.canvas.tag_bind(square, '<Leave>', lambda *args: None)
            self.canvas.tag_bind(square, '<ButtonPress-1>', lambda *args: None)

    def _enter_selectable_moves(self, square):
        """
        打てる場所にカーソルが合ったとき
        """
        def _enter(event):
            self.canvas.itemconfigure(square, fill=COLOR_RED)

        return _enter

    def _leave_selectable_moves(self, square):
        """
        打てる場所からカーソルが離れた
        """
        def _leave(event):
            self.canvas.itemconfigure(square, fill=COLOR_YELLOW)

        return _leave

    def _press_selectable_moves(self, x, y):
        """
        打てる場所をクリックしたとき
        """
        def _press(event):
            if not self.event.is_set():
                self.move = (x, y)
                self.event.set()  # ウィンドウへ手の選択を通知

        return _press


class ScreenInfo:
    """
    情報表示テキスト
    """
    def __init__(self, canvas, player):
        self.canvas = canvas
        self.player = player
        self.text = {}

        # テキスト作成
        for name in TEXT_OFFSET_Y.keys():
            for color in TEXT_OFFSET_X.keys():
                self._create_text(color, name)  # 表示テキスト

    def _create_text(self, color, name):
        """
        表示テキスト作成
        """
        self.text[color + "_" + name] = self.canvas.create_text(
            TEXT_OFFSET_X[color],
            TEXT_OFFSET_Y[name],
            text=DEFAULT_TEXT[name][color](self),
            font=('', TEXT_FONT_SIZE[name]),
            fill=TEXT_COLOR[name][color]
        )

    def set_text(self, color, name, text):
        """
        表示テキストの文字列を設定
        """
        text_id = self.text[color + "_" + name]
        self.canvas.itemconfigure(text_id, text=text)


class ScreenStart:
    """
    スタートテキスト
    """
    def __init__(self, canvas):
        self.canvas = canvas

        # テキスト作成
        self.text = canvas.create_text(
            OFFSET_START_X,
            OFFSET_START_Y,
            text=START_TEXT,
            font=('', TEXT_FONT_SIZE['start']),
            fill=COLOR_YELLOW
        )

        # イベント生成
        self.event = threading.Event()

        # マウスアクション登録
        canvas.tag_bind(self.text, '<Enter>', self._enter_start)
        canvas.tag_bind(self.text, '<Leave>', self._leave_start)
        canvas.tag_bind(self.text, '<ButtonPress-1>', self._on_start)

    def _enter_start(self, event):
        """
        カーソルが合った時
        """
        self.canvas.itemconfigure(self.text, fill=COLOR_RED)  # 赤色にする

    def _leave_start(self, event):
        """
        カーソルが離れた時
        """
        self.canvas.itemconfigure(self.text, fill=COLOR_YELLOW)  # 黄色にする

    def _on_start(self, event):
        """
        スタートテキストを押した場合
        """
        if not self.event.is_set():
            self.event.set()           # スタートイベントを通知

    def set_state(self, state):
        """
        スタートを有効化/無効化
        """
        text = START_TEXT if state == 'normal' else ''
        self.canvas.itemconfigure(self.text, text=text, state=state)


class Menu(tk.Menu):
    """
    メニュー
    """
    def __init__(self, root, black_players, white_players):
        super().__init__(root)

        self.size = DEFAULT_BOARD_SIZE
        self.black_player = black_players[0]
        self.white_player = white_players[0]

        # イベントの生成
        self.event = threading.Event()

        # メニューアイテムの生成
        menu_items = {
            'size': range(board.MIN_BOARD_SIZE, board.MAX_BOARD_SIZE + 1, 2),
            'black': black_players,
            'white': white_players,
        }
        self._create_menu_items(menu_items)

    def _create_menu_items(self, menu_items):
        """
        メニューの追加
        """
        for name, items in menu_items.items():
            menu = tk.Menu(self, tearoff=False)

            for item in items:
                menu.add_command(label=str(item), command=self._command(name, item))

            self.add_cascade(menu=menu, label=MENU_NAME[name])

    def _command(self, name, item):
        """
        メニュー設定変更時
        """
        def change_menu_selection():
            if not self.event.is_set():
                self.size = item if name == 'size' else self.size
                self.black_player = item if name == 'black' else self.black_player
                self.white_player= item if name == 'white' else self.white_player
                self.event.set()  # ウィンドウへメニューの設定変更を通知

        return change_menu_selection

    def set_state(self, state):
        """
        メニューのステータス設定(有効化/無効化)
        """
        for name in MENU_NAME.values():
            self.entryconfigure(name, state=state)


if __name__ == '__main__':
    import time
    from player import Player

    state = 'INIT'

    def resize_board(window):
        global state

        if window.menu.event.is_set():
            # メニューからの通知を取得
            window.size = window.menu.size
            window.player['black'] = window.menu.black_player
            window.player['white'] = window.menu.white_player

            state = 'INIT'  # ウィンドウ初期化
            window.menu.event.clear()   # イベントをクリア

            return True

        return False

    def test_play(window, game_strategies):
        global state

        demo = False

        while True:
            resize_board(window)

            if state == 'INIT':
                demo = False
                window.init_screen()
                window.set_state('normal')
                state = 'DEMO'

            if state == 'DEMO':
                demo = True
                resize_flag = False
                center = window.board.size // 2

                for x, y in [(center, center-1), (center-1, center)]:
                    if resize_board(window):
                        resize_flag = True
                        break

                    center = window.board.size // 2
                    time.sleep(TURN_STONE_WAIT)
                    window.board.remove_stone('black', x, y)
                    window.board.put_turnblack(x, y)

                    if resize_board(window):
                        resize_flag = True
                        break

                    center = window.board.size // 2
                    time.sleep(TURN_STONE_WAIT)
                    window.board.remove_stone('turnblack', x, y)
                    window.board.put_white(x, y)

                    if resize_board(window):
                        resize_flag = True
                        break

                    center = window.board.size // 2
                    time.sleep(TURN_STONE_WAIT)
                    window.board.remove_stone('white', x, y)
                    window.board.put_turnwhite(x, y)

                    if resize_board(window):
                        resize_flag = True
                        break

                    center = window.board.size // 2
                    time.sleep(TURN_STONE_WAIT)
                    window.board.remove_stone('turnwhite', x, y)
                    window.board.put_black(x, y)

                if not resize_flag:
                    center = window.board.size // 2

                    for x, y in [(center-1, center-1), (center, center)]:
                        if resize_board(window):
                            break

                        center = window.board.size // 2
                        time.sleep(TURN_STONE_WAIT)
                        window.board.remove_stone('white', x, y)
                        window.board.put_turnwhite(x, y)

                        if resize_board(window):
                            break

                        center = window.board.size // 2
                        time.sleep(TURN_STONE_WAIT)
                        window.board.remove_stone('turnwhite', x, y)
                        window.board.put_black(x, y)

                        if resize_board(window):
                            break

                        center = window.board.size // 2
                        time.sleep(TURN_STONE_WAIT)
                        window.board.remove_stone('black', x, y)
                        window.board.put_turnblack(x, y)

                        if resize_board(window):
                            break

                        center = window.board.size // 2
                        time.sleep(TURN_STONE_WAIT)
                        window.board.remove_stone('turnblack', x, y)
                        window.board.put_white(x, y)

                if window.start.event.is_set():
                    window.set_state('disable')  # メニューを無効化
                    window.start.event.clear()
                    state = 'START'

            if state == 'START':
                if not demo:
                    window.init_screen()
                    window.set_state('disable')

                demo = False
                print("start", window.board.size, window.info.player['black'], window.info.player['white'])

                board = Board(window.board.size)
                black_player = Player('black', window.info.player['black'], game_strategies[window.info.player['black']])
                white_player = Player('white', window.info.player['white'], game_strategies[window.info.player['white']])

                while True:
                    playable = 0

                    moves = list(board.get_possibles('black').keys())

                    if moves:
                        window.board.enable_moves(moves)
                        window.board.selectable_moves(moves)

                        time.sleep(0.3)
                        black_player.put_stone(board)

                        window.board.disable_moves(moves)
                        window.board.enable_move(*black_player.move)

                        window.board.put_stone('black', *black_player.move)

                        time.sleep(0.3)
                        window.board.turn_stone('black', black_player.captures)

                        window.board.disable_move(*black_player.move)

                        playable += 1

                    moves = list(board.get_possibles('white').keys())

                    if moves:
                        window.board.enable_moves(moves)

                        time.sleep(0.3)
                        white_player.put_stone(board)

                        window.board.disable_moves(moves)
                        window.board.enable_move(*white_player.move)

                        window.board.put_stone('white', *white_player.move)

                        time.sleep(0.3)
                        window.board.turn_stone('white', white_player.captures)
                        window.board.disable_move(*white_player.move)

                        playable += 1

                    if not playable:
                        state = 'END'
                        window.set_state('normal')
                        break

            if state == 'END':
                demo = False

                if window.start.event.is_set():
                    window.set_state('disable')
                    window.start.event.clear()
                    state = 'START'

    root = tk.Tk()
    root.withdraw()  # 表示が整うまで隠す

    b = ['ユーザ', 'かんたん', 'ふつう', 'むずかしい']
    w = ['ユーザ', 'かんたん', 'ふつう', 'むずかしい']

    window = Window(root=root, black_players=b, white_players=w)

    game_strategies = {
        'ユーザ': strategies.WindowUserInput(window),
        'かんたん': strategies.Unselfish(),
        'ふつう': strategies.Random(),
        'むずかしい': strategies.Greedy(),
    }

    game = threading.Thread(target=test_play, args=([window, game_strategies]))
    game.daemon = True
    game.start()

    root.deiconify()  # 表示する
    root.mainloop()
