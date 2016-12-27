# 冒泡排序法：升序排列
# 依次比较数列相邻元素的大小
def sort():
    sequence = input('输入要排列的数字，用逗号隔开：').split(',')
    bubble(sequence)
    # print(sequence)

def bubble(sequence):
    i = 0
    j = 0
    for j in range(len(sequence)-1,-1,-1):
        for i in range(0, j, 1):
            if sequence[i] > sequence[i + 1]:
                sequence[i], sequence[i + 1] = sequence[i + 1], sequence[i]
            print(sequence)

sort()
