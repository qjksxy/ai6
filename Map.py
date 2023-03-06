import tkinter as tk
import os
import time
import copy

#定义窗口
top = tk.Tk()
top.title("六子棋X")
top.geometry('1200x1200')
mapsize = 15        # 定义地图尺寸
pixsize = 20        # 元素尺寸
winSet = 6          # 连子个数
blankcode = 0       # 空白编号
whitecode = 1       # 白棋
blackcode = -1      # 黑棋
turn_counter = 0    # 保存当前为第几手
is_game_over = False
is_turn_white = True
win_data_set_path = 'DataSets\\win'
los_data_set_path = 'DataSets\\los'
train_net = None

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

# 定义画布
canvas = tk.Canvas(top, height=mapsize * pixsize, width=mapsize * pixsize,
                 bg = "gray")
canvas.pack(pady=10)
for i in range(mapsize):
    canvas.create_line(i * pixsize, 0,
                  i * pixsize, mapsize * pixsize,
                  fill='black')
    canvas.create_line(0, i * pixsize,
                  mapsize * pixsize, i * pixsize,
                  fill='black')

# 初始棋盘
# 创建二维数组 whiteBoard 和 stepBoard, 用 0 填充
whiteBoard = []
stepBoard = []
for i in range(mapsize):
    row = []
    rowBak = []
    for j in range(mapsize):
        row.append(0)
        rowBak.append(blankcode)
    whiteBoard.append(rowBak)
    stepBoard.append(row)
blackBoard = copy.deepcopy(whiteBoard)

def restart():
    global is_game_over
    global is_turn_white
    global turn_counter
    for child in child_map:
        canvas.delete(child)
    child_map.clear()
    turn_counter = 0
    is_game_over = False
    is_turn_white = True
    map_records1.clear()
    map_records2.clear()
    step_records1.clear()
    step_records2.clear()
    score_records1.clear()
    score_records2.clear()
    for i in range(mapsize):
        for j in range(mapsize):
            whiteBoard[j][i] = blankcode
            blackBoard[j][i] = blankcode

def save_data_set(tag):
    if train_net != None:
        train_net(tag)
    else:
        winfilename = win_data_set_path + '\\' + time.strftime("%Y%m%d%H%M%S", time.localtime()) + '.txt'
        losfilename = los_data_set_path + '\\' + time.strftime("%Y%m%d%H%M%S", time.localtime()) + '.txt'
        if not os.path.exists('DataSets'):
            os.mkdir('DataSets')
        if not os.path.exists(win_data_set_path):
            os.mkdir(win_data_set_path)
        if not os.path.exists(los_data_set_path):
            os.mkdir(los_data_set_path)
        strInfo1 = ''
        for i in range(len(map_records1)):
            for j in range(mapsize):
                for k in range(mapsize):
                    strInfo1 += str(map_records1[i][j][k]) + ','
            strInfo1 += '\n'
            for j in range(mapsize):
                for k in range(mapsize):
                    strInfo1 += str(step_records1[i][j][k]) + ','
            strInfo1 += '\n'
        strInfo2 = ''
        for i in range(len(map_records2)):
            for j in range(mapsize):
                for k in range(mapsize):
                    strInfo2 += str(map_records2[i][j][k]) + ','
            strInfo2 += '\n'
            for j in range(mapsize):
                for k in range(mapsize):
                    strInfo2 += str(step_records2[i][j][k]) + ','
            strInfo2 += '\n'
        if tag == 1:
            with open(winfilename,"w") as f:
                f.write(strInfo1)
            with open(losfilename,"w") as f:
                f.write(strInfo2)
        else:
            with open(winfilename,"w") as f:
                f.write(strInfo2)
            with open(losfilename,"w") as f:
                f.write(strInfo1)

def win(tag):
    global is_game_over
    if auto_play == 0:
        print(str(tag) + 'win')
        print('game over!')
    is_game_over = True
    save_data_set(tag)
    return tag

def JudgementPro():
    global is_game_over
    judgemap = whiteBoard
    for i in range(mapsize):
        # 判断行
        chessLen = 0
        currCol = 0
        for j in range(mapsize):
            if judgemap[i][j] == currCol:
                chessLen = chessLen+1
                if chessLen >= winSet and currCol != 0:
                    return win(currCol)
            else:
                chessLen = 1
                currCol = judgemap[i][j]
        # 判断列
        chessLen = 0
        currCol = 0
        for j in range(mapsize):
            if judgemap[j][i] == currCol:
                chessLen = chessLen+1
                if chessLen >= winSet and currCol != 0:
                    return win(currCol)
            else:
                chessLen = 1
                currCol = judgemap[j][i]
    # 判断斜线
    chessLen = 0
    currCol = 0
    for i in range(2*mapsize - 1):
        ix=1
        iy=1
        len=1

# 返回获胜方
# 否则返回0
def judgement_result():
    global is_game_over
    judgemap = whiteBoard
    for i in range(mapsize):
        for j in range(mapsize):
            if judgemap[j][i] != blankcode:
                tag = judgemap[j][i]
                checkrow = True
                checkCol = True
                checkLine = True
                checkLine2 = True
                for k in range(winSet - 1):
                    if i + k + 1 < mapsize: #行
                        if (judgemap[j][i + k + 1] != tag) and checkrow:
                            checkrow = False
                        if j + k + 1 < mapsize: #斜线
                            if (judgemap[j + k + 1][i + k + 1] != tag) and checkLine:
                               checkLine = False
                        else:
                            checkLine = False
                    else:
                        checkrow = False
                        checkLine = False
                    if j + k + 1 < mapsize: #列
                       if (judgemap[j + k + 1][i] != tag) and checkCol:
                           checkCol = False
                       if i - k - 1 >= 0: #斜线
                            if (judgemap[j + k + 1][i - k - 1] != tag) and checkLine2:
                               checkLine2 = False
                       else:
                            checkLine2 = False
                    else:
                        checkCol = False
                        checkLine2 = False
                    if not checkrow and not checkCol and not checkLine and not checkLine2:
                        break
                if checkrow or checkCol or checkLine or checkLine2:
                    if auto_play == 0:
                        print (str(tag) + 'win')
                        print ('game over!')
                    is_game_over = True
                    save_data_set(tag)
                    return tag
    return 0
            
play_with_computer = None
auto_play = 0
get_max_score = None

# 电脑落子
def computer_play():
    x, y, score = play_with_computer(is_turn_white)
    return chess(x, y, score)

# 游戏开始
def start_x(event):
    global auto_play
    if is_game_over:
        print('Game over, restart!')
        restart()
        return
    # 如果是电脑自弈：
    if auto_play > 0:
        print("电脑自弈开始")
        while auto_play > 0:
            res = computer_play()
            if res != 0:
                auto_play -= 1
                restart()
                computer_play()

        print("电脑自弈完成")
        return

    # 玩家落子时，判断接下来由谁落子：如果是电脑，则电脑进行落子，否则函数结束
    # 记录当前玩家操控的棋子
    playrole = is_turn_white
    x = event.x // pixsize
    y = event.y // pixsize
    if x >= mapsize or y >= mapsize:
        return
    if whiteBoard[y][x] != blankcode:
        return
    score = 0
    if play_with_computer != None:
        _x, _y, score = play_with_computer(is_turn_white)
    res = chess(x, y, score)
    if res != 0:
        return
    if playrole != is_turn_white:
        for i in [0, 1]:
            computer_play()

# playChess 函数
# 落子顺序  人--AI
def play_chess(event):
    global auto_play
    if is_game_over:
        print('Game over, restart!')
        restart()
        return 
    x = event.x // pixsize
    y = event.y // pixsize
    if x >= mapsize or y >= mapsize:
        return
    if whiteBoard[y][x] != blankcode:
        return
    score = 0
    if play_with_computer != None:
        _x, _y, score = play_with_computer(is_turn_white)
    res = chess(x, y, score)
    # 如果没分出胜负：
    if res == 0:
        if play_with_computer != None:
            x, y, score = play_with_computer(is_turn_white)
            res = chess(x,y,score)
            # AutoPlay == 0, 玩家电脑对战
            while auto_play > 0:
                while res == 0:
                    x, y, score = play_with_computer(is_turn_white)
                    res = chess(x,y,score)
                auto_play -= 1
                chess(x,y,score)
                x, y, score = play_with_computer(is_turn_white)
                res = chess(x,y,score)
    
def chess(x,y,score):
    global is_turn_white
    global turn_counter
    if is_game_over:
        if auto_play == 0:
            print('game is over, restart!')
        restart()
        return -1
    if whiteBoard[y][x] != blankcode:
        if auto_play == 0:
            print('game is over, restart!')
        restart()
        return -1    
    step = copy.deepcopy(stepBoard)
    step[y][x] = 1
    if is_turn_white: #白棋是人工走的 如果过用来当训练集 用反转棋盘
        map_records1.append(copy.deepcopy(blackBoard))
        step_records1.append(step)
        score_records1.append(score)
        whiteBoard[y][x] = whitecode #1白 -1黑
        blackBoard[y][x] = blackcode
        child = canvas.create_oval(x * pixsize,
                                   y * pixsize, 
                                   x * pixsize + pixsize,  
                                   y * pixsize + pixsize, fill='white')
    else:
        map_records2.append(copy.deepcopy(whiteBoard))
        step_records2.append(step)
        score_records2.append(score)
        whiteBoard[y][x] = blackcode #1白 -1黑
        blackBoard[y][x] = whitecode
        child = canvas.create_oval(x * pixsize,
                                   y * pixsize, 
                                   x * pixsize + pixsize,  
                                   y * pixsize + pixsize, fill='black')

    child_map.append(child)

    # 连下两子交换颜色
    if turn_counter < 1:
        turn_counter = turn_counter + 1
    else:
        is_turn_white = not is_turn_white
        turn_counter = 0
    return judgement_result()

#添加按钮
def re_auto_play():
    global auto_play
    auto_play += 5000
btnUp = tk.Button(top, text ="自动训练加开始1000次", command = re_auto_play)
btnUp.pack()

#添加按钮
def auto_play_once():
    if play_with_computer != None:
        x, y, score = play_with_computer(is_turn_white)
        chess(x,y,score)
btnAuto = tk.Button(top, text ="自动走1次", command = auto_play_once)
btnAuto.pack()

# 添加按钮  -- 开始游戏
def start_game_btn():
    restart()
startGameBtn = tk.Button(top, text="开始游戏/重新开始", command=start_game_btn)
startGameBtn.pack()

# 画布与鼠标左键进行绑定
#canvas.bind("<B1-Motion>", playChess)
canvas.bind("<Button-1>", start_x)

#显示游戏窗口
def show_windows():
    top.mainloop()