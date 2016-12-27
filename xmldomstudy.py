# -*- coding:utf-8 -*-
import xml.dom as xd
import xml.dom.minidom as xmini
from xml.dom import *

# help(xmini.DOMImplementation)
# DOMImplementation接口 - 判断DOM是否支持某些特性(Features)
print('DOMImplementation接口'.center(50, '*'))
impl = xmini.DOMImplementation()
print('DOMImplementation:', impl)
print(impl.hasFeature('events', '2.0'))
print('查看Implementation的特性：', impl._features)
print(impl.getInterface('xml'))  # 返回DOMImplementation接口对象本身：self
doctype = impl.createDocumentType('good', 'unknown', 'fuck')
print('doctype:', doctype)
document = impl.createDocument('unknown', 'good', doctype)
print('生成了document:', document)

# Document接口,生成xml文档的访问入口,也就是根节点
print('Document接口'.center(50, '*'))
mydom = xmini.parse('demo.xml')
print('用parse函数生成：', mydom)  # Document object
docfromstr = xmini.parseString('<root />')
print('用parsestring函数生成：', docfromstr)  # Document object

# DOM生成的时候，其根节点已然诞生，就是documentElement
docroot = docfromstr.documentElement
print('DOM的根节点documentElement', docroot)
print('DOM的子节点是否等于DOM的根节点:',  # 答案：True
      docroot == docfromstr.childNodes[0])
print('DOM的根节点的父节点还是DOM', docroot.parentNode)

# 创建元素节点
# 创建节点即实例化节点Node类，是由DOM(Document)提供的方法来创建的
# 当一个节点被创建时，他就是一个孤零零的节点对象，并不与DOM有什么关系
print('\n创建元素节点')
elem_car = docfromstr.createElement('car')
elem_plane = docfromstr.createElement('plane')
print('元素节点elem：', elem_car)  # <DOM Element: sell at 0x10166f470>
print(type(elem_car.toxml()))  # 字面是toxml，实际是把对象变成xml字符串string
print('根节点的父节点是？', elem_car.parentNode)  # 返回None，用parentNode回不到自己的DOM
print('DOM有子节点吗？', docfromstr.hasChildNodes())
print('DOM的子节点列表？', docfromstr.childNodes)  # 根元素是DOM的0号子节点
# 给元素节点添加属性，方法一
elem_car.setAttribute('Vol','3.0T')
print(elem_car.attributes)

print()
# print('@' * 25)

# 创建文本节点
text = docfromstr.createTextNode('A fancy car')
print('文本节点', text)  # <DOM Text node "'VeryGood'">
print('文本节点的类型值', text.nodeType)  # 3
print('文本节点的节点名称', text.nodeName)  # #text
print('文本节点的值', text.nodeValue)  # A fancy car
print('在xml文档中的表现形式',text.toxml())

# 创建属性节点
print()
attr = docfromstr.createAttribute('MadeIn')  # 生成属性节点时只定义了属性名
print('属性节点：', attr)  # <xml.dom.minidom.Attr object at 0x101663570>
attr.value = 'China'  # 设置属性节点的属性值
print('测试是否是同一个',attr.value is attr.nodeValue)

# 注释节点
comment1 = docfromstr.createComment('i want to buy this car')
print('\n注释节点：',comment1)
print(comment1.nodeValue)  # 对比
print(comment1.toxml())  # 对比

# 把创建的各类型节点按层次【挂】上去
print('把car挂到根节点下：', docroot.appendChild(elem_car))
print('把plane挂到根节点下：', docroot.appendChild(elem_plane))
elem_car.appendChild(text)
elem_car.appendChild(comment1)
# 给元素节点添加属性，方法二。其他的节点都可以用appendChild()
# 唯独属性节点要用setAttributeNode
# 元素节点的属性并不是属性节点，而是NamedNodeMap对象，
# 属性节点只是作为参数传入元素对象的setAttributeNode()方法
elem_car.setAttributeNode(attr)

print('打印DOM：', docfromstr.toxml())

# Node接口 被Document继承
print('Node接口'.center(50, '*'))
# 节点类型 nodeType
print('节点类型nodeType：', attr.nodeType)  # 2
print('节点类型nodeType：', docroot.nodeType)  # 1
print('节点类型nodeType：', text.nodeType)  # 3
print('节点类型nodeType：', docfromstr.nodeType)  # 9 DOM也算一个大节点
# 获取DOM根节点 -> DOM对象的documentElement属性
root = mydom.documentElement  # 根节点获取
print(root)  # 根节点
print(root.childNodes)

# Element接口
print('Element接口'.center(50, '*'))
# help(xmini.Document)

# Text接口
print('Text接口'.center(50, '*'))

# Comment接口
print('Comment接口'.center(50, '*'))


#

# help(xmini.NamedNodeMap)
