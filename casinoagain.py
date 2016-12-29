# -*- coding:utf-8 -*-
import random
print("重新规划")
# 连赢时按照斐波那契数列押注，一旦输了winning归零
# winning从零开始时，一旦输了就用2倍反复押，直到回到上一轮winning结束的那个hook,
# 搏完了之后winning要归位的（在bet()上提现搏完了）
# 加入心理承受的标杆函数
# wining一旦从正数变成0或负数，则记录本场cih为secure
# 思路整理：
# 1、把输出信息分段，单独控制；
# 2、把play拆成playonce和playn；
# 3、bet()的策略封装到playn的循环中，playonce撤掉循环
# 4、在playn中操作内部变量，最终调用bet()把内部变量传到对象属性#


class Dices:
    """
    用法：
    1、Dices.outcome -> 得到一组骰子，直到调用shake()否则outcome不会变化
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
    """"""

    def __init__(self, cih=500):
        self.chipInHand = cih

    def guess(self, beton, howmuch):
        return beton


class Dealer:
    """
    """


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

    def __init__(self, n):
        dice = Dices()  # 实例化骰盅
        self.outcome = dice.outcome  # 一组骰子摇好了
        while Casino.loopcount <= n:
            pass








