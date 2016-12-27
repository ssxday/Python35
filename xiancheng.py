# -*- coding:utf-8 -*-
def isPrime(n=3):
    if n <= 1:
        return False
    for i in range(2, n // 2 + 1):
        if n % i == 0:
            return False
        else:
            continue
    return True


def forthrd(start=2, step=100, mark=''):
    fltr = filter(isPrime, range(start, start + step))
    i = 0
    for r in fltr:
        print(r, mark)
        i += 1
    return i


print(' 主程序开始了 '.center(50, '='))
print('没有使用线程的情况：')
start = 10000000
step = 130
# forthrd(start, step, 'a')
# print()
# forthrd(start, step, 'b')
import threading
print('创建并使用线程：')
# help(threading.Thread.daemon)
# 创建线程，交替执行子线程
ta = threading.Thread(target=forthrd, args=(start, step, 'A'))
tb = threading.Thread(target=forthrd, args=(start, step, 'B'))
# print('线程a：',ta)  # <Thread(Thread-1, initial)>
# print('线程b：',tb)  # <Thread(Thread-2, initial)>
# Daemon 和 isDaemon()
print('%s会守护主进程吗：%s' % (ta.name, ta.isDaemon()))
print('%s会守护主进程吗：%s' % (tb.name, tb.isDaemon()))
# ta.daemon = True
# tb.daemon = True
print('%s会守护主进程吗：%s' % (ta.name, ta.isDaemon()))
print('%s会守护主进程吗：%s' % (tb.name, tb.isDaemon()))
# 开启执行
print('使用线程后的执行情况：')
# tb.start()
# ta.start()
# isAlive()方法 与 name属性
print('线程%s在运行吗：' % ta.name, ta.is_alive())  # 同isAlive()
print('线程%s在运行吗：' % tb.name, tb.isAlive())
# 在主线程调用子线程的join()方法，主程序会等ta，tb完成后才继续！！！
# 实现效果：大部队原地待命等着ta，tb
if ta.is_alive():
    ta.join()  # 主线程会等ta完成再继续
if tb.is_alive():
    tb.join()  # 主线程会等tb完成再继续

# 线程同步
print('\n线程同步问题(开启flag为True时会锁定GG标记)')
# 锁住变量threading.Lock & threading.RLock
# 用第二种办法：继承Thread类来创建线程
print('通过继承Thread类创建线程：')
# 定义一个全局变量
GG = 'imGlobal'
# 继承threading.Thread类
class Mythread(threading.Thread):
    def __init__(self, mark='', dolock=False):
        super(Mythread, self).__init__()  # 必须首先调用父类构造方法
        self._mark = mark
        self.dolock = dolock

    # 重载run()方法
    def run(self):
        if self.dolock:
            self._dolock()  # 封装了同步锁
        fltr = filter(self._isPrime, range(10000000, 10000000 + 130))
        for r in fltr:
            print(r, self._mark, GG)

    def _isPrime(self, n=3):
        if n <= 1:
            return False
        for i in range(2, n // 2 + 1):
            if n % i == 0:
                return False
            else:
                continue
        return True

    def _dolock(self):
        # 创建锁对象
        rlock = threading.RLock()
        print('创建锁对象：', rlock)
        # 哪个线程调用了rlock的acquire()方法，中间操作的数据就会被它锁住
        rlock.acquire()
        global GG
        GG = '我被%s锁住了' % self.name  # 把全局变量锁住了
        rlock.release()


# 实例化自定义线程类
mya = Mythread('classA')
myb = Mythread('classB', True)
# print('自定义线程mya：',mya)
# print('自定义线程myb：',myb)
# 执行操作：
# myb.start()
# mya.start()  # mya在这里就开始了！！
try:
    mya.join()  # 主程序等着mya
    myb.join()
except RuntimeError:
    pass
# Event对象（类）
print('线程间的通信：Event对象')
# 实例化Event对象
evt = threading.Event()
help(threading.Event.is_set)
print('内部flag标记：',evt.is_set())



# end
print(' 主线程在此结束 '.center(50, '='))
