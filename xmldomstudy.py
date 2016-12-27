# -*- coding:utf-8 -*-
import xml.dom as xd
import xml.dom.minidom as xmini
from xml.dom import *
# help(xmini.DOMImplementation)
# DOMImplementation接口 - 判断DOM是否支持某些特性(Features)
print('DOMImplementation接口'.center(50,'*'))
impl = xmini.DOMImplementation()
print('DOMImplementation:',impl)
print(impl.hasFeature('events','2.0'))
print(impl._features)
print(impl.getInterface('xml'))  # 返回接口对象本身：self
doctype = impl.createDocumentType('good','unknown','fuck')
print('doctype:',doctype)
document = impl.createDocument('unknown','good',doctype)
print('生成了document:',document)

# Document接口,生成xml文档的访问入口,也就是根节点
print('Document接口'.center(50,'*'))
mydom = xmini.parse('demo.xml')
print('用parse函数生成：',mydom)  # Document object
docfromstr = xmini.parseString('<root />')
print('用parsestring函数生成：', docfromstr)  # Document object

# 创建元素节点
# 如果直接用DOM创建elem元素节点，那么目前看来，这个节点跟本DOM一点儿关系都没有
# 用DOM直接创建的元素节点，自己本身就是根节点，孤零零的
print('\n不用documentElement根节点，直接用DOM创建元素')
elem = docfromstr.createElement('sell')
print('创建元素节点elem：', elem)  # <DOM Element: sell at 0x10166f470>
print(type(elem.toxml()))  # 字面是toxml，实际是把对象变成xml字符串string
print('根节点的父节点是？',elem.parentNode)  # 返回None，用parentNode回不到自己的DOM
# 以上直接用DOM来创建各类节点是不推荐的，因为他们并不能回到原来的DOM
# 所以要用DOM的documentElement根节点来创建元素
print('\n使用documentElement根节点，用DOM的根节点创建元素：')
print('DOM有子节点吗？',docfromstr.hasChildNodes())
print('DOM的子节点列表？',docfromstr.childNodes)  # 根元素是DOM的0号子节点
docroot = docfromstr.documentElement
print('DOM的根节点documentElement', docroot)
print('DOM的子节点是否等于DOM的根节点:',  # 答案：True
      docroot == docfromstr.childNodes[0])
print('DOM的根节点的父节点还是DOM',docroot.parentNode)
print('DOM的根元素目前有无子节点？',docroot.hasChildNodes())
# 上条表达式返回False，说明前面创建的节点跟DOM的根节点一点关系没有
# 下面用DOM的根节点新建各类节点
print('jdhfahfafasdfa;bdpdsa',docroot.appendChild(elem))
print(docfromstr.toxml())
# docfromstr.createComment('wocaonima')
# print(docfromstr.toxml())
print()
print('@'*25)
# 创建文本节点
text = docfromstr.createTextNode('VeryGood')
print('文本节点',text)  # <DOM Text node "'VeryGood'">
# print(text.toxml())
# 创建属性节点
attr = docfromstr.createAttribute('madein')
print('属性节点：',attr)  # <xml.dom.minidom.Attr object at 0x101663570>
print(attr.nodeName)

# Node接口 被Document继承
# 获取DOM根节点 -> DOM对象的documentElement属性
print('Node接口'.center(50,'*'))
root = mydom.documentElement  # 根节点获取
print(root)  # 根节点
print(root.childNodes)


# Element接口
print('Element接口'.center(50,'*'))
# help(xmini.Document)

# Text接口
print('Text接口'.center(50,'*'))


# Comment接口
print('Comment接口'.center(50,'*'))


#

# help(xmini.Node.appendChild)





