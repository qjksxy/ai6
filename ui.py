import tkinter as tk
import os
import time
import copy
import random

#定义窗口
top = tk.Tk()
top.title("六子棋X")
top.geometry('1200x1200')
mapsize = 15        # 定义地图尺寸
pixsize = 30        # 像素尺寸
win_set = 6         # 连子个数
blankcode = 0       # 空白编号
whitecode = -1      # 白棋
blackcode = 1       # 黑棋
turn_counter = 0    # 保存当前为第几手
is_game_over = False
is_turn_black = True
# 棋子列表
child_map = []
board = []
# 定义画布
canvas = tk.Canvas(top, height=mapsize * pixsize, width=mapsize * pixsize, bg = "gray")

def canvas_init():
    global canvas
    canvas.pack(pady=10)
    for i in range(mapsize):
        canvas.create_line(i * pixsize, 0, i * pixsize, mapsize * pixsize, fill='black')
        canvas.create_line(0, i * pixsize, mapsize * pixsize, i * pixsize, fill='black')
    for i in range(mapsize * mapsize):
        board.append(blankcode)
    restart()
    add_btn('自动训练', re_auto_play)
    add_btn('自动走1次', auto_play_once_btn)
    add_btn('开始游戏/重新开始', start_game_btn)
    canvas.bind("<Button-1>", touch_canvas)

def get_board(x, y):
    return board[y * mapsize + x]

def get_board_safe(x, y):
    if x < 0 or y < 0 or x >= mapsize or y >= mapsize:
        return blankcode
    else:
        return get_board(x, y)

def set_board(x, y, value):
    global board
    board[y * mapsize + x] = value

def restart():
    global is_game_over
    global is_turn_black
    global turn_counter
    for child in child_map:
        canvas.delete(child)
    child_map.clear()
    turn_counter = 0
    is_game_over = False
    is_turn_black = True
    for i in range(mapsize * mapsize):
        board[i] = blankcode
    # 下第一子
    chess(mapsize//2, mapsize//2, 0)
    is_turn_black = False
    turn_counter = 0

def touch_canvas(event):
    global is_turn_black, turn_counter
    # 获取 x y 坐标
    x = event.x // pixsize
    y = event.y // pixsize
    if x >= mapsize or y >= mapsize or get_board(x, y) != blankcode:
        return
    res = chess(x, y, 0)

def chess(x, y, score):
    global is_turn_black
    global turn_counter
    if is_game_over or get_board(x, y) != blankcode:
        return -1
    if is_turn_black:
        fill_color = 'black'
        set_board(x, y, blackcode)
    else:
        fill_color = 'white'
        set_board(x, y, whitecode)
    child = canvas.create_oval(x * pixsize,
                               y * pixsize,
                               x * pixsize + pixsize,
                               y * pixsize + pixsize, fill=fill_color)
    child_map.append(child)
    # 连下两子交换颜色
    if turn_counter < 1:
        turn_counter = turn_counter + 1
    else:
        is_turn_black = not is_turn_black
        turn_counter = 0
    return judge_result(x, y)

def win(flag):
    print("-----Game end-----")
    print(str(flag) + 'wins')
    return flag

def judge_result(x, y):
    len = 0
    curr_col = blankcode
    for i in range(11):
        col = get_board_safe(x - 5 + i, y)
        if col != blankcode and col == curr_col:
            len += 1
            if len >= 6:
                return win(col)
        if col != curr_col:
            len = 1
            curr_col = col
    len = 0
    curr_col = blankcode
    for i in range(11):
        col = get_board_safe(x, y - 5 + i)
        if col != blankcode and col == curr_col:
            len += 1
            if len >= 6:
                return win(col)
        if col != curr_col:
            len = 1
            curr_col = col
    len = 0
    curr_col = blankcode
    for i in range(11):
        col = get_board_safe(x - 5 + i, y - 5 + i)
        if col != blankcode and col == curr_col:
            len += 1
            if len >= 6:
                return win(col)
        if col != curr_col:
            len = 1
            curr_col = col
    len = 0
    curr_col = blankcode
    for i in range(11):
        col = get_board_safe(x + 5 - i, y - 5 + i)
        if col != blankcode and col == curr_col:
            len += 1
            if len >= 6:
                return win(col)
        if col != curr_col:
            len = 1
            curr_col = col
    return 0

#添加按钮
def re_auto_play():
    global auto_play
    auto_play += 10

#添加按钮
def auto_play_once_btn():
    i = 0
    res = -1
    while i < 20 and res == -1:
        x = random.randint(0, mapsize - 1)
        y = random.randint(0, mapsize - 1)
        res = chess(x, y, 0)
        i += 1

# 添加按钮  -- 开始游戏
def start_game_btn():
    restart()
    pass

#显示游戏窗口
def show_windows():
    top.mainloop()

def add_btn(_text, _command):
    button = tk.Button(top, text=_text, command=_command)
    button.pack()

if __name__ == '__main__':
    canvas_init()
    show_windows()