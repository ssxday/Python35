# -*- coding:utf-8 -*-
# 栈 stack


class MyStack:
    def __init__(self, size=5):
        self.size = size  # 栈容量
        self.stack = []  # 栈
        # self.top = -1  # 指定栈顶位置。Python由于有-1索引，用不到这一条

    def push(self, data):
        if not self._isfull():
            self.stack.append(data)
        else:
            raise MyStackException('MyStack Overflow')

    def pop(self):
        if not self._isempty():
            return self.stack.pop()
        else:
            raise MyStackException('MyStack Empty')

    def clearup(self):
        self.stack = []

    def _isfull(self):
        if len(self.stack) < self.size:
            return False
        else:
            return True

    def _isempty(self):
        if len(self.stack) == 0:
            return True
        else:
            return False


class MyStackException(Exception):
    def __init__(self, note=''):
        self.note = note

    def __str__(self):
        return self.note


ms = MyStack(5)
# 入栈
try:
    for i in range(1, 15):
        ms.push(i)
except MyStackException:
    print(ms.stack)

# 出栈
print(ms.pop())
print(ms.stack)
