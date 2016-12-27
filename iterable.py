# 序列 对string,tuple,list通用
# len()
# sum()
# all()
# any()
# min()
# max()
# #

ll = [1, 2, 5, 3.2]
print(max(ll))

ll = ['a', '', 'T', '}']
print('max()执行：', max(ll))  # 按ascii码排
print('all()执行：', all(ll))
print('any()执行：', any(ll))
