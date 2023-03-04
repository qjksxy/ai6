import numpy as np
import pandas as pd
import time

np.random.seed(10)  # reproducible

N_STATES = 12                 # 一维世界的宽度
ACTIONS = ['left','right']    # 探索者可用的动作
EPSILON = 0.9                 # greedy贪婪度
ALPHA = 0.3                   # 学习率
GAMMA = 0.9                   # 奖励递减值
MAX_EPISODES = 20             # 最大回合数
FRESH_TIME = 0.1              # 每回合移动间隔时间

'''
我们要将所有Q values放在q_table中，更新q_table也是在更新他的行为准则。
q_table的index是所有对应的state(o所在的位置)，columns是对应的action(探险者选择left或者right)
'''
def bulid_q_table(n_states, actions):
    table = pd.DataFrame(
        np.zeros((n_states, len(actions))),  # q_table 全 0 初始
        columns=actions,  # columns 对应的是行为名称
    )
    return table

'''
定义 action
接着定义探险者是如何挑选行为的，这就是我们引入epsilon greedy的概念。
因为在初始阶段，随机的探索环境，往往比固定的行为模式要好，所以这也是累积经验的阶段，
我们希望探险者不那么贪婪（greedy），所以EPSILON就是用来控制贪婪程度的值。
EPSILON可以随着探险时间不断提升（越来越贪婪），不过在这个例子中，我们就固定EPSILON=0.9,
90%的时间是选择最优策略，10%的时间来探索。
'''
def choose_action(state, q_table):
    state_actions = q_table.iloc[state, :]      # 选出这个state的所有 action的value值
    if (np.random.uniform() > EPSILON) or (state_actions.all() == 0):  # 非贪婪 or 或者这个 state 还没有探索过
        action_name = np.random.choice(ACTIONS)
    else:
        action_name = state_actions.idxmax()    # 贪婪模式
    return action_name

'''
环境的反馈
做出行为后，环境也要给我们的行为一个反馈，反馈出下一个state(S_)和上一个state(S)做出action(A)所得到的reward(R)。
这里定义的规则是，只有当o移动到了T（探险者获取了宝藏），探险者才会得到唯一的奖励，
奖励值R=1，其他情况没有奖励。
'''

def get_env_feedback(S,A):
    if A== 'right': #往右探险
        if S == N_STATES - 2: #找到宝藏
            S_ = 'terminal'
            R = 1
        else:
            S_ = S + 1
            R = 0
    else: #往左探险
        R = 0
        if S == 0:
            S_ = S #碰壁
        else:
            S_ = S - 1
    return S_,R


'''
环境更新
'''
def update_env(S, episode, step_counter):
    env_list = ['-']*(N_STATES-1) + ['T']   # '---------T' our environment
    if S == 'terminal':
        interaction = 'Episode %s: total_steps = %s' % (episode+1, step_counter)
        print('\r{}'.format(interaction), end='')
        time.sleep(2)
        print('\r                                ', end='')
    else:
        env_list[S] = 'o'
        interaction = ''.join(env_list)
        print('\r{}'.format(interaction), end='')
        time.sleep(FRESH_TIME)


def rl():
    q_table = bulid_q_table(N_STATES,ACTIONS)     # 初始化q_table
    for episode in range(MAX_EPISODES):           # 回合
        step_counter = 0
        S = 0 #回合初始的位置
        is_terminated = False
        update_env(S,episode,step_counter)        # 环境更新
        while not is_terminated:
            A = choose_action(S,q_table)          # 选择行为
            S_,R = get_env_feedback(S,A)          # 实施行为并得到环境的反馈
            q_predict = q_table.loc[S,A]          # 估算的（状态-行为）值
            if S_ != 'terminal':
                q_target = R + GAMMA*q_table.iloc[S_,:].max() #实际的（状态-行为)值
            else:
                q_target = R #实际的（状态-行为值）
                is_terminated = True

            q_table.loc[S,A] += ALPHA*(q_target - q_predict) #q_table更新
            S = S_ #更新探索者位置

            update_env(S,episode,step_counter+1)
            step_counter += 1
    return q_table

if __name__ == '__main__':
    table = rl()
    print(table)

'''
建立 QTable 和状态转移表
重复训练：
    根据当前状态选择动作 A
    
'''