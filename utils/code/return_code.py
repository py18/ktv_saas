'''
    return Json models
'''
import datetime

class ReCode(object):

    def error_func(self, status, error):
        
        data = {
            "status":status,  # 状态
            "error":error,  # 错误提示
            "message": "操作失败",  # 信息
            "timestamp":datetime.datetime.now(),  # 时间
        }
        return data

    def success_func(self,data: dict):

        re_data = {
            "status":1,
            "message":"操作成功",
            "data":data,
            "timestamp":datetime.datetime.now()
        }
        return re_data