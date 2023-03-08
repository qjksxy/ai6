import tkinter as tk
import os
import time
import copy
import random

# 定义常量
MAP_SIZE = 15       # 定义地图尺寸
PIX_SIZE = 30       # 像素尺寸
WIN_SET = 6         # 连子个数
BLANK = 0           # 空白编号
WHITE = -1          # 白棋
BLACK = 1           # 黑棋
CANT_CHESS = -10    # 发生错误：落子失败
NOT_WIN = 0
BLACK_WIN = 1
WHITE_WIN = -1
DRAW = 2
CHESSABLE = 1
NOCHESSABLE = 0
SUCCESS = 1
ERROR = 0
# 奖励分数
SING4 = 1
SING5 = 1
DOUB2 = 1
DOUB3 = 1
DOUB4 = 1
DOUB5 = 1
CONN6 = 1


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
chessable = []
# 设置是否显示图形界面
no_gui = True
# 定义画布
canvas = tk.Canvas(top, height=MAP_SIZE * PIX_SIZE, width=MAP_SIZE * PIX_SIZE, bg ="gray")

def canvas_init():
    global canvas, no_gui
    no_gui = False
    canvas.pack(pady=10)
    for i in range(MAP_SIZE):
        canvas.create_line(i * PIX_SIZE, 0, i * PIX_SIZE, MAP_SIZE * PIX_SIZE, fill='black')
        canvas.create_line(0, i * PIX_SIZE, MAP_SIZE * PIX_SIZE, i * PIX_SIZE, fill='black')
    for i in range(MAP_SIZE * MAP_SIZE):
        board.append(BLANK)
        chessable.append(NOCHESSABLE)
    restart()
    add_btn('自动训练', re_auto_play)
    add_btn('自动走1次', auto_play_once_btn)
    add_btn('开始游戏/重新开始', start_game_btn)
    canvas.bind("<Button-1>", touch_canvas)

def get_board(x, y):
    return board[y * MAP_SIZE + x]

def get_board_safe(x, y):
    if x < 0 or y < 0 or x >= MAP_SIZE or y >= MAP_SIZE:
        return BLANK
    else:
        return get_board(x, y)

def set_board(x, y, value):
    global board
    board[y * MAP_SIZE + x] = value

def set_chessable(x, y):
    global chessable
    for i in range(5):
        for j in range(5):
            _x = x - 2 + i
            _y = y - 2 + j
            if _x < 0 or _y < 0 or _x >= MAP_SIZE or _y >= MAP_SIZE:
                continue
            chessable[_y * MAP_SIZE + _x] = CHESSABLE
    chessable[y * MAP_SIZE + x] = NOCHESSABLE

def get_chessable(x, y):
    if x < 0 or y < 0 or x >= MAP_SIZE or y >= MAP_SIZE:
        return NOCHESSABLE
    return chessable[y * MAP_SIZE + x]

def restart():
    global game_is_over, is_turn_black, turn_counter, chesses_count
    if not no_gui:
        for child in child_map:
            canvas.delete(child)
    child_map.clear()
    chesses_count = 0
    turn_counter = 0
    game_is_over = False
    is_turn_black = True
    for i in range(MAP_SIZE * MAP_SIZE):
        board[i] = BLANK
    # 下第一子
    chess(MAP_SIZE // 2, MAP_SIZE // 2, 0)
    is_turn_black = False
    turn_counter = 0

def touch_canvas(event):
    global is_turn_black, turn_counter
    # 获取 x y 坐标
    x = event.x // PIX_SIZE
    y = event.y // PIX_SIZE
    if x >= MAP_SIZE or y >= MAP_SIZE or get_board(x, y) != BLANK:
        return
    chess(x, y, 0)

def chess(x, y, score):
    global is_turn_black, chesses_count
    global turn_counter
    if game_is_over or get_board(x, y) != BLANK:
        return CANT_CHESS
    if is_turn_black:
        fill_color = 'black'
        set_board(x, y, BLACK)
    else:
        fill_color = 'white'
        set_board(x, y, WHITE)
    if not no_gui:
        child = canvas.create_oval(x * PIX_SIZE,
                                   y * PIX_SIZE,
                                   x * PIX_SIZE + PIX_SIZE,
                                   y * PIX_SIZE + PIX_SIZE, fill=fill_color)
        child_map.append(child)
    chesses_count += 1
    set_chessable(x, y)
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
    curr_col = BLANK
    for i in range(11):
        col = get_board_safe(x - 5 + i, y)
        if col != BLANK and col == curr_col:
            len += 1
            if len >= 6:
                return win(col)
        if col != curr_col:
            len = 1
            curr_col = col
    len = 0
    curr_col = BLANK
    for i in range(11):
        col = get_board_safe(x, y - 5 + i)
        if col != BLANK and col == curr_col:
            len += 1
            if len >= 6:
                return win(col)
        if col != curr_col:
            len = 1
            curr_col = col
    len = 0
    curr_col = BLANK
    for i in range(11):
        col = get_board_safe(x - 5 + i, y - 5 + i)
        if col != BLANK and col == curr_col:
            len += 1
            if len >= 6:
                return win(col)
        if col != curr_col:
            len = 1
            curr_col = col
    len = 0
    curr_col = BLANK
    for i in range(11):
        col = get_board_safe(x + 5 - i, y - 5 + i)
        if col != BLANK and col == curr_col:
            len += 1
            if len >= 6:
                return win(col)
        if col != curr_col:
            len = 1
            curr_col = col
    return 0

def _equals1(x):
    if x == 1:
        return 1
    else:
        return 0

def get_state():
    me = [_equals1(x) for x in board]
    co = [_equals1(-1 * x) for x in board]
    me.extend(co)
    me.extend(chessable)
    return me

def check_reward(chess_list):
    return 0

def reward(camp):
    player1 = camp
    player2 = 1 - camp
    board1 = []
    board2 = []
    reward = 0
    if camp == WHITE:
        board1 = [-1 * x for x in board]
        board2 = board
        player2 = BLACK
    else:
        board1 = board
        board2 = [-1 * x for x in board]
        player2 = WHITE
    # 分片
    head = -1
    tail = -1
    # 检查所有横行
    for j in range(MAP_SIZE):
        for i in range(MAP_SIZE):
            if get_board(j, i) == player2:
                tail = i
                if tail - head + 1 < WIN_SET:
                    head = tail
                    continue
                else:
                    # 从 board[j][head] 到 board[j][tail] 检查奖励布局
                    l = []
                    for m in range(head+1, tail-1):
                        l.append(get_board(j, m) * player1)
                    reward += check_reward(l)
        if MAP_SIZE - tail + 1 < WIN_SET:
            continue
        else:
            # 从 board[j][tail] 到 board[j][MAP_SIZE] 检查奖励布局
            l = []
            for m in range(tail + 1, MAP_SIZE - 1):
                l.append(get_board(j, m) * player1)
            reward += check_reward(l)
    # 检查所有竖列
    head, tail = -1, -1
    for j in range(MAP_SIZE):
        for i in range(MAP_SIZE):
            if get_board(i, j) == player2:
                tail = i
                if tail - head + 1 < WIN_SET:
                    head = tail
                    continue
                else:
                    # 从 board[head][j] 到 board[tail][j] 检查奖励布局
                    l = []
                    for m in range(head+1, tail-1):
                        l.append(get_board(m, j) * player1)
                    reward += check_reward(l)
        if MAP_SIZE - tail + 1 < WIN_SET:
            continue
        else:
            # 从 board[tail][j] 到 board[MAP_SIZE][j] 检查奖励布局
            l = []
            for m in range(tail + 1, MAP_SIZE - 1):
                l.append(get_board(m, j) * player1)
            reward += check_reward(l)
    # 检查所有左上-右下斜线
    # 右上部分棋盘
    head, tail = -1, -1
    for j in range(MAP_SIZE):
        for i in range(MAP_SIZE - j):
            if get_board(j + i, i) == player2:
                tail = i
                if tail - head + 1 < WIN_SET:
                    head = tail
                    continue
                else:
                    # 从 board[j][head] 到 board[j][tail] 检查奖励布局
                    l = []
                    for m in range(head + 1, tail - 1):
                        l.append(get_board(j + m, m) * player1)
                    reward += check_reward(l)
        if MAP_SIZE - j - tail + 1 < WIN_SET:
            continue
        else:
            l = []
            for m in range(tail + 1, MAP_SIZE - 1):
                l.append(get_board(j + m, m) * player1)
            reward += check_reward(l)
    # 检查左下部分棋盘
    head, tail = -1, -1
    for j in range(MAP_SIZE):
        for i in range(MAP_SIZE - j):
            if get_board(i, j + i) == player2:
                tail = i
                if tail - head + 1 < WIN_SET:
                    head = tail
                    continue
                else:
                    # 从 board[j][head] 到 board[j][tail] 检查奖励布局
                    l = []
                    for m in range(head + 1, tail - 1):
                        l.append(get_board(m, j + m) * player1)
                    reward += check_reward(l)
        if MAP_SIZE - j - tail + 1 < WIN_SET:
            continue
        else:
            l = []
            for m in range(tail + 1, MAP_SIZE - 1):
                l.append(get_board(m, j + m) * player1)
            reward += check_reward(l)
    # 检查所有右上-左下斜线
    # 检查左上部分棋盘
    head, tail = -1, -1
    for j in range(MAP_SIZE):
        for i in range(j + 1):
            if get_board(j - i, i) == player2:
                tail = i
                if tail - head + 1 < WIN_SET:
                    head = tail
                    continue
                else:
                    # 从 board[j][head] 到 board[j][tail] 检查奖励布局
                    l = []
                    for m in range(head + 1, tail - 1):
                        l.append(get_board(j - m, m) * player1)
                    reward += check_reward(l)
        if MAP_SIZE - j - tail + 1 < WIN_SET:
            continue
        else:
            l = []
            for m in range(tail + 1, MAP_SIZE - 1):
                l.append(get_board(j - m, m) * player1)
            reward += check_reward(l)
    # 检查右下部分棋盘
    head, tail = -1, -1
    for j in range(MAP_SIZE):
        for i in range(MAP_SIZE - j):
            if get_board(MAP_SIZE - i - 1, j + i) == player2:
                tail = i
                if tail - head + 1 < WIN_SET:
                    head = tail
                    continue
                else:
                    # 从 board[j][head] 到 board[j][tail] 检查奖励布局
                    l = []
                    for m in range(head + 1, tail - 1):
                        l.append(get_board(MAP_SIZE - m - 1, j + m) * player1)
                    reward += check_reward(l)
        if MAP_SIZE - j - tail + 1 < WIN_SET:
            continue
        else:
            l = []
            for m in range(tail + 1, MAP_SIZE - 1):
                l.append(get_board(MAP_SIZE - m - 1, j + m) * player1)
            reward += check_reward(l)

    return reward

def computer_step(x, y, camp):
    # param:
    # - x, y: 落子位置;
    # - camp: 阵营
    #   - 1 WHITE
    # return next_state, reward, done
    chess(x, y, 0)
    return get_state(), reward(camp), game_is_over

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
        if get_chessable(x, y) == NOCHESSABLE:
            continue
        res = chess(x, y, 0)
        i += 1
    if res == CANT_CHESS:
        return ERROR
    else:
        return SUCCESS

# 添加按钮  -- 开始游戏
def start_game_btn():
    restart()

# 显示游戏窗口
def show_windows():
    if no_gui:
        return
    top.mainloop()

def add_btn(_text, _command):
    button = tk.Button(top, text=_text, command=_command)
    button.pack()

if __name__ == '__main__':
    canvas_init()
    show_windows()