# -*- coding:utf-8 -*-
import random

print("重新规划")


# 思路整理：
# 1、把输出信息分段，单独控制；
# 2、本例是玩一轮的情况
#


class Dices:
    """设计为单例模式
    用法：
    1、Dices.secret -> 得到一组骰子，直到调用shake()否则outcome不会变化
    2、shake() -> 返回一组新骰子组合
    3、counter() -> tuple(Triple, Small, Big)
    """
    _only = None

    def __new__(cls, *args, **kwargs):
        if cls._only is None:
            cls._only = object.__new__(cls, *args)  # 这里有一点小变化，注意会否出错
        return cls._only

    counter = [0, 0, 0]

    def __init__(self):
        self.data = ''
        self.outcome = self.shake()  # 同时data也记录

    def shake(self):
        """
        由Dealer调用，换一组新的骰子
        :return:豹子，小，大
        """
        dice_set = [1, 2, 3, 4, 5, 6]
        dice1 = random.choice(dice_set)
        dice2 = random.choice(dice_set)
        dice3 = random.choice(dice_set)

        self.data = "|%d %d %d|" % (dice1, dice2, dice3)
        setsum = dice1 + dice2 + dice3
        outcome = None  # 先初始化一下

        if dice1 == dice2 and dice2 == dice3:
            Dices.counter[0] += 1
            outcome = 0
            self.data += "T |"

        elif 4 <= setsum <= 10:
            Dices.counter[1] += 1
            outcome = 1
            self.data += "S |"

        elif 11 <= setsum <= 17:
            Dices.counter[2] += 1
            outcome = 2
            self.data += "B |"
        self.outcome = outcome
        return outcome


class Notebook:
    """设计成单例模式
    00293|2 2 6| S |962 LOSE wining=-3押大2单位 启动secure=966
    格式：
    1、序号|Player押什么押多少|Dices骰子读数|大小|Dealer输赢|Player连赢|Player警戒线
    2、最终统计信息
    思路：
    需要记录信息的对象调用本类，写入自己对应的信息
    每轮结束时，由Player调用本类的最终输出
    """
    _only = None

    def __new__(cls, *args, **kwargs):
        if cls._only is None:
            cls._only = object.__new__(cls, *args, **kwargs)
        return cls._only

    def __init__(self):
        pass

    def jilu(self):
        pass

    def tongji(self):
        pass


class Player:
    """设置Player为单例模式，只有唯一的对象
    # Player的属性如下：
    chipsInHand 手中筹码
    secure 警戒线
    lastresult 上次的输赢
    # winning单轮设计还用不到，先占位
    @beton 押什么
    @howmuch 押多少
    bingo 赢的次数
    screwed 输的次数
    # Player的方法如下：
    think()
    guess()
    @feedback() 接受游戏结果的反馈，从而改变对象的某些属性
    """
    _only = None

    def __new__(cls, *args, **kwargs):
        if cls._only is None:
            cls._only = object.__new__(cls, *args, **kwargs)
        return cls._only

    def __init__(self, cih=500):
        self.chipsInHand = cih  # 手中筹码
        self.secure = cih  # 警戒值
        self.lastresult = False  # 上一轮的输赢记录
        # self.winning = 0  # 连赢轮数（单轮设计用不到）
        self.beton = self.guess()
        self.howmuch = self.think()

    def guess(self, beton=2):
        # 尝试：guess负责beton
        self.beton = beton  # 还要多次guess嘛，return是初始化用的
        return beton

    def think(self, howmuch=1):
        # 尝试：think负责howmuch
        """
        1、考虑安全线
        2、考虑是不是第一次下注
        3、判断上一轮dice是否是豹子0
        4、
        :return:
        """
        if self.chipsInHand < self.secure:
            pass
        else:
            pass
            # 判断上次是不是豹子
        self.howmuch = howmuch  # 还要不断的think嘛
        return howmuch

    # 由dealer进行调用
    def feedback(self, wl):
        if wl:  # win
            if self.lastresult:  # 上次也赢了
                pass
            else:  # 上次输了
                pass
            pass
        else:  # lose
            if self.lastresult:  # 但是上次赢了
                pass
            else:  # 上次也输了
                pass
            pass
        # 记录本次输赢结果供下次使用
        self.lastresult = wl
        # 判断连赢次数是否超过心理预期
        pass
        # 生成说明
        pass


class Dealer:  # 有可能本类才是各类的核心
    """一轮游戏争取只在这里解决，多轮再去Casino
    # Dealer实例化Dices和Player两个对象
    # Dealer方法如下：
    """

    def __init__(self):
        self.dice = Dices()  # 实例化骰盅，单例模式
        self.player = Player()  # 实例化玩家，单例模式

    def deal(self):
        if self.dice.outcome == self.player.beton:
            # Win
            self.player.chipsInHand += self.player.howmuch
            wl = True
        else:
            # lose
            self.player.chipsInHand -= self.player.howmuch
            wl = False

        # 向player发送反馈
        self.player.feedback(wl)  # wl -> win or lose


class Casino:
    """循环过程在这里完成
    一个完整的playn()流程自diceset()起，经过guess()，至deal()，
    最后notes()输出单轮情况说明
    统计信息最后输出
    playn()首先实例化Dices()
        Dices() -> outcome
        Dices() -> data记录
        Dices() -> counter -> 统计阶段
    """
    loopcount = 0

    def __init__(self, n=300):
        while Casino.loopcount <= n:
            pass


