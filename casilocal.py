# -*- coding:utf-8 -*-
import random
print("蜗牛打法")
# 连赢时按照斐波那契数列押注，一旦输了winning归零
# winning从零开始时，一旦输了就用2倍反复押，直到回到上一轮winning结束的那个hook,
# 搏完了之后winning要归位的（在bet()上提现搏完了）
# 加入心理承受的标杆函数
# wining一旦从正数变成0或负数，则记录本场cih为secure
# 思路整理：
# 1、把输出信息分段，单独控制；
# 2、把play拆成playonce和playn；
# 3、bet()的策略封装到playn的循环中，playonce撤掉循环
# #


class Casino:
    # 元信息
    BOTTOM = 500  # 底线
    arr_beton = ["豹子", "小", "大"]

    # 统计信息
    num_baozi = 0  # 豹子出了多少次
    num_small = 0  # 小出现的次数
    num_big = 0  # 大出现的次数
    max_wining = 0  # 最高连赢次数
    reverse = 0  # 调转的次数(输的次数)
    bingo = 0  # 赢的总数
    looptimes = 0  # 循环play次数

    # 单次信息
    wining = 0  # 连续赢的次数，负数代表连续输
    lastresult = False  # True为上次赢了，False为上次输了
    outcome = -1  # outcome代表上一次(单次)结果的数字形式：豹子 = 0；小 = 1；大 = 2

    # 通知内容
    note = ""
    notexe = ""
    note_secure = ""

    # 构造方法
    def __init__(self, ttl=300, cih=500, echo=True):
        # 初始化
        self.chipsInHand = cih  # 初始化筹码
        self.maxChip = cih  # 拥有筹码数量的最高记录
        self.secure = cih  # 安全底线
        self.echo = echo  # 是否输出的标志
        self.beton = 2  # 2代表默认大
        self.howmuch = 1

        # 启动play()
        self.playn(ttl)
        # self.playonce()

    def playn(self, n):
        # 开始循环play
        for i in range(n):
            if self.chipsInHand <= self.howmuch:
                break  # 筹码输光，退出
            else:
                self.looptimes += 1  # 循环次数 + 1

            # 第一步，bet
            self.bet()
            # 第二步，摇骰子
            self.diceset()  # 执行摇色子，并记录这次出的大小结果
            # 第三步，判断
            self.deal()
            # 第四步，打印结果出来
            self.notes()

    def playonce(self):
        # 第一步，bet
        self.bet()
        # 第二步，摇骰子
        self.diceset()  # 执行摇色子，并记录这次出的大小结果
        # 第三步，判断
        self.deal()
        # 第四步，打印结果出来
        # self.notes()

    # 第一步bet
    # 自动掉头
    # 现在没有解决的是，
    def bet(self):
        if self.chipsInHand < self.secure:  # 如果跌破secure安全线
            if self.outcome == 0:  # 如果上次是豹子
                self.beton = 2  # 这次就押大
            else:  # 否则上把结果是啥，那么这把就押啥
                self.beton = self.outcome

            # 翻2.2倍，即3倍
            self.howmuch *= 2.5  # 不严谨，应确保从1开始，因此要重新写个函数
            self.psych()  # 总是跟在howmuch后面
            self.notexe = "\t押%s%d单位\t启动secure=%d" % (self.arr_beton[self.beton], self.howmuch, self.secure)
        else:  # 还在secure安全线以上
            if self.wining == 0:  # 如果没有连赢或连输(确定是首次)
                self.beton = 2
                self.howmuch = 1
                self.psych()  # 总是跟在howmuch后面
            else:
                if self.outcome == 0:
                    self.beton = 2  # 上把出现了豹子的情况，出现豹子是一定输的，这把就押大
                # self.howmuch = 1
                else:
                    self.beton = self.outcome
                self.howmuch = self.fibo(self.wining)
                self.psych()  # 总是跟在howmuch后面
            self.notexe = "\t押%s%d单位" % (self.arr_beton[self.beton], self.howmuch)

    # 第二步摇骰子
    def diceset(self):
        dice = [1, 2, 3, 4, 5, 6]
        dice1 = random.choice(dice)
        dice2 = random.choice(dice)
        dice3 = random.choice(dice)

        self.note = "%05d |%d %d %d| " % (self.looptimes, dice1, dice2, dice3)
        setsum = dice1 + dice2 + dice3
        if dice1 == dice2 and dice2 == dice3:
            self.num_baozi += 1
            self.outcome = 0
            self.note += "T |"

        elif 4 <= setsum <= 10:
            self.num_small += 1
            self.outcome = 1
            self.note += "S |"

        elif 11 <= setsum <= 17:
            self.num_big += 1
            self.outcome = 2
            self.note += "B |"

    # 第三步判断
    def deal(self):
        arr = {True: "WIN!", False: "LOSE"}
        if self.beton == self.outcome:
            # Win
            self.chipsInHand = self.chipsInHand + self.howmuch
            # 判断连赢次数
            if self.lastresult:
                self.wining += 1
                self.secured(self.wining)
                self.m_wining()  # 记录最高连赢次数。
            else:
                self.wining = 1
                self.secured(self.wining)

            # 记录最高筹码值while win
            if self.chipsInHand > self.maxChip:
                self.maxChip = self.chipsInHand

            # 记录本次输赢结果
            self.lastresult = True
            # 记录赢的次数
            self.bingo += 1
        else:
            # lose
            self.chipsInHand = self.chipsInHand - self.howmuch  # lose
            if self.lastresult:
                self.wining = -1
                # self.secure = self.chipsInHand # 本次输了，上次赢了，secure加码
                self.secured(self.wining)
            else:
                self.wining -= 1
                self.secured(self.wining)

            self.lastresult = False
            # 记录调转次数，在此规则下，调转次数等于输的次数。
            self.reverse += 1

        # 连赢次数归位
        if self.wining >= 8:
            self.wining = 0
            self.secured(self.wining)

        self.note += '%d\t%s\twining=%s' % \
                     (
                     self.chipsInHand, arr[self.lastresult], ("+%d" % self.wining if self.wining >= 0 else self.wining))
        # self.notexe += "&nbsp;"

    def notes(self):
        if self.echo:
            print(self.note + self.notexe)

    def fibo(self, n):
        if n <= 1:
            return 1
        elif n >= 2:
            return self.fibo(n - 1) + self.fibo(n - 2)

    def psych(self, p=0.05):
        # 心理作用的影响函数
        if self.chipsInHand >= (1 + p) * Casino.BOTTOM and self.chipsInHand - self.howmuch < Casino.BOTTOM:
            # print("心理干预，冷静十分钟！")
            # exit()
            pass

    # 记录最高连赢

    def m_wining(self):
        if self.wining > self.max_wining:
            self.max_wining = self.wining

    temp_wining = 0

    def secured(self, v):
        # from php
        # static temp_wining

        if Casino.temp_wining >= 2 and v <= 0:
            # 执行记录secure的动作
            self.secure = self.chipsInHand
        Casino.temp_wining = v
        return v

    def tongji(self):
        print()
        tongji = "small:%d (%f%%)\n" % (self.num_small, self.num_small * 100 / self.looptimes)
        tongji += "big:%d (%f%%)\n" % (self.num_big, self.num_big * 100 / self.looptimes)
        tongji += "豹子:%d (%f%%)\n" % (self.num_baozi, self.num_baozi * 100 / self.looptimes)
        tongji += "\n玩的次数：%d" % self.looptimes
        tongji += "\n剩余筹码：%d" % self.chipsInHand
        tongji += "\n最高筹码：%d" % self.maxChip
        tongji += "\n最高连赢次数：%d" % self.max_wining
        tongji += "\n调转次数：%d(%f%%)" % (self.reverse, self.reverse * 100 / self.looptimes)
        tongji += "\n赢的次数：%d(%f%%)" % (self.bingo, self.bingo * 100 / self.looptimes)
        print(tongji)

    def __del__(self):
        if self.echo:
            self.tongji()


# Game Start！
# 可带两个参数，第一个为$total,第二个为chipsInHand
casino = Casino(300, 500)
# 统计section
del casino  # 执行析构方法，调用tongji()
