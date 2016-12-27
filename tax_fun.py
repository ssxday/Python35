def tax():
    # 级别tier必须按升序排列，且税率rate与之一一对应，程序才能正常工作
    global tier,rate
    # 确定工资所在级别的位置
    for i in range(len(tier)):
        if income < tier[0]:
            exit('工资不能小于零')
        elif income >= tier[-1]:
            tax = (income - tier[-1]) * rate[-1]
            for x in range(len(tier) - 1, 0, -1):
                tax += (tier[x] - tier[x - 1]) * rate[x - 1]
        elif tier[i] <= income and income < tier[i + 1]:
            tax = (income - tier[i]) * rate[i]
            for j in range(i, 0, -1):
                tax += (tier[j] - tier[j - 1]) * rate[j - 1]

    return tax

# 只要函数内部不再另外赋值，引用时还是用外面的global
tier = [0, 3500, 5000, 8000, 12500, 38500, 58500, 83500]
rate = [0, 0.03, 0.10, 0.20, 0.25, 0.30, 0.35, 0.40]

if len(tier) != len(rate):
    exit("级别或税率设置有误")

income = int(input('请输入您的收入：'))
print("需要缴纳的所得税为", tax(), "元\n实际收入为", income - tax(), '元')
