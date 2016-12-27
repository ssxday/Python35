# -*- coding:utf-8 -*-
import random


class Games:
    """
    每一种游戏必须带着以下数据return
    1、result_set:
    2、conclusion
    3、rate:value
    格式为((result), conclusion, rate)
    """
    def diceshake(self):
        # 摇出abc三次,point为点数
        a = random.randint(1, 6)
        b = random.randint(1, 6)
        c = random.randint(1, 6)
        point = None
        if a == b == c:
            point = 0
        elif 4 <= a + b + c <= 10:
            point = 1
        elif 11 <= a + b + c <= 17:
            point = 2
        else:
            pass
        return (a, b, c), point, 2

    def blackjack(self):
        pass

    def russianroller(self):
        pass


class Casino(Games):
    def __init__(self, guess=2, cash=1000):
        # 初始化...
        self.relations = ('同', '小', '大')
        self.chips_in_hand = 0  # 剩余chips
        self.chips_on_table = 0  #
        self.loops = 0  # 轮数
        self.guess = guess
        self.notes = ''  # 结果展示数据

        # about round
        self.result_sets = tuple()
        self.conclusion = int()
        self.rate = 2

        # start...
        self.cashin(cash)
        # 以下为单独一轮
        self.bet(self.guess)  # make a guess with some chips
        self.play()  # 调用Games里的游戏方法
        w_or_l = self.deal()  # return bool结果，并执行chips的划拨
        self.notespad(w_or_l)  # 输出展示
        # 一轮结束
        self.cashout()
        pass

    def cashin(self, cash):
        self.chips_in_hand += cash
        pass

    def bet(self,guess=2, howmuch=1):
        # 资金变动
        self.chips_on_table = howmuch
        self.chips_in_hand -= howmuch
        # 猜的目标
        self.guess = guess
        pass

    def play(self):
        # return数据的索引为：
        # [0] 结果集
        # [1] 结论
        # [2] rate
        # 调用Games里的方法
        self.result_sets, self.conclusion, self.rate = self.diceshake()
        return

    def deal(self):
        # 判断结果，结算本轮chips
        if self.guess == self.conclusion:
            # won
            self.chips_in_hand += self.chips_on_table * self.rate
            return True
        else:
            # lose
            # self.chips_in_hand不变
            return False
        pass

    def notespad(self, wol):
        # 把结果集tuple result_sets -> string result_str
        result_str = ' '.join([str(s) for s in self.result_sets])
        if wol:
            self.notes += "%s %s won!\n" % (result_str, self.relations[self.guess])
        else:
            self.notes += "%s %s lose\n" % (result_str, self.relations[self.guess])
        print(self.notes)
        # 整理并输出结果
        pass

    def engine(self, maxn=500):
        for n in range(maxn):
            pass
        pass

    def cashout(self):
        # 计算净增量
        pass

    def __del__(self):
        # 概率统计
        # 结束
        print('回家')
        pass


print(' Testing as follows '.center(70, '='))
# gm = Games()
csn = Casino(2)

# print(csn.play())
# print(csn.notes)

