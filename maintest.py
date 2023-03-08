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

if __name__ == '__main__':
    action = Action()
    action.x = 10
    action.y = 20
    x, y = step(action)
    print(x, y)
    # board = [1, 0, -1, 0, -1]
    # s = [_equals1(x) for x in board]
    # t = [_equals1(-1 * x) for x in board]
    # s.extend(t)
    # print(s)