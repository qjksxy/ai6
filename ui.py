import tkinter as tk
import os
import time
import copy
import random

# 定义常量
MAP_SIZE = 15       # 定义地图尺寸
PIX_SIZE = 30       # 像素尺寸
WIN_SET = 6         # 连子个数
BLANK_CODE = 0      # 空白编号
WHITE_CODE = -1     # 白棋
BLACK_CODE = 1      # 黑棋
CANT_CHESS = -10    # 无法在指定位置落子
NOT_WIN = 0
BLACK_WIN = 1
WHITE_WIN = -1
DRAW = 2

# 定义窗口
top = tk.Tk()
top.title("六子棋X")
top.geometry('1200x1200')
turn_counter = 0    # 保存当前为第几手
game_is_over = False
is_turn_black = True
chesses_count = 0
# 棋子列表
child_map = []
board = []
# 定义画布
canvas = tk.Canvas(top, height=MAP_SIZE * PIX_SIZE, width=MAP_SIZE * PIX_SIZE, bg ="gray")

def canvas_init():
    global canvas
    canvas.pack(pady=10)
    for i in range(MAP_SIZE):
        canvas.create_line(i * PIX_SIZE, 0, i * PIX_SIZE, MAP_SIZE * PIX_SIZE, fill='black')
        canvas.create_line(0, i * PIX_SIZE, MAP_SIZE * PIX_SIZE, i * PIX_SIZE, fill='black')
    for i in range(MAP_SIZE * MAP_SIZE):
        board.append(BLANK_CODE)
    restart()
    add_btn('自动训练', re_auto_play)
    add_btn('自动走1次', auto_play_once_btn)
    add_btn('开始游戏/重新开始', start_game_btn)
    canvas.bind("<Button-1>", touch_canvas)

def get_board(x, y):
    return board[y * MAP_SIZE + x]

def get_board_safe(x, y):
    if x < 0 or y < 0 or x >= MAP_SIZE or y >= MAP_SIZE:
        return BLANK_CODE
    else:
        return get_board(x, y)

def set_board(x, y, value):
    global board
    board[y * MAP_SIZE + x] = value

def restart():
    global game_is_over, is_turn_black, turn_counter, chesses_count
    for child in child_map:
        canvas.delete(child)
    child_map.clear()
    chesses_count = 0
    turn_counter = 0
    game_is_over = False
    is_turn_black = True
    for i in range(MAP_SIZE * MAP_SIZE):
        board[i] = BLANK_CODE
    # 下第一子
    chess(MAP_SIZE // 2, MAP_SIZE // 2, 0)
    is_turn_black = False
    turn_counter = 0

def touch_canvas(event):
    global is_turn_black, turn_counter
    # 获取 x y 坐标
    x = event.x // PIX_SIZE
    y = event.y // PIX_SIZE
    if x >= MAP_SIZE or y >= MAP_SIZE or get_board(x, y) != BLANK_CODE:
        return
    res = chess(x, y, 0)

def chess(x, y, score):
    global is_turn_black, chesses_count
    global turn_counter
    if game_is_over or get_board(x, y) != BLANK_CODE:
        return CANT_CHESS
    if is_turn_black:
        fill_color = 'black'
        set_board(x, y, BLACK_CODE)
    else:
        fill_color = 'white'
        set_board(x, y, WHITE_CODE)
    child = canvas.create_oval(x * PIX_SIZE,
                               y * PIX_SIZE,
                               x * PIX_SIZE + PIX_SIZE,
                               y * PIX_SIZE + PIX_SIZE, fill=fill_color)
    child_map.append(child)
    chesses_count += 1
    # 连下两子交换颜色
    if turn_counter < 1:
        turn_counter = turn_counter + 1
    else:
        is_turn_black = not is_turn_black
        turn_counter = 0
    return judge_result(x, y)

def win(flag):
    global game_is_over
    game_is_over = True
    print("-----Game end-----")
    win_str = 'in function ui.win: ERROR'
    if flag == BLACK_WIN:
        win_str = '黑棋获胜'
    if flag == WHITE_WIN:
        win_str = '白棋获胜'
    if flag == DRAW:
        win_str = '平局'
    print(win_str)
    return flag

def judge_result(x, y):
    global game_is_over
    if chesses_count == MAP_SIZE * MAP_SIZE:
        return win(DRAW)
    len = 0
    curr_col = BLANK_CODE
    for i in range(11):
        col = get_board_safe(x - 5 + i, y)
        if col != BLANK_CODE and col == curr_col:
            len += 1
            if len >= 6:
                return win(col)
        if col != curr_col:
            len = 1
            curr_col = col
    len = 0
    curr_col = BLANK_CODE
    for i in range(11):
        col = get_board_safe(x, y - 5 + i)
        if col != BLANK_CODE and col == curr_col:
            len += 1
            if len >= 6:
                return win(col)
        if col != curr_col:
            len = 1
            curr_col = col
    len = 0
    curr_col = BLANK_CODE
    for i in range(11):
        col = get_board_safe(x - 5 + i, y - 5 + i)
        if col != BLANK_CODE and col == curr_col:
            len += 1
            if len >= 6:
                return win(col)
        if col != curr_col:
            len = 1
            curr_col = col
    len = 0
    curr_col = BLANK_CODE
    for i in range(11):
        col = get_board_safe(x + 5 - i, y - 5 + i)
        if col != BLANK_CODE and col == curr_col:
            len += 1
            if len >= 6:
                return win(col)
        if col != curr_col:
            len = 1
            curr_col = col
    return 0

# 添加按钮
def re_auto_play():
    auto_play = 10
    restart()
    while auto_play > 0:
        print('auto_play: ' + str(auto_play))
        while not game_is_over:
            auto_play_once_btn()
        auto_play -= 1

# 添加按钮  -- AI 进入下棋
def auto_play_once_btn():
    i = 0
    res = CANT_CHESS
    while i < 20 and res == CANT_CHESS:
        x = random.randint(0, MAP_SIZE - 1)
        y = random.randint(0, MAP_SIZE - 1)
        res = chess(x, y, 0)
        i += 1

# 添加按钮  -- 开始游戏
def start_game_btn():
    restart()
    pass

# 显示游戏窗口
def show_windows():
    top.mainloop()

def add_btn(_text, _command):
    button = tk.Button(top, text=_text, command=_command)
    button.pack()

if __name__ == '__main__':
    canvas_init()
    show_windows()