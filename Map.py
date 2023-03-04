import tkinter as tk
import os
import time
import copy

#定义窗口
top = tk.Tk()
top.title("魔改五子棋")
top.geometry('900x900')
#定义地图尺寸
mapsize = 15
#元素尺寸
pixsize = 20
#连子个数
winSet = 5
#空白编号
blankcode = 0
#白棋
whitecode = 1
#黑棋
blackcode = -1

#定义画布
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

#棋子列表
childMap = []

#记录棋图
mapRecords1 = []
mapRecords2 = []
#记录棋步
stepRecords1 = []
stepRecords2 = []

#记录得分
scoreRecords1 = []
scoreRecords2 = []

isGameOver = False
IsTurnWhite = True

def Restart():
    global isGameOver
    global IsTurnWhite
    for child in childMap:
        canvas.delete(child)
    childMap.clear()
    isGameOver = False
    IsTurnWhite = True
    mapRecords1.clear()
    mapRecords2.clear()
    stepRecords1.clear()
    stepRecords2.clear()
    scoreRecords1.clear()
    scoreRecords2.clear()
    for i in range(mapsize):
        for j in range(mapsize):
            whiteBoard[j][i] = blankcode
            blackBoard[j][i] = blankcode


WinDataSetPath = 'DataSets\\win'
LosDataSetPath = 'DataSets\\los'

TrainNet = None

def SaveDataSet(tag):
    if TrainNet != None:
        TrainNet(tag)
    else:
        winfilename = WinDataSetPath + '\\' + time.strftime("%Y%m%d%H%M%S", time.localtime()) + '.txt'
        losfilename = LosDataSetPath + '\\' + time.strftime("%Y%m%d%H%M%S", time.localtime()) + '.txt'
        if not os.path.exists('DataSets'):
            os.mkdir('DataSets')
        if not os.path.exists(WinDataSetPath):
            os.mkdir(WinDataSetPath)
        if not os.path.exists(LosDataSetPath):
            os.mkdir(LosDataSetPath)
        strInfo1 = ''
        for i in range(len(mapRecords1)):
            for j in range(mapsize):
                for k in range(mapsize):
                    strInfo1 += str(mapRecords1[i][j][k]) + ','
            strInfo1 += '\n'
            for j in range(mapsize):
                for k in range(mapsize):
                    strInfo1 += str(stepRecords1[i][j][k]) + ','
            strInfo1 += '\n'
        strInfo2 = ''
        for i in range(len(mapRecords2)):
            for j in range(mapsize):
                for k in range(mapsize):
                    strInfo2 += str(mapRecords2[i][j][k]) + ','
            strInfo2 += '\n'
            for j in range(mapsize):
                for k in range(mapsize):
                    strInfo2 += str(stepRecords2[i][j][k]) + ','
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
    global isGameOver
    if AutoPlay == 0:
        print(str(tag) + 'win')
        print('game over!')
    isGameOver = True
    SaveDataSet(tag)
    return tag

def JudgementPro():
    global isGameOver
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
def JudgementResult():
    global isGameOver
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
                    if AutoPlay == 0:
                        print (str(tag) + 'win')
                        print ('game over!')
                    isGameOver = True
                    SaveDataSet(tag)
                    return tag
    return 0
            
PlayWithComputer = None
AutoPlay = 0
GetMaxScore = None

def playChess(event):
    global AutoPlay
    if isGameOver:
        print('Game over, restart!')
        Restart()
        return 
    x = event.x // pixsize
    y = event.y // pixsize
    if x >= mapsize or y >= mapsize:
        return
    if whiteBoard[y][x] != blankcode:
        return
    score = 0
    if PlayWithComputer != None:
        _x, _y, score = PlayWithComputer(IsTurnWhite)
    res = chess(x, y, score)
    if res == 0:
        if PlayWithComputer != None:
            x, y, score = PlayWithComputer(IsTurnWhite)
            res = chess(x,y,score)
            while AutoPlay > 0:
                while res == 0:
                    x, y, score = PlayWithComputer(IsTurnWhite)
                    res = chess(x,y,score)
                AutoPlay -= 1
                chess(x,y,score)
                x, y, score = PlayWithComputer(IsTurnWhite)
                res = chess(x,y,score)

TurnCounter = 0
    
def chess(x,y,score):
    global IsTurnWhite
    global TurnCounter

    # 连下两子交换颜色
    if TurnCounter < 1:
        TurnCounter = TurnCounter + 1
    else:
        IsTurnWhite = not IsTurnWhite
        TurnCounter = 0
    if isGameOver:
        if AutoPlay == 0:
            print('game is over, restart!')
        Restart()
        return -1
    if whiteBoard[y][x] != blankcode:
        if AutoPlay == 0:
            print('game is over, restart!')
        Restart()
        return -1    
    step = copy.deepcopy(stepBoard)
    step[y][x] = 1
    if IsTurnWhite: #白棋是人工走的 如果过用来当训练集 用反转棋盘
        mapRecords1.append(copy.deepcopy(blackBoard))
        stepRecords1.append(step)
        scoreRecords1.append(score)
        whiteBoard[y][x] = whitecode #1白 -1黑
        blackBoard[y][x] = blackcode
        child = canvas.create_oval(x * pixsize,
                                   y * pixsize, 
                                   x * pixsize + pixsize,  
                                   y * pixsize + pixsize, fill='white')
    else:
        mapRecords2.append(copy.deepcopy(whiteBoard))
        stepRecords2.append(step)
        scoreRecords2.append(score)
        whiteBoard[y][x] = blackcode #1白 -1黑
        blackBoard[y][x] = whitecode
        child = canvas.create_oval(x * pixsize,
                                   y * pixsize, 
                                   x * pixsize + pixsize,  
                                   y * pixsize + pixsize, fill='black')

    childMap.append(child)
    return JudgementResult()

#添加按钮
def ReAutoPlay():
    global AutoPlay
    AutoPlay += 1000
 
btnUp = tk.Button(top, text ="自动训练加开始1000次", command = ReAutoPlay)
btnUp.pack()

#添加按钮
def AutoPlayOnce():
    if PlayWithComputer != None:
        x, y, score = PlayWithComputer(IsTurnWhite)
        chess(x,y,score)
 
btnAuto = tk.Button(top, text ="自动走1次", command = AutoPlayOnce)
btnAuto.pack()
# 画布与鼠标左键进行绑定
#canvas.bind("<B1-Motion>", playChess)
canvas.bind("<Button-1>", playChess)

#显示游戏窗口
def ShowWind():
    top.mainloop()