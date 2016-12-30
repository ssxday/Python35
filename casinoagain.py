# -*- coding:utf-8 -*-
import random

print("重新规划")

# 思路整理：
# 1、把输出信息分段，单独控制；
# 2、本例是玩一轮的情况
#


class Dices:
    """
    用法：
    1、Dices.secret -> 得到一组骰子，直到调用shake()否则outcome不会变化
    2、shake() -> 返回一组新骰子组合
    3、counter() -> tuple(Triple, Small, Big)
    """
    counter = (0, 0, 0)

    def __init__(self):
        self.data = ''
        self.outcome = self.shake()  # 同时data也记录

    def shake(self):
        """
        换一组新的骰子
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
        return outcome


class Player:
    """
    # Player的属性如下：
    chipsInHand
    secure
    beton
    howmuch
    # Player的方法如下：
    think()
    guess()
    """

    def __init__(self, cih=500):
        self.chipsInHand = cih  # 手中筹码
        self.secure = cih  # 警戒值
        self.beton = self.guess()
        self.howmuch = self.think()

    def guess(self, beton=2):
        # 尝试：guess负责beton
        return beton

    def think(self,howmuch=1):
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
        return howmuch


class Dealer:  # 有可能本类才是各类的核心
    """
    # Dealer属性如下：
    cover -> int 骰子有结果了，但是放在罩子里不让人知道
    lastresult -> bool 上一轮的输赢
    # Dealer方法如下：
    """

    def __init__(self):
        self.dice = Dices()  # 实例化骰盅
        self.player = Player()  # 实例化玩家
        self.outcome = 'unknown'
        self.cover = self.dice.outcome  # 一组骰子摇好了,但是还没人知道
        self.lastresult = False

    def uncover(self):
        self.outcome = self.cover  # 结果揭晓

    def deal(self):
        if self.outcome == self.player.beton:
            # Win
            self.player.chipsInHand += self.player.howmuch
            pass
        else:
            # lose
            self.player.chipsInHand -= self.player.howmuch
            pass


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

