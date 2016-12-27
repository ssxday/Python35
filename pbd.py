# import pdb
#
# pdb.run('''
# for i in range(3):
#     print(i)
# ''')
# import pdb
def grade(n):
    '''
    >>> grade(95)
    'youxiu'
    >>> grade(80)
    'liang'
    '''
    if n > 90:
        return 'youxiu'
    elif n >80:
        return 'liang'
    else:
        return 'yiban'

if __name__ == '__main__':
    import doctest
    doctest.testmod()


print(grade(80))
print('haha')






