# -*- coding:utf-8 -*-
import xml.dom.minidom as xmini
# 搜索node下的元素节点
def lookfortag(node,tagname):
    tags = node.getElementsByTagName(tagname)
    return tags

def lookforattr(elem,attr):
    pass











