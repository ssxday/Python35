# -*- coding:utf-8 -*-
class MyQuene:
    def __init__(self, size=10):
        self.size = size
        self.q = []

    def getin(self, element):
        if self._isFull():
            raise MyQueneException('the line is already full.')
        else:
            self.q.append(element)

    def getoff(self):
        if self._isEmpty():
            raise MyQueneException('the line has no one left.')
        else:
            return self.q.pop(0)

    def dismiss(self):
        self.q = []

    def _isFull(self):
        if len(self.q) == self.size:
            return True
        else:
            return False

    def _isEmpty(self):
        if len(self.q) == 0:
            return True
        else:
            return False


class MyQueneException(Exception):
    def __init__(self, note):
        self.note = note

    def __str__(self):
        return self.note


mq = MyQuene(7)
try:
    for i in range(1, 15):
        mq.getin(i)  # 入队
except MyQueneException:
    print(mq.q)

# 出队
print(mq.getoff())
print(mq.q)
