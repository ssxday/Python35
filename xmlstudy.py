# -*- coding:utf-8 -*-
import xml.etree.ElementTree as ET
x = ET.parse('egg.xml')
print('parse()函数：',x,'可以用来验证良构性')
# Element类，实例化构建标签
root = ET.Element('shops',sell='goods')  # 标签对象
print('设好了root看一下：',root)
# 设置标签内容
root.text = 'www.cnshops.com'
# 构建子标签
wanda = ET.SubElement(root,'wanda')
haian = ET.SubElement(root,'haian')
# 孙标签
logo = ET.SubElement(wanda,'logo')
area = ET.SubElement(wanda,'Area')
revenue = ET.SubElement(wanda,'revenue')
logo.text = 'wanda'
area.text = "15678"
revenue.text = '174'

# 封装一个批量添加子标签的函数
# def struc(*tags,**subtags):
#     subobj = dict()
#     for tag in tags:
#         subobj[str(tag)] = list()
#         for subtag,text in subtags.items():
#             subtag = ET.SubElement(tag,subtag)
#             subtag.text = text
#             subobj[str(tag)].append(subtag)
#
#     return subobj
# subs = struc(haian,wanda,logo='default',area='100',revenue=147)
# print('封装后返回的对象列表',subs)

# 把标签及其子标签弄成tree
tree = ET.ElementTree(root)  # 树对象(一大堆结构化的标签对象)
print('把标签放进了tree里：',tree)
# 把tree结构化打印出来，类似于PHP的var_dump
ET.dump(tree)

# 把xml树写到文件里去
tree.write('print.xml')

# 字符实体entity
# help(ET.parse)
a = ET.XML('<a>haha<b>sub/&lt;tag</b></a>')
print('a=',a)
ET.dump(a)

# CDATA段<![CDATA[ ... ]]>
# 处理指令Procession Instruction
# 注释<!-- -->
# xml定义declaration
# <?xml version="1.0" encoding="utf-8"?>


# sax
from xml.sax import *
import xml.sax.handler as xh
# print(type(xml.sax.ContentHandler.characters))
# 内容处理接口ContentHandler
# help(xsax.ContentHandler)


class MyContentHandler(xh.ContentHandler):
    def startElement(self,name,attrs):
        print('标签名是%s'%name)
        print('attrs的类型是',attrs.items())  # <class 'xml.sax.xmlreader.AttributesImpl'>
        print()

    def characters(self,content):
        if content.strip() != '':
            print('characters是：',content.strip())

    def ignorableWhitespace(self,white):
        print('发现一处whitespace！')


class MyDTDHandler(xh.DTDHandler):
    def notationDecl(self,name,publicId,systemId):
        print('dtd哈：',name,publicId,systemId)
    pass

class MyEntityResolver(xh.EntityResolver):
    def resolveEntity(self,publicid,systemid):
        print('实体处理@',publicid,systemid)

class MyErrorHandler(xh.ErrorHandler):
    def error(self,exception):
        print('error:',exception)
    def warning(self,exception):
        print('warning#',exception)
# 创建一个parser对象
psr = make_parser()
# <xml.sax.expatreader.ExpatParser object at 0x101ca2048>
print('解析器parser对象：',psr)  # 打火
# 设置相应的handler
psr.setContentHandler(MyContentHandler())  # 挂档
psr.setDTDHandler(MyDTDHandler())
psr.setEntityResolver(MyEntityResolver())
psr.setErrorHandler(MyErrorHandler())
psr.parse('demo.xml')  # 踩油门

import xml.sax.xmlreader as xr
import xml.sax.expatreader as xp
help(xr.XMLReader)
# handler = psr.getContentHandler()
# print('handler',handler)

# ExpatParser
# (xml.sax.xmlreader.IncrementalParser, xml.sax.xmlreader.Locator)

# IncrementalParser(XMLReader)

