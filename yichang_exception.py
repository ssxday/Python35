# -*- coding:utf-8 -*-
# 测试"错误"
ass = 'motherfucker'
# print(asss)

# 测试"异常"
# print(dir(__builtins__))  # 前面一大堆都是说的异常名称

class MyError(Exception):
    def __init__(self,value):
        self.tips = value

    def __str__(self):
        return self.tips


class FuckError(Exception):
    def __init__(self,tips='dont do that'):
        self.tips = tips

    def __str__(self):
        return self.tips

# 手动抛出异常
for i in range(5):
    try:
        if i == 2:
            raise FuckError
    except FuckError as e:
        print('Fuck!被捕获了',e.__str__())
    else:
        print('motherfucker跑了')
    print(i)


# assert语句
    # assert <条件>   条件为假时才抛出异常
    # except用AssertionError来捕获
try:
    assert 2==1
except AssertionError:
    print('断言错了')
