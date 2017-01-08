"""
Licensed Materials - Property of SSX
Copyright statement and purpose...
--------------------------------------------
File Name:casino_local.py
Author:
Version:2.0 - interactive
Description:本程序设计为交互式提供建议，并不保证结果
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
"""
import random
print("玩骰子initialized")


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
    序号|Player押什么押多少|Dices骰子读数|大小|chipsInHand|Player输赢|Player连赢|Player警戒线
    """
    def __init__(self, flag=True):
        self.history_length = 7
        self.dice_history = []
        self.cih_history = []
        self.wl_history = [False]
        self.flag = flag
        self.dice_reading = ''
        self.player_data = ''
        self.player_did = ''
        self.secure = 500
        self.dice_counter = [0, 0, 0]
        self.wl_counter = [0, 0]
        self.loop_counter = 0
        self.chipsLeft = 0
        self.maxChip = 500

    def history_record(self, which, happened):
        if which.__len__() >= self.history_length:
            which.pop(0)
        which.append(happened)

    def dice2notebook(self, data):
        a, b, c, d = data
        self.history_record(self.dice_history, d)
        self.dice_reading = '|%d %d %d|%s|' % (a, b, c, ['T', 'S', 'B'][d])
        self.dice_counter[data[3]] += 1

    def player2notebook(self, data):
        self.loop_counter += 1
        wl, cih, beton, howmuch, secure = data
        self.history_record(self.wl_history, wl)
        self.history_record(self.cih_history, cih)
        if wl:
            self.wl_counter[1] += 1
        else:
            self.wl_counter[0] += 1
        self.chipsLeft = cih
        self.secure = secure
        self.player_did = '押{}{:>3}单位'.format(['', '小', '大'][beton], howmuch)
        self.player_data = '{:<4} {:<4}'.format(cih, {True: 'WIN', False: 'LOSE'}[wl])
        if cih > self.maxChip:
            self.maxChip = cih
        self.echo()

    def echo(self):
        reg = r'{:0>4d} {} {} {} 警戒线={}'
        if self.flag:
            line = reg.format(
                self.loop_counter, self.player_did,
                self.dice_reading, self.player_data,
                self.secure)
            print(line)

    def statistic(self):
        dice_p = [i / sum(self.dice_counter) for i in self.dice_counter]
        for o, t, p in zip(['豹子', '小', '大'], self.dice_counter, dice_p):
            print('%s:%d(%.2f%%)' % (o, t, p * 100))
        print('\n玩了 %d 轮' % sum(self.dice_counter))
        wl_p = [i / sum(self.wl_counter) for i in self.wl_counter]
        for o, p, t in zip(['输', '赢'], self.wl_counter, wl_p):
            print('%s的次数：%d(%f%%)' % (o, p, t * 100))
        print('剩余筹码：%d' % self.chipsLeft)
        print('最高纪录：%d' % self.maxChip)

    def __del__(self):
        if self.flag:
            print()
            self.statistic()


@singleton
class Player:
    """设置Player为单例模式，只有唯一的对象
    chipsInHand 手中筹码
    secure 警戒线
    lastresult 上次的输赢
    @beton 押什么
    @howmuch 押多少
    bingo 赢的次数
    screwed 输的次数
    think()
    guess()
    @feedback() 接受游戏结果的反馈，从而改变对象的某些属性
    """
    def __init__(self, cih=500):
        self.notebook = Notebook()
        self.chipsInHand = cih
        self.notebook.cih_history.append(cih)
        self.secure = cih
        self.maxChip = cih
        self.winning = 0
        self.beton = 2
        self.howmuch = 1

    def guess(self):
        """负责押边策略"""
        try:
            last = self.notebook.dice_history[-2]
            self.beton = last if last != 0 else random.choice([1, 2])
        except IndexError:
            self.beton = random.choice([1, 2])
        # self.beton = random.choice([1, 2])

    def evaluate(self):
        """负责出多少的策略"""
        if self.chipsInHand < self.secure:
            self.howmuch *= 2
        else:
            self.howmuch = self.__fibo(self.winning)
        self.chipsInHand -= self.howmuch

    def __fibo(self, n=3):
        if n <= 2:
            return 1
        else:
            return self.__fibo(n-1) + self.__fibo(n-2)

    def dealer2player(self, wl):
        last_wl = self.notebook.wl_history[-1]
        if wl and last_wl:
            self.winning += 1
            self.secure = self.notebook.cih_history[-1]
        elif not (wl or last_wl):
            self.winning -= 1
        elif (wl, last_wl) == (True, False):
            self.winning = 1
        elif (wl, last_wl) == (False, True):
            self.winning = -1
            self.secure = self.notebook.cih_history[-2]
        data = (wl, self.chipsInHand, self.beton, self.howmuch, self.secure)
        self.notebook.player2notebook(data)


class Dealer:
    """一轮游戏争取只在这里解决，多轮再去Casino
    """
    def __init__(self, cih):
        self.player = Player(cih)

    def deal(self):
        self.player.guess()
        self.player.evaluate()
        print('\n建议：不妨押{} {}单位'.format(('T', 'S', 'B')[self.player.beton], self.player.howmuch))
        outcome = input('摇出了什么：0，1，2 ？')
        if outcome == 'end':
            exit('不玩了')
        if int(outcome) == self.player.beton:
            self.player.chipsInHand += 2*self.player.howmuch
            wl = True
        else:
            wl = False
        self.player.dealer2player(wl)


@singleton
class Casino:
    """循环过程在这里完成"""
    def __init__(self, wallet=500):
        self.loopcount = 0
        self.dealer = Dealer(wallet)
        while self.dealer.player.chipsInHand > 0:
            self.loopcount += 1
            self.dealer.deal()

playN = Casino(300)
