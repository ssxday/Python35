# 税收计算程序
income = int(input('请输入您的收入：'))  # python3.x中，input的输入的内容默认为字符串
tax = 0
# 级别tier必须按升序排列，且税率rate与之一一对应，程序才能正常工作
tier = [0, 3500, 5000, 8000, 12500, 38500, 58500, 83500]
rate = [0, 0.03, 0.10, 0.20, 0.25, 0.30, 0.35, 0.40]
# 确定工资所在级别的位置
for i in range(len(tier)):
    if income < 0:
        exit('工资不能小于零')
    elif income >= tier[-1]:
        tax = (income - tier[-1]) * rate[-1]
        for x in range(len(tier)-1,0,-1):
            tax += (tier[x] - tier[x-1]) * rate[x-1]
    elif tier[i] <= income and income < tier[i + 1]:
        tax = (income - tier[i]) * rate[i]
        for j in range(i, 0, -1):
            tax += (tier[j] - tier[j - 1]) * rate[j-1]
print("需要缴纳的所得税为",tax,"元\n实际收入为",income - tax,'元')
