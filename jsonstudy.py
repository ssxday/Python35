# -*- coding:utf-8 -*-
"""
Licensed Materials - Property of SSX
Copyright statement and purpose...
-----------------------------------------------------
File Name:
Author:
Version:
Description:

"""
import json

pythondict = {
    'a': 'apple',
    'b': 'banana',
    'c': {
        'usd': 'dollar',
        'cny': 'yuan'
    }
}
print('这是Python字典', pythondict)
# 把Python对象转成JSON字符串
print('python -> JSON')
p2j = json.dumps(pythondict)
print('这是由Python字典转换成的JSON格式的字符串:\n', p2j, '\n其类型是：', type(p2j))
print('写入json文件：')
with open('json.json', 'w') as f:
    a = json.dump(p2j, f)
    print('返回：', a)
# 写入文件的是下面这串内容
"{\"a\": \"apple\", \"b\": \"banana\", \"c\": {\"cny\": \"yuan\", \"usd\": \"dollar\"}}"

# 把JSON转换为Python对象
print('\nJSON -> python')
jsonstr = '{"a": "apple", "c": {"cny": "yuan", "usd": "dollar"}, "b": "banana"}'
j2p = json.loads(jsonstr)
print('JSON字符串转化成了Python对象：', j2p)
print('这个对象的类型是：', type(j2p))  # dict
print('从.json文件里读取json内容并转化：')
with open('json.json', 'r') as jsonfromfile:
    jf2p = json.load(jsonfromfile)
    print('从json文件中转化成的Python与JSON同型的字符串', jf2p)
    print('再用loads把字符串变成Python的结构化对象字典')
    fin = json.loads(jf2p)
    print(fin, '其类型是：', type(fin))
    # fins = json.loads(jsonfromfile.read())
    # print(fins)
