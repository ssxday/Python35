# -*- coding:utf-8 -*-
"""
这是一个模拟玩骰子猜大小的游戏
各类的定义如下：
class Notebook
    记录游戏结果并进行统计
class Dices
    随机生成一套骰子
class Player
    实现玩游戏的方法
class Dealer
    对游戏结果进行判断
"""
import random

print("面向对象模式重写玩骰子游戏")


class Notebook:
    """设计成单例模式
    单行格式：
    序号|Player押什么押多少|Dices骰子读数|大小|chipsInHand|Player输赢|Player连赢|Player警戒线
    """
    _only = None

    def __new__(cls, *args, **kwargs):
        if cls._only is None:
            cls._only = object.__new__(cls, *args)
        return cls._only

    def __init__(self, flag=True):
        # 单轮游戏展示信息
        self.flag = flag  # 输出开关
        self.dice_reading = ''  # 骰子读数及大小
        self.player_data = ''  # cih及输赢
        self.player_did = ''  # Player押什么以及押多少
        # 统计信息
        self.dice_counter = [0, 0, 0]  # 骰子计数器：统计豹，大，小的次数
        self.wl_counter = [0, 0]  # [输,赢]计数器
        self.loop_counter = 0  # 序号记录 -> 调用player_write()方法的次数
        self.chipsLeft = 0
        self.maxChip = 500  # 记录最高筹码值
        pass

    # 由Dices调用
    def from_dice(self, data):
        a, b, c, d = data
        self.dice_reading = '|%d %d %d|%s|' % (a, b, c, ['T', 'S', 'B'][d])
        self.dice_counter[data[3]] += 1  # 骰子计数器+1
        pass

    # 由Player调用
    def player_write(self, data):
        self.loop_counter += 1  # 次数计数器先跳字
        # 拆包data
        wl, cih, beton, howmuch = data
        if wl:
            self.wl_counter[1] += 1
        else:
            self.wl_counter[0] += 1
        self.chipsLeft = cih  # 手上剩余筹码
        # 格式化
        self.player_did = '押%s%d单位' % (['', '小', '大'][beton], howmuch)
        self.player_data = '%d %s' % (cih, {True: 'WIN', False: 'LOSE'}[wl])
        # 判断是否突破最高筹码
        if cih > self.maxChip:
            self.maxChip = cih
        self.echo()  # 调用单行输出
        pass

    # 输出一条信息
    def echo(self):
        # 格式：
        # 序号|Player押什么押多少|Dices骰子读数|大小|chipsInHand|Player输赢|Player连赢|Player警戒线
        reg = r'{:0>3d} {} {} {}'
        if self.flag:  # 输出开关打开
            line = reg.format(self.loop_counter, self.player_did, self.dice_reading, self.player_data)
            print(line)

    # 整理n次统计信息
    def statistic(self):
        # 统计1、统计骰子结果及概率
        dice_p = [i / sum(self.dice_counter) for i in self.dice_counter]
        for o, t, p in zip(['豹子', '小', '大'], self.dice_counter, dice_p):
            print('%s:%d(%.2f%%)' % (o, t, p * 100))
        # 统计2、统计输赢结果及概率
        wl_p = [i / sum(self.wl_counter) for i in self.wl_counter]
        for o, p, t in zip(['输', '赢'], self.wl_counter, wl_p):
            print('%s的次数：%d(%f%%)' % (o, p, t * 100))
        # 其他信息
        print('剩余筹码：%d' % self.chipsLeft)
        print('最高纪录：%d' % self.maxChip)

    # 整个过程结束时调用，输出统计信息
    def __del__(self):
        if self.flag:
            print()  # 空一行
            self.statistic()  # 调用输出统计信息


class Dices:
    """设计为单例模式
    用法：
    1、outcome -> 得到一组骰子，直到调用shake()否则outcome不会变化
    2、shake() -> 返回一组新骰子组合
    """
    _only = None

    def __new__(cls, *args, **kwargs):
        if cls._only is None:
            cls._only = object.__new__(cls, *args)  # 这里有一点小变化，注意会否出错
        return cls._only

    def __init__(self):
        self.notebook = Notebook()  # 实例化笔记本单例
        self.outcome = 'unknown'  # 在shake()里调用notebook的方法记录

    def shake(self):
        """
        由Dealer调用，换一组新的骰子
        :return:豹子，小，大
        """
        dice_set = [1, 2, 3, 4, 5, 6]
        dice1 = random.choice(dice_set)
        dice2 = random.choice(dice_set)
        dice3 = random.choice(dice_set)

        setsum = dice1 + dice2 + dice3
        outcome = None  # 先初始化一下
        data = [dice1, dice2, dice3]

        if dice1 == dice2 and dice2 == dice3:
            outcome = 0
        elif 4 <= setsum <= 10:
            outcome = 1
        elif 11 <= setsum <= 17:
            outcome = 2
        data.append(outcome)  # 添加outcome信息
        self.outcome = outcome  # 刷新self.outcome
        self.notebook.from_dice(data)  # 调用笔记本，记录数据
        return outcome


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
            cls._only = object.__new__(cls, *args)
        return cls._only

    def __init__(self, cih=500):
        self.notebook = Notebook()  # 拿出笔记本
        self.chipsInHand = cih  # 手中筹码
        self.secure = cih  # 警戒值
        self.maxChip = cih
        self.lastresult = False  # 上一轮的输赢记录
        # self.winning = 0  # 连赢轮数（单轮设计用不到）
        self.beton = 2  # 不再初始化时调用guess
        self.howmuch = 1  # 不再初始化时调用think

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
        data = [wl]  # 产生的信息记录
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
        # 生成说明data->[输赢,当前轮cih]
        data += [self.chipsInHand, self.beton, self.howmuch]
        self.notebook.player_write(data)


class Dealer:  # 有可能本类才是各类的核心
    """一轮游戏争取只在这里解决，多轮再去Casino
    # Table实例化Dices和Player两个对象
    # Table方法如下：
    """

    def __init__(self):
        self.dice = Dices()  # 实例化骰盅，单例模式
        self.player = Player()  # 实例化玩家，单例模式

    def deal(self):
        self.dice.shake()  # 摇骰子,Dices变换outcome
        self.player.guess()  # Player变换beton
        self.player.think()  # Player变换howmuch
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
    """
    def __init__(self, n=300):
        self.loopcount = 0  # 循环次数记录
        self.dler = Dealer()
        while self.loopcount < n:
            self.loopcount += 1
            self.dler.deal()


# play = Dealer()
# play.deal()  # 玩一轮

playN = Casino(1)  # 循环玩,默认300次
