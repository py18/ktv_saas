'''
    该为格式化输入方法，包含： 输出时间格式化， 货币输出格式化等

'''


import datetime,time
import decimal


def two_decimal_func(num):
    '''
        TODO: 格式化int（金钱/分）输出，保留两位小数，并转换为（元） 除以100
    '''
    return str(decimal.Decimal("%.2f" % float(0.00))) if num is None else str(decimal.Decimal("%.2f" % float(int(num)/100)))

def two_decimal_not_divided_by_100(num):
    '''
        TODO: 格式化int（金钱/分）输出，保留两位小数，并转换为（元）
    '''
    return str(decimal.Decimal("%.2f" % float(0.00))) if num is None else str(decimal.Decimal("%.2f" % float(int(num))))


def put_time_format(stime):
    '''
        TODO: 转换时间输出样式为 ： '%Y-%m-%d %H:%M:%S'
    '''
    atime = datetime.datetime.now()
    if type(stime) != type(atime):
        raise Exception({"code":-115,"msg":"后台时间类型出现错误，必须是datetime"})
    return stime.strftime('%Y-%m-%d %H:%M:%S')

def value_int_return(va):
    if va:
        a = int(va)
    else:
        a = 0
    return a

def time_in_range(begin,end):
        #如果当前时间在活动范围内，则返回“真”
    
    curr = datetime.datetime.now().time()
    begin_hours, begin_min = begin.split(':')
    end_hours, end_min = end.split(':')
    start_time = datetime.time(int(begin_hours), int(begin_min))
    end_time = datetime.time(int(end_hours), int(end_min))
    if start_time <= end_time:
        return start_time <= curr <= end_time
    else:
        return start_time <= curr or curr <= end_time

def jisuan_time(stime):
    now_time = datetime.datetime.now()
    now_time_unix = time.mktime(now_time.timetuple())
    stime_unix = time.mktime(stime.timetuple())
    long_s = now_time_unix - stime_unix
    a = 60 * 60
    ru = round(long_s/a,1)
    return ru

def comparison_time(begin,end):
        #如果当前时间在活动范围内，则返回“真”
    
    begin_hours, begin_min = begin.split(':')
    end_hours, end_min = end.split(':')
    start_time = datetime.time(int(begin_hours), int(begin_min))
    end_time = datetime.time(int(end_hours), int(end_min))
    if start_time > end_time:
        return 1
    else:
        return 0

def comparison_time_gte(begin,end):
        #时间对比 begin >= end
    
    begin_hours, begin_min = begin.split(':')
    end_hours, end_min = end.split(':')
    start_time = datetime.time(int(begin_hours), int(begin_min))
    end_time = datetime.time(int(end_hours), int(end_min))
    if start_time >= end_time:
        return 1
    else:
        return 0

def comparison_time_lt(begin,end):
        #时间对比 begin < end
    
    begin_hours, begin_min = begin.split(':')
    end_hours, end_min = end.split(':')
    start_time = datetime.time(int(begin_hours), int(begin_min))
    end_time = datetime.time(int(end_hours), int(end_min))
    if start_time < end_time:
        return 1
    else:
        return 0