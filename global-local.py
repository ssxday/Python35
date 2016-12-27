_a = 3
_b = 5
def plus():
    # _a = 8
    global _a
    _a = 8
    _b = 9
    return _a + _b #visited the global variables

print(plus())
print(_b)
print(_a)