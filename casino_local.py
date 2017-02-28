# -*- coding:utf-8 -*-
"""
Licensed Materials - Property of SSX
Copyright statement and purpose...
--------------------------------------------
File Name:casino_local.py
Author:
Version:2.0
Description:这是一个模拟玩骰子猜大小的游戏，标准输出流为console
各类除既有实例化过程以外，不可以再进行任何新的实例化过程，必须使用既有对象的元素
- 各类的定义如下：
class Notebook
    记录游戏结果并进行统计
class Dices
    随机生成一套骰子
class Player
    实现玩游戏的方法
class Dealer
    对游戏结果进行判断
class Casino
    循环引擎
-------------------
class PsychError(Exception)
    心理作用
"""
import random

print("面向对象模式重写玩骰子游戏")


# 单例装饰器
def singleton(cls, *args, **kw):
    instances = {}

    def _singleton(*args):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton


@singleton
class Notebook:
    """设计成单例模式
    单行格式：
    序号 Player.beton howmuch |Dices骰子读数|大小|chipsInHand Player输赢 Player警戒线
    """

    def __init__(self, flag=True):
        # 历史记录
        self.history_length = 4  # 历史记录保留个数，所有历史记录共用
        self.dice_history = []  # 骰子结果的历史记录
        self.cih_history = []  # 每轮筹码浮动的历史记录
        self.wl_history = [0, ]  # 输赢结果的历史记录，初始化为0 -> False
        # 单轮游戏展示信息
        self.flag = flag  # 输出开关
        self.dice_reading = ''  # 骰子读数
        self.dice_sum = ''  # 骰子和的大小
        self.player_data = ''  # cih及输赢
        self.player_did = ''  # Player押什么以及押多少
        self.secure = 0  # 警戒线初始化，在输出前会被刷新
        # howmuch成为notebook对象属性是为了，
        # 当Player在改变howmuch后，依然可以在notebook中找回没有变动前的值，
        # 在触发心理作用后，Player可以找回上一轮结束后的howmuch
        # 需要更多次历史记录时，可建立history
        self.howmuch = 1
        # 统计信息
        self.dice_counter = [0, 0, 0]  # 骰子计数器：统计豹，大，小的次数
        self.wl_counter = [0, 0]  # [输,赢]计数器
        self.loop_counter = 0  # 序号记录 -> 调用player2notebook()方法的次数
        self.chipsLeft = 0
        self.maxChip = 500  # 记录最高筹码值

    # 记录历史的通行方法
    def history_record(self, which, happened):
        if which.__len__() >= self.history_length:
            which.pop(0)
        which.append(happened)

    # 由Dices调用
    def dice2notebook(self, data):
        a, b, c, d = data
        self.history_record(self.dice_history, d)  # 对骰子结果进行记录
        self.dice_reading = '|{} {} {}|'.format(a, b, c)
        self.dice_sum = '{}'.format(['T', 'S', 'B'][d])
        self.dice_counter[data[3]] += 1  # 骰子计数器+1

    # 由Player调用
    def player2notebook(self, data):
        self.loop_counter += 1  # 次数计数器先跳字
        # 拆包data
        wl, cih, beton, howmuch, secure = data
        # 分别处理各项数据
        # 处理wl
        self.history_record(self.wl_history, wl)
        self.wl_counter[wl] += 1
        # 处理cih
        self.history_record(self.cih_history, cih)
        self.chipsLeft = cih  # 手上剩余筹码
        # 判断是否突破最高筹码
        if cih > self.maxChip:
            self.maxChip = cih
        # 处理howmuch
        self.howmuch = howmuch  # 为可能触发的psych()记录上轮的howmuch
        # 处理secure
        self.secure = secure
        # 格式化
        self.player_did = '押{}{:>3}单位'.format(['', '小', '大'][beton], howmuch)
        self.player_data = '{:<4} {:<4}'.format(cih, {True: 'WIN', False: 'LOSE'}[wl])
        # 调用单行输出
        self.echo()

    # 输出一条信息
    def echo(self):
        # 格式：
        reg = r'{:0>4d} {player_did} {dice_reading}{dice_sum}| {player_data} 警戒线={secure}'
        if self.flag:  # 输出开关打开
            line = reg.format(
                self.loop_counter,
                player_did=self.player_did,
                dice_reading=self.dice_reading,
                dice_sum=self.dice_sum,
                player_data=self.player_data,
                secure=self.secure)
            print(line)

    # 由Player调用
    def psy2notebook(self):
        self.loop_counter += 1  # 同样由Player调用，也得跳字儿
        """心理干预的记录"""
        if self.flag:
            print(r'{:0>4d} psychological intervention triggered.'.format(self.loop_counter))

    # 整理n次统计信息
    def statistic(self):
        # 统计1、统计骰子结果及概率
        dice_p = [i / sum(self.dice_counter) for i in self.dice_counter]
        for o, t, p in zip(['豹子', '小', '大'], self.dice_counter, dice_p):
            print('%s:%d(%.2f%%)' % (o, t, p * 100))
        # 统计2、统计输赢结果及概率
        text = '\n玩了 {} 轮，实际将耗时{}小时{}分钟'.format(
            sum(self.dice_counter),
            divmod(sum(self.dice_counter), 60)[0],
            divmod(sum(self.dice_counter), 60)[1]
        )
        print(text)
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


@singleton
class Dices:
    """设计为单例模式
    用法：
    1、outcome -> 得到一组骰子，直到调用shake()否则outcome不会变化
    2、shake() -> 返回一组新骰子组合
    """

    def __init__(self):
        self.notebook = Notebook()  # 实例化笔记本单例
        self.dice_set = (1, 2, 3, 4, 5, 6)
        self.outcome = 'unknown'  # 在shake()里调用notebook的方法记录

    def shake(self):
        """由Dealer调用，换一组新的骰子"""
        dice1 = random.choice(self.dice_set)
        dice2 = random.choice(self.dice_set)
        dice3 = random.choice(self.dice_set)
        sum = dice1 + dice2 + dice3
        outcome = None  # 先初始化一下

        if dice1 == dice2 and dice2 == dice3:
            outcome = 0
        elif 4 <= sum <= 10:
            outcome = 1
        elif 11 <= sum <= 17:
            outcome = 2
        data = (dice1, dice2, dice3, outcome)
        self.outcome = outcome  # 刷新self.outcome
        self.notebook.dice2notebook(data)  # 调用笔记本，记录数据


@singleton
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
    evaluate()
    guess()
    calm()
    @feedback() 接受游戏结果的反馈，从而改变对象的某些属性
    """

    def __init__(self, cih=500):
        self.notebook = Notebook()  # 拿出笔记本
        self.chipsInHand = cih  # 手中筹码
        self.notebook.cih_history.append(cih)  # 初始化时先把首次加进notebook
        self.secure = cih  # 警戒值
        self.winning = 0  # 连赢轮数
        self.beton = 2  # 受guess()直接影响
        self.howmuch = 1  # 受evaluate()直接影响

    def guess(self):
        """负责押边策略"""
        try:
            # 跟随最近揭晓的dice结果，如果上次dice不幸出了T，则随机选择
            last = self.notebook.dice_history[-2]  # -1是刚开出来未揭晓的结果
            self.beton = last if last != 0 else random.choice([1, 2])
        except IndexError:
            # 出错的原因是首次游戏并未产生最近揭晓的结果
            self.beton = random.choice([1, 2])

            # if not any(self.notebook.wl_history[-3:]):
            #     self.beton = random.choice([1, 2])

            # self.beton = random.choice([1, 2])  # 完全随机策略

    def evaluate(self):
        """负责出多少的策略"""
        if self.chipsInHand < self.secure:
            self.howmuch *= 2
        else:
            self.howmuch = self.__fibo(self.winning)
        # 形成最终howmuch前需要过一遍心理干预
        # 有可能会改变howmuch最终的值
        self.__psych()
        # 自己需要先减掉
        self.chipsInHand -= self.howmuch

    def __fibo(self, n):
        if n <= 1:  # 因为n会从0开始，而且n有可能为负数，要确保n为负数时没有机会调用本方法
            return 1
        else:
            return self.__fibo(n - 1) + self.__fibo(n - 2)

    def __psych(self):
        """心理干预策略"""
        assert self.chipsInHand >= 2 * self.howmuch

    def calm(self):
        """心理干预启动后的反应策略"""
        self.howmuch = self.notebook.howmuch  # 回到上一轮结束时的状态
        # Then...
        self.notebook.psy2notebook()

    def set_secure(self, wl):
        """策略如下：
        wl_history:
        [0,0,0] -> pass                | [0,0,1] -> secure=chipsInHand
        [0,1,0] -> pass                | [0,1,1] -> secure=chipsInHand
        [1,0,0] -> pass                | [1,0,1] -> secure=chipsInHand
        [1,1,0] -> secure=chipsInHand  | [1,1,1] -> secure=chipsInHand
        """
        # if wl or all(self.notebook.wl_history[-2:]):
        #     self.secure = self.chipsInHand
        if wl and self.notebook.wl_history[-1]:
            self.secure = self.notebook.chipsLeft  # 策略同e60ef26

    def set_winning(self, wl):
        """"""
        last_wl = self.notebook.wl_history[-1]
        if wl and last_wl:
            self.winning += 1
        elif not (wl or last_wl):
            self.winning -= 1
        elif (wl, last_wl) == (1, 0):
            self.winning = 1
        elif (wl, last_wl) == (0, 1):
            self.winning = -1
        # 赢太久不好
        self.winning = 1 if self.winning >= 10 else self.winning

    # 由dealer进行调用，向Player反馈输赢信息
    def dealer2player(self, wl):
        # 一定要在notebook.player2notebook()之前调取所需notebook.history
        # 设置新的安全线
        self.set_secure(wl)
        # 根据本次输赢 -> 判断连赢次数
        self.set_winning(wl)
        # 生成传给notebook的数据data->(输赢,当前轮cih,beton,howmuch,刷新警戒线)
        data = (wl, self.chipsInHand, self.beton, self.howmuch, self.secure)
        self.notebook.player2notebook(data)


class Dealer:  # 本类才是各类的核心
    """一轮游戏争取只在这里解决，多轮再去Casino
    # Table实例化Dices和Player两个对象
    # Table方法如下：
    """

    def __init__(self):
        self.dice = Dices()  # 实例化骰盅，单例模式
        self.player = Player()  # 实例化玩家，单例模式

    def deal(self):
        self.dice.shake()  # 摇骰子,Dices变换outcome
        try:
            self.player.evaluate()  # Player变换howmuch
        except AssertionError:
            self.player.calm()  # 心理干预启动后的应对措施
        else:
            self.player.guess()  # Player变换beton
            if self.dice.outcome == self.player.beton:
                # Win
                self.player.chipsInHand += 2 * self.player.howmuch
                wl = 1
            else:
                # lose
                wl = 0
            # 向player发送反馈
            self.player.dealer2player(wl)  # wl -> win or lose


class PsychIntervention(Exception):
    """心理干预异常"""

    def __init__(self, text='Psychological Intervention Triggered.'):
        self.text = text

    def __str__(self):
        return self.text


class Casino:
    """循环过程在这里完成"""

    def __init__(self, n=300):
        self.loopcount = 0  # 循环次数记录
        self.dealer = Dealer()
        while self.loopcount < n:
            self.loopcount += 1
            self.dealer.deal()
            if self.dealer.player.chipsInHand < self.dealer.player.howmuch:
                break


playN = Casino(500)  # 循环玩,默认300次
