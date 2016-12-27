# -*- coding:utf-8 -*-
# 有向图：节点+路径
# 构建"图"
graph = {
    'A': ['C', 'B', 'D'],
    'B': ['E', ],
    'C': ['D', 'F'],
    'D': ['E', 'G'],
    'E': [],
    'F': ['D', 'G'],
    'G': ['E', ]
}


# 搜索图
def search(graph, start, desti):
    roads = []
    pathgen(graph, [start], desti, roads)
    roads.sort(key=lambda x: len(x))
    return roads


def pathgen(graph, path, desti, roads):
    """

    :param graph: 以字典构造的图
    :param path: <list> 由节点依次排列形成的路线列表
    :param desti: 指定终点
    :param roads: <list> 所有可行的路线的列表。PS:roads需要参与迭代，不能再内部初始化的
    :return: None
    """
    posi = path[-1]
    if posi == desti:
        # 找到目的地
        roads.append(path)
    else:  # 没找到目的地的情况
        for i in graph[posi]:
            if i not in path:  # 不走回头路？
                pathgen(graph, path + [i, ], desti, roads)


r = search(graph, 'A', 'E')

for i in r:
    print(i)
