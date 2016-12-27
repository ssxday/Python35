# 写一个根据日期计算星期几的模块
def whatday(s = '19860831'):
    #s是传进来的日期字符串
    s = str(s)  # 强制转换类型，传进来的是数字还是字符串都无所谓了
    import time,datetime
    time_s = list(time.strptime(s,'%Y%m%d'))
    # print(time_s)
    days = {
        0:'星期一',
        1:'星期二',
        2:'星期三',
        3:'星期四',
        4:'星期五',
        5:'星期六',
        6:'星期天'
    }
    return days[time_s[6]]  # 索引6代表星期

