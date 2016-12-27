#!usr/bin/python
# -*- coding:utf-8 -*-


class myClass:
    """
    这是文档字符串
    """
    x = '本来的样子，我是类属性'  # 类属性

    def info(self):
        print('类属性myClass.x :', myClass.x)
        print('实例属性self.x :', self.x)

    def chglei(self):
        myClass.x = '类属性改了'

    def chgshili(self):
        self.x = '实例属性改了'

# myClass.info()
mc1 = myClass()
mc2 = myClass()

mc1.info()
mc2.info()

# print(' mc1修改实例属性'.center(50,'*'))
# mc1.chgshili()  # mc1修改了实例属性
# print(' mc1 '.center(20,'*'))
# mc1.info()
# print(' mc2 '.center(20,'*'))
# mc2.info()

"""
******* mc1 ********
类属性myClass.x : 本来的样子
实例属性self.x : 实例属性改了
******* mc2 ********
类属性myClass.x : 本来的样子
实例属性self.x : 本来的样子
"""
print(' mc1修改类属性'.center(50,'*'))
mc1.chglei()
print(' mc1 '.center(20,'*'))
mc1.info()
print(' mc2 '.center(20,'*'))
mc2.info()
"""
类属性myClass.x : 类属性改了
实例属性self.x : 类属性改了
类属性myClass.x : 类属性改了
实例属性self.x : 类属性改了
"""


class DemoMthd:
    c = '我是一个类属性'
    def __init__(self):
        self.c = '我是self的c属性'
    def normal(self):
        print("调用了正常方法")

    @classmethod
    def cls_mthd(cls):
        print('调用了类方法')
        print(cls.c)

    @staticmethod
    def static_mthd(s):
        print('调用了静态方法',s)

print('此时还没有实例化'.center(50,'*'))
DemoMthd.cls_mthd()
DemoMthd.static_mthd('还没实例化呢')
DemoMthd.normal('d')  #没有实例化的时候也可以调用一般的方法，只要传一个参数补齐self的位置

print('已经实例化了'.center(50,'*'))
dm = DemoMthd()
dm.cls_mthd()
dm.static_mthd('自己填上一个self吧')
dm.normal()

# 多重继承
print('多重继承'.center(50,'*'))
class Prta:
    def __init__(self):
        self.x = '我是x'
        self.y = '我是y'
        print('Prta类构造方法执行了！！')

    def show(self):
        print('我是父类A')


class Prtb:
    def __init__(self):
        print('Prtb的构造方法执行了')
    def show(self):
        print('我是父类B')
    def __selfish(self):
        print('我是Prtb带__的私有方法')


class Sub1(Prta,Prtb):
    """
    我是Sub1类的文档字符串
    """
    a = '我是类Sub1的a属性，不带self哦'
    b = '我是类Sub1的b属性，不带self哦'
    pass


class Sub2(Prtb,Prta):
    pass

class Sub3(Prta,Prtb):
    def show(self):
        Prta.show(self)  # 父类同名方法被覆盖后，要想调用父类方法时，要写出父类的名字进行调用
        Prtb.show(self)  # 调用父类方法，务必传入self，否则报错。

sub1 = Sub1()
sub2 = Sub2()
sub3 = Sub3()
print('以上是实例化过程')
sub1.show()  # show()是继承的
sub2.show()
sub3.show()
print('是否能继承父类的__私有方法？答案是不能。报错！')
# sub1._Prta__selfish()  # 答案是不能

"""
对象实例理所当然可以访问实例属性，
当实例属性与类属性重名时，对象访问到的只能是实例属性；
对象实例也可以访问到类属性，当且仅当，
没有实例属性与之重名的时候，访问不到实例属性，自然去找同名的类属性顶上
"""
print('\n类的特殊属性：')
# 类的特殊属性__class__
print('__class__是：', sub1.__class__)

# __dict__
print('__dict__是：', sub1.__dict__)

# __doc__
print('__doc__是：',sub1.__doc__)

# __module__
print('__module__是：',sub1.__module__)

#
print('__module__是：',myClass.__bases__)

#
print(Sub1)

# 重构类的特殊方法
# __init__()
print('\n重构类的特殊方法：')
print('Python中可以直接单独调用构造方法：')
sub1.__init__()

# 重构__new__() 创建单例模式
print('单利模式：')
class SingleIns:
    __instance = None
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls,*args,**kwargs)
        return cls.__instance
    def __init__(self):
        pass

si = SingleIns()
sii = SingleIns()
print(si)
print(sii)

# __getitem__()
class Shop(Sub3):
    def __init__(self):
        self.fruits = ['apple','banana','coconut','durian']
    # 把序列映射到实例对象上去
    def __getitem__(self, i):
        return self.fruits[i]
    def __str__(self):
        return 'This is a shop'
    def __len__(self):
        return len(self.fruits)
    def __call__(self, *args, **kwargs):
        print(self.fruits)
    def ts(self):
        print(super(Shop,self))



shop = Shop()  # 操作shop对象的序列，就等于操作self.fruits
for i in shop:
    print(i)
shop.foods = ['rice','noodle']  # 属性可以动态添加
print(shop.__dict__)  # 查看属性已经添加进去了
# __str__()
print(str(shop))
# __len__()
print('重构__len__()',len(shop))
# __call__()
print('call调用：')
shop()  # 调用shop()，本来没法调用
# super()
shop.ts()

# 抽象基类
print('抽象基类'.center(50,'*'))
from abc import ABCMeta,abstractmethod
class Viecle(metaclass=ABCMeta):
    @abstractmethod
    def drive(self):
        print('提前出发前进')
        pass
    def park(self):
        print('停车入库')

class Car(Viecle):
    def drive(self):
        super(Car, self).drive()
        print('前进')
    def fuel(self,l):
        print('加油%d升'%l)


bmw = Car()
bmw.fuel(50)
bmw.drive()



# help(super)


# 垃圾回收机制
# print('\n垃圾回收机制：')
# import gc
# # help(gc)
# print(gc.get_stats())
# print(gc.isenabled())
# print('清理个数：',gc.collect())






