# -*- coding:utf-8 -*-
class BTree:
    def __init__(self, value):
        self.left = None
        self.right = None
        self.value = value

    def setleftson(self, son):
        self.left = BTree(son)
        return self.left

    def setrightson(self, son):
        self.right = BTree(son)
        return self.right

    def display(self):
        print(self.value)


root = BTree('ROOT')
A = root.setleftson('A')
B = root.setrightson('B')
C = A.setleftson('C')
D = A.setrightson('D')
# print(D.value)
E = B.setrightson('E')
F = D.setleftson('F')
G = D.setrightson('G')


# 用left或right进行导航
# root.left.right.left.display()

# 遍历二叉树，三种次序
# 先序遍历
def preorder(tree):
    if tree:
        tree.display()
        if tree.left:
            preorder(tree.left)
        if tree.right:
            preorder(tree.right)


# 中序遍历
def inorder(tree):
    if tree:
        if tree.left:
            inorder(tree.left)
        tree.display()
        if tree.right:
            inorder(tree.right)


# 后序遍历
def postorder(tree):
    if tree:
        if tree.left:
            postorder(tree.left)
        if tree.right:
            postorder(tree.right)
        tree.display()


print('先序遍历：')
preorder(root)
print('中序遍历：')
inorder(root)
print('后序遍历:')
postorder(root)

# 二叉树排序
print('二叉树排序：')
p = [3, 5, 20, 7, 43, 2, 15, 30]







