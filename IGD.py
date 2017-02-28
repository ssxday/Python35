# iterator，generator，decorator
# 迭代器 A(n)=3n+1
print('等差数列迭代器'.center(50, '*'))


class MyIterator:
    def __init__(self, maxn):
        self.n = 0
        self.maxn = maxn

    def __iter__(self):
        return self

    def __next__(self):  # 索引从1开始计,反复运行__next__()
        self.n += 1
        if self.n < self.maxn:
            return 3 * (self.n - 1) + 1
        else:
            raise StopIteration


dengcha = MyIterator(5)
print(dengcha)
for i in dengcha:
    print(i)
# 斐波那契数列迭代器
print('斐波那契数列迭代器'.center(50, '*'))


class Fibo:
    def __init__(self, stop):
        self.stop = stop
        self.n = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.n < self.stop:
            self.n += 1
            return self.__fb(self.n)
        else:
            raise StopIteration

    def __fb(self, n):
        if n <= 0:
            pass
        elif n == 1:
            return 0
        elif n == 2:
            return 1
        elif n >= 3:
            return self.__fb(n - 1) + self.__fb(n - 2)


a = [i for i in Fibo(15)]
print(a)
print('长度:', len(a))

print('iter函数'.center(50, '*'))

# iter(callable,sentinel)函数,iter()的功能类似__next__()会反复执行里面的函数
# 碰到sentinel就停止迭代,取不到sentinel
x = 0


def for_iter():
    base = 3
    global x
    x += 5
    return x + base


print(iter(for_iter, 43))
for i in iter(for_iter, 23):  # sentinel必须精确指定，否则一直迭代下去
    print(i)

print('itertools模块 - 无限迭代'.center(50, '*'))
import itertools
# chain: 多个序列连在一起迭代，仿佛是一个序列似的
print('chain(seq1,seq2)')
a = ['a','b']
b = [1,2]
chain = itertools.chain(a,b)
print('chain是个{}对象'.format(chain))
for c in chain:
    print(c)

print()
print("无限迭代count(),用于生成等差数列")
for i in itertools.count(3, 4):  # y = 3 + 4x
    if i < 15:  # 如果不加条件会一直往下走,必须加break
        print(i)
    else:
        break

print('无限迭代cycle(seq)')
# 无限迭代cycle(seq)
x = 0
for i in itertools.cycle('ha'):
    print(i)
    x += 1
    if x > 4:
        break

print('无限迭代repeat(elem[,n])')
# 无限迭代repeat()对比cycle()
x = 0
for i in itertools.repeat('ha'):
    print(i)
    x += 1
    if x > 4:
        break

# 迭代短序列
print('itertools模块 - 迭代短序列'.center(50, '*'))
# compress(data,selector) 类似于迭代器中的filter
a = [3, 5, 8, 9, 14]
b = itertools.compress(a, [1, 0, 1, 0])
print(list(b))
# filterfalse()
c = itertools.filterfalse(lambda x: x % 2 == 0, a)  # 把为真的都剔除掉了，剩下了奇数
print('c:', list(c))

# dropwile():一旦开始了就停不下
a = [3, 5, 8, 9, 14, 1, 4]
b = itertools.dropwhile(lambda x: x < 6, a)  # 一旦开始，后面的就不再管了
print(list(b))

# takewhile():一旦停下就开始不了
d = itertools.takewhile(lambda x: x > 6, a)
print('d:', list(d))  # 如果第一次就没取到，后面就没机会取到了

# tee(iterable,n): 把iterable里面的元素重复n次进行迭代，n必填，默认为2
# iterable作用被弱化
# 对比无限迭代中的cycle()
print('tee:')
for its in itertools.tee([1, 2, 3], 3):
    print(its)
    for it in its:
        print(it)

# 组合迭代
print('itertools模块 - 组合迭代'.center(50, '*'))
# product() 迭代出所有的排列，以元组形式return
a = itertools.product([1, 2], [3, 4], [5, 6])
print(a)
for i in a:
    print(i)

# permutations(seq,r) --> seq中r个元素的排列
print('permutations(seq,r) --> seq中r个元素的排列')

Arrange = itertools.permutations('abc', 2)  # A3(2) = 6个
for a in Arrange:
    print(a)

# combinations(seq,r) --> seq中r个元素的排列
print('combinations(seq,r) --> seq中r个元素的组合')

Combination = itertools.combinations('abcd', 2)
for c in Combination:
    print(c)

# 生成器Generator
print('生成器Generator'.center(50, '*'))


def myYield(n):
    while n > 0:
        print("开始生成...:")
        yield n
        print("完成一次...:")
        n -= 1


if __name__ == '__main__':
    # for i in myYield(4):
    #     print("遍历得到的值：",i)
    # print()

    my_yield = myYield(3)
    print('已经实例化生成器对象')
    my_yield.__next__()
    print('第二次调用__next__()方法：')
    my_yield.__next__()  # 恢复运行是从yield之后开始运行

print('利用生成器接收调用者传来的值：'.center(20, '*'))


def myYield(n):
    while n > 0:
        print('紧贴yield前面')
        rcv = yield n  # rcv（yield语句）就是等着接收send(n)变量的，
        print('@@@紧跟yield后面')
        n -= 1
        print('rcv现在是', rcv)  # 第一次执行到此处时(第二次next)，rcv没有send(n)时都是None
        if rcv is not None:
            n = rcv
            print('n现在是', n)


if __name__ == '__main__':
    my_yield = myYield(5)
    print(my_yield.__next__())
    print(my_yield.__next__())
    # print(my_yield.__next__())
    # print(my_yield.__next__())
    # print(my_yield.__next__()) # 此处及往上还是中规中矩
    # print(my_yield.__next__())
    print('下面send给生成器一个值，重新初始化生成器。')
    print(my_yield.send(10))  # send()在重置生成器的同时，也起到一轮next的作用！！
    # print(my_yield.__next__())

# 装饰器
print('装饰器Decorator'.center(50, '*'))


# 定义一个时间装饰器
def timecost(func):
    def wrapper(*args, **kwargs):
        import time
        t1 = time.time()
        # 被装饰的函数有返回值的话，这里要用变量接着，最后一层一层向外return
        value = func(*args, **kwargs)
        t2 = time.time()
        sub = t2 - t1
        print('Time Cost:%f seconds' % sub)
        return value

    return wrapper


# 测试自定义装饰器
@timecost
def isprime(n=3):
    if n <= 1:
        return False
    for i in range(2, n // 2 + 1):
        if n % i == 0:
            return False
        else:
            continue
    return True


print(isprime(999900000011111111111111111))
