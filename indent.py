# -*- coding: utf-8 -*- 加这一句可中文注释
import random
# print (random.path)

def compareNum(num1,num2):
    if num1 > num2:
        return 1
    elif num1 == num2:
        return 0
    else:
        return -1# English

num1 = random.randrange(1,9)
num2 = random.randrange(1,9)

print('num1=', num1)
print('num2=', num2)

rst = compareNum(num1,num2)
print (rst)

