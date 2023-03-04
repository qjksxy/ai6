import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
import numpy as np
import random
import os
import Map

#定义DQN
class DQN():
    def __init__(self):
        self.n_input = Map.mapsize * Map.mapsize
        self.n_output = 1
        self.current_q_step = 0
        self.avg_loss = 0
        self.train_times = 0
        self.x = tf.placeholder("float", [None, Map.mapsize, Map.mapsize], name = 'x')
        self.y = tf.placeholder("float", [None, self.n_output], name = 'y')
        self.create_Q_network()
        self.create_training_method()
        self.saver = tf.train.Saver()
        self.sess = tf.Session()
        #self.sess = tf.InteractiveSession()
        self.sess.run(tf.initialize_all_variables())
        
    def create_Q_network(self):
        wc1 = tf.Variable(tf.random_normal([3, 3, 1, 64], stddev = 0.1), dtype=tf.float32, name = 'wc1')
        wc2 = tf.Variable(tf.random_normal([3, 3, 64, 128], stddev = 0.1), dtype=tf.float32, name = 'wc2')
        wc3 = tf.Variable(tf.random_normal([3, 3, 128, 256], stddev = 0.1), dtype=tf.float32, name = 'wc3')
        wd1 = tf.Variable(tf.random_normal([256, 128], stddev = 0.1), dtype=tf.float32, name = 'wd1')
        wd2 = tf.Variable(tf.random_normal([128, self.n_output], stddev = 0.1), dtype=tf.float32, name = 'wd2')
        
        bc1 = tf.Variable(tf.random_normal([64], stddev = 0.1), dtype=tf.float32, name = 'bc1')
        bc2 = tf.Variable(tf.random_normal([128], stddev = 0.1), dtype=tf.float32, name = 'bc2')
        bc3 = tf.Variable(tf.random_normal([256], stddev = 0.1), dtype=tf.float32, name = 'bc3')
        bd1 = tf.Variable(tf.random_normal([128], stddev = 0.1), dtype=tf.float32, name = 'bd1')
        bd2 = tf.Variable(tf.random_normal([self.n_output], stddev = 0.1), dtype=tf.float32, name = 'bd2')
        
        weights = {
            'wc1' : wc1,
            'wc2' : wc2,
            'wc3' : wc3,
            'wd1' : wd1,
            'wd2' : wd2
        }
        
        biases = {
            'bc1' : bc1,
            'bc2' : bc2,
            'bc3' : bc3,
            'bd1' : bd1,
            'bd2' : bd2
        }
        
        self.Q_value = self.conv_basic(self.x, weights, biases)
        self.Q_Weihgts = [weights, biases]

    def conv_basic(self, _input, _w, _b):
        #input
        _out = tf.reshape(_input, shape = [-1, Map.mapsize, Map.mapsize, 1])
        #conv layer 1
        _out = tf.nn.conv2d(_out, _w['wc1'], strides=[1, 1, 1, 1], padding='SAME')
        _out = tf.nn.relu(tf.nn.bias_add(_out, _b['bc1']))
        _out = tf.nn.max_pool(_out, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
        #conv layer2
        _out = tf.nn.conv2d(_out, _w['wc2'], strides=[1, 1, 1, 1], padding='SAME')
        _out = tf.nn.relu(tf.nn.bias_add(_out, _b['bc2']))
        _out = tf.nn.max_pool(_out, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
        #conv layer3
        _out = tf.nn.conv2d(_out, _w['wc3'], strides=[1, 1, 1, 1], padding='SAME')
        _out = tf.nn.relu(tf.nn.bias_add(_out, _b['bc3']))
        _out = tf.reduce_mean(_out, [1, 2])
        #fully connected layer1
        _out = tf.nn.relu(tf.add(tf.matmul(_out, _w['wd1']), _b['bd1']))
        #fully connected layer2
        _out = tf.add(tf.matmul(_out, _w['wd2']), _b['bd2'])
        return _out
    
    def create_training_method(self):
        #self.cost = tf.reduce_mean(self.LosFunction(logits=self.Q_value, labels=self.y))
        self.cost = tf.reduce_mean(tf.squared_difference(self.Q_value,self.y))
        self.optm = tf.train.AdamOptimizer(learning_rate = 0.001, name='Adam').minimize(self.cost)   

    '''
    def LosFunction(self, logits, labels):
        los = tf.square(logits - labels)
        return los
    '''
    def restore(self):
        if os.path.exists('Saver/cnnsaver.ckpt-0.index'):
            self.saver.restore(self.sess, os.path.abspath('Saver/cnnsaver.ckpt-0'))

    #黑棋代表电脑 如果该白旗走的话 用黑白反转棋盘
    def computerPlay(self, IsTurnWhite):
        board = []
        if IsTurnWhite:
            board = np.array(Map.blackBoard)
        else:
            board = np.array(Map.whiteBoard)
        boards = []
        positions = []
        for i in range(Map.mapsize):
            for j in range(Map.mapsize):
                if board[j][i] == Map.blankcode:
                    predx = np.copy(board)
                    predx[j][i] = Map.blackcode
                    boards.append(predx)
                    positions.append([i, j])
        if len(positions) == 0:
            return 0,0,0
        nextStep = None
        #if Map.AutoPlay == 0:
        nextStep = self.sess.run(self.Q_value, feed_dict = {self.x : boards})
        #else:
            #nextStep = self.sess.run(self.TargetQ_value, feed_dict = {self.x : boards})
        #print(nextStep)
        maxx = 0
        maxy = 0
        maxValue = -1000   #实际最大价值  用于后续学习
#        maxi = 0
        for i in range(len(positions)):
            value = nextStep[i] + random.randint(0,10) / 1000 #如果没有最优步子 则随机选择一步
            if value > maxValue:
                maxValue = value
                maxx = positions[i][0]
                maxy = positions[i][1]
#        print(boards)
#        print(nextStep)
        rdm = random.randint(0, 100)
        if Map.AutoPlay > 0 and rdm > 95:
            step = random.randint(0, len(positions) - 1)
            maxx = positions[step][0]
            maxy = positions[step][1]
        return maxx, maxy, maxValue
       
    
        
    def TrainOnce(self, winner):
        board1 = np.array(Map.mapRecords1)
        board2 = np.array(Map.mapRecords2)
        step1 = np.array(Map.stepRecords1)
        step2 = np.array(Map.stepRecords2)
        scoreR1 = np.array(Map.scoreRecords1)
        scoreR2 = np.array(Map.scoreRecords2)
        board1 = np.reshape(board1, [-1, Map.mapsize, Map.mapsize])
        board2 = np.reshape(board2, [-1, Map.mapsize, Map.mapsize])
        step1 = np.reshape(step1, [-1, Map.mapsize, Map.mapsize])
        step2 = np.reshape(step2, [-1, Map.mapsize, Map.mapsize])
        
        score1 = []
        score2 = []
        
        board1 = (board1 * (1 - step1)) + step1 * Map.blackcode
        board2 = (board2 * (1 - step2)) + step2 * Map.blackcode
        #每步的价值 = 奖励（胜1负-1其他0） + （-0.95） * 对方棋盘能达到的最大价值（max taget Q） 
        for i in range(len(board1)):
            if i == len(scoreR2):#白方多一步  白方赢
                score1.append([1.0]) #获得1分奖励
                if winner == 2:
                    print('error step count!')
            else:
#                print(scoreR2[i])
                score1.append([scoreR2[i][0] * -0.9])
                #score1.append([0])
        if winner == 2:
            #惩罚败方的最后一步
            score1[len(score1) - 1][0] = -0.9
        for i in range(len(board2)):
            if i == len(scoreR1) - 1:#黑白方步数一样 黑方赢
                score2.append([1.0])
                if winner == 1:
                    print('error step count!')
            else:
                score2.append([scoreR1[i + 1][0] * -0.9])
                #score2.append([0])
        if winner == 1:
            score2[len(score2) - 1][0] = -0.9
        borders = np.concatenate([board1, board2],axis=0)
        scores = np.concatenate([score1, score2],axis=0)
        _, totalLoss = self.sess.run([self.optm, self.cost], feed_dict = {self.x : borders, 
                           self.y:scores })
            
        self.avg_loss += totalLoss
        self.train_times += 1
        if Map.AutoPlay % 100 == 0:
            print('train avg loss ' + str(self.avg_loss / self.train_times) + ' has times ' + str(Map.AutoPlay))
            self.avg_loss = 0
            self.train_times = 0
            if Map.AutoPlay == 0:
                self.saver.save(self.sess, os.path.abspath('Saver/cnnsaver.ckpt'), global_step = 0)
            else:
                self.saver.save(self.sess, os.path.abspath('Saver/cnnsaver.ckpt'), global_step = (Map.AutoPlay - 1) // 100)
    
    def PlayWithHuman(self):
        self.restore()
        Map.PlayWithComputer = self.computerPlay
        Map.TrainNet = self.TrainOnce
        Map.ShowWind()
        
if __name__ == '__main__':
    dqn = DQN()
    dqn.PlayWithHuman()