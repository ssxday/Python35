# -*- coding: utf-8 -*-
# 列表作为参数传递

def jisuan(args=[]):
    x, y = args  # 在函数内部解包，但参数数量必须等于列表长度
    return x + y


print(jisuan([1, 2]))  # 参数需要传列表，而不能只传值


# 传递可变参数！！！
def changing(*args):  # 用*表示引用元组
    print(args)


changing(1, 2, 3, 6)


def search(*t, **d):  # 用**表示引用字典
    keys = d.keys()
    values = d.values()
    print(keys, values)
    for i in t:
        for k in keys:
            if i == k:
                print('find:', d[k])


# *务必要写在**前面！！
search(1, 'two', 'one', two='twooooooo')  # 实参不能加引号


# 函数返回多个值
# 思路：打包进元组，调用时解包
def fanhuiduogezhi(x, y, z):
    l = [x, y, z]
    l.reverse()
    numbers = tuple(l)
    return numbers


# fanhuiduogezhi()最终返回的实际是一个元组，调用时拆包
x, y, z = fanhuiduogezhi(7, 8, 9)
print(z)


def fanhuiduo(*t):
    l = list(t)
    l.reverse()
    a, b, c = tuple(l)
    return a, b, c


x, y, z = fanhuiduo(6, 9, 15)  # 如果在函数内部解包了，也要在外面分别对应上
print(x)

# lambda匿名函数
# 1、变量可以作为函数使用
lmd = lambda x, y: x ** y
print(lmd(2, 3))

# 2、lambda直接做函数
print((lambda x: -x)(-19))  # 求相反数


# 注意：lambda中只能用表达式，不能用判断、循环这类多重语句

# generator函数，在循环中，一次只返回一个值
def gnrt(n):
    for i in range(n):
        yield i ** 2


print("gnrt:", gnrt(6))
r = gnrt(6)
print(r.__next__())

# exercise5
s = lambda x, y: x + y
print('exercise5:\n', s('aa', 'bb'))

print('*' * 30)
# 函数中引用的全局变量，只是那个模块中的全局变量。
from gl import foo_fun

name = 'Current module'


def bar():
    print('当前模块中函数bar:')
    print('变量name：', name)


def call_foo_fun(fun):
    fun()


if __name__ == '__main__':
    bar()
    print()
    foo_fun()
    print()
    call_foo_fun(foo_fun)

# 闭包：打包函数和函数的执行环境，比如函数所需的全局变量，都在一个大的闭包对象里
print('\n闭包:')
s = '模块级全局变量'
def bibao():
    s  = '嵌入函数的执行环境'
    def show(s):
        print(s)

    show(s)

bibao()  # 可见是里面的s被执行了

# 延迟执行
print('延迟执行 及 泛型函数：')

def delay_func(a,b):
    def eryuanyicifangcheng(x):
        print(a * x + b)
    return eryuanyicifangcheng

eyyc = delay_func(3,4)
print(eyyc)
eyyc(8)

print('上下文管理器：')
class FileMgr:
    """
    定义一个文件资源打开、关闭的管理器
    """
    def __init__(self,pathname):
        self.pathname = pathname
        self.f = None  # 此时还不用open文件资源

    def __enter__(self):
        self.f = open(self.pathname, 'r', encoding='utf-8')
        return self.f  # __enter__()一定要把资源return出来，as语句将与之绑定！！

    def __exit__(self, exc_type, exc_val, exc_tb):  # 各种exc参数用来跟踪错误
        # 退出with语句时执行
        if self.f:
            self.f.close()
            print('file closed.')

# 使用上下文管理器（ContextManager）
with FileMgr('./chaoxie.txt') as f:
    l1 = f.readline()
    f.readline()
    l2 = f.readline()
    print(l1, l2)
# with结束之时，资源也就关闭了，不用再手动关一次

# 使用装饰器装饰生成器，使其变成一个上下文管理器，那么yield后的表达式即为as后的变量
import contextlib
# help(contextlib.ContextDecorator)


@contextlib.contextmanager
def my_gnr(n):
    print('yield之前')
    yield n
    print('yield结束')

m5 = my_gnr(5)

# 使用上下文管理器
with m5 as val:
    print(val)
    print(val)
    print(val)
    print(val)
    print(val)

print(hasattr(m5,"__enter__"))

class DemoClass:
    class_val = 'leishuxing'
    def __init__(self):
        self.x = 'shilix'
        print(self.class_val)

# 用字符串操作对象属性
print('用字符串操作对象属性'.center(30,'*'))
dc = DemoClass()
# print(dc.class_val)
# print(DemoClass.class_val)
setattr(DemoClass,'fuck','zhangsan')
print('newly created attibute fuck:',DemoClass.fuck)

# 用字典构造分支结构
print('用字典构造分支结构'.center(30,'*'))
def branch_a():
    print('分支a')
def branch_b():
    print('fuckb')
def branch_c():
    print('c')
# 构造函数字典，跟switch...case...差不多
func_dict = {
    'a': branch_a,  # 不加括号
    'b': branch_b(),  # 一旦加括号，就会直接执行里面的print了
    'c': branch_c
}
# 调用
func_dict['c']()  # 加括号调用

# 鸭子类型 duck typing
print('鸭子类型 duck typing'.center(30,'*'))
class Duck:
    def jiaosheng(self):
        print('gagaga')
class Cat:
    def jiaosheng(self):
        print('miaomiaomiao')
class Tree():
    pass
# 以上是三种类,下面实例化
duck = Duck()
cat = Cat()
tree = Tree()
# 定义一个函数，可以调用任何带有jiaosheng方法的对象
def jiaoqilai(obj):
    obj.jiaosheng()

# 调用jiaoqilai
jiaoqilai(cat)  # 让猫叫起来
jiaoqilai(duck)  # 让鸭子叫起来
# jiaoqilai(tree)  # 让树叫起来 会出错，因为Class Tree里面没有定义jiaosheng方法



