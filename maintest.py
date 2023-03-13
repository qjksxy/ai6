import ui

class Action:
    def __init__(self):
        self.x = 1
        self.y = 1


def _equals1(x):
    if x == 1:
        return 1
    else:
        return 0

def step(action):
    return action.x, action.y

def test():
    pass

def ju(mod, count, sc):
    if count >= 6:
        print('l6')
    if count == 5:
        if mod == 's':
            print('s5')
        if mod == 'd':
            print('d5')
    if count == 4:
        if mod == 's':
            print('s4')
        if mod == 'd':
            print('d4')
    if count == 3:
        if mod == 's':
            print('s3')
        if mod == 'd':
            print('d3')
    if count == 2:
        if mod == 's':
            print('s2')
        if mod == 'd':
            print('d2')
    return sc

def re(chess_list):
    l = len(chess_list)
    sc = 0
    count = 0
    i = 0
    for i in range(l):
        if chess_list[i] == 1:
            count += 1
        if chess_list[i] == 0:
            break
    sc = ju('s', count, sc)
    if chess_list[i] == 1:
        return sc
    count = 0
    for j in range(i, l):
        if chess_list[j] == 1:
            count += 1
        if chess_list[j] == 0:
            sc = ju('d', count, sc)
            count = 0
    count = 0
    for i in range(l):
        x = l - i - 1
        if chess_list[x] == 1:
            count += 1
        if chess_list[x] == 0:
            break
    sc = ju('s', count, sc)
    return sc

if __name__ == '__main__':
    # action = Action()
    # action.x = 10
    # action.y = 20
    # x, y = step(action)
    # print(x, y)
    board = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    # s = [_equals1(x) for x in board]
    # t = [_equals1(-1 * x) for x in board]
    # s.extend(t)
    # print(s)
    re(board)