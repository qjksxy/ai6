import tkinter as tk
import os
import time
import copy

#定义窗口
top = tk.Tk()
top.title("六子棋X")
top.geometry('1200x1200')
mapsize = 15        # 定义地图尺寸
pixsize = 30        # 元素尺寸
win_set = 6         # 连子个数
blankcode = 0       # 空白编号
whitecode = -1      # 白棋
blackcode = 1       # 黑棋
turn_counter = 0    # 保存当前为第几手
is_game_over = False
is_turn_black = True
white_board = []
black_board = []
stepBoard = []
row = []
row_bak = []
# 棋子列表
child_map = []
# 记录棋图
map_records1 = []
map_records2 = []
# 记录棋步
step_records1 = []
step_records2 = []
# 记录得分
score_records1 = []
score_records2 = []
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

def get_board(x, y):
    return board[y * mapsize + x]

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
    chess(x, y, 0)

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
    # return judge_result()

#添加按钮
def re_auto_play():
    global auto_play
    auto_play += 10
btnUp = tk.Button(top, text ="自动训练加开始10次", command = re_auto_play)
btnUp.pack()

#添加按钮
# def auto_play_once():
#     if play_with_computer != None:
#         x, y, score = play_with_computer(is_turn_white)
#         chess(x,y,score)
# btnAuto = tk.Button(top, text ="自动走1次", command = auto_play_once)
# btnAuto.pack()

# 添加按钮  -- 开始游戏
def start_game_btn():
    restart()
    pass
startGameBtn = tk.Button(top, text="开始游戏/重新开始", command=start_game_btn)
startGameBtn.pack()

canvas.bind("<Button-1>", touch_canvas)

#显示游戏窗口
def show_windows():
    top.mainloop()

if __name__ == '__main__':
    canvas_init()
    show_windows()