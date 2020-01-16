from django.core.paginator import Paginator
from django.http import JsonResponse
from rest_framework.views import APIView

from db_module import models
from db_module.db_module_func import create_merchant, get_timestamp, get_merchant, pg_fun, re_ok_func, re_no_func


class CreateMerchant(APIView):
    def post(self,request,*args,**kwargs):
        data = self.request.data
        re_dict = {}
        try:
            info = create_merchant(data)
            if info == 'ok':
                re_dict['status'] = 1
                re_dict['data'] = None
                re_dict['message'] = '成功'
                re_dict['timestamp'] = get_timestamp()
        except Exception as w:
            re_dict['status'] = -1
            re_dict['error'] = w
            re_dict['message'] = '失败'
            re_dict['timestamp'] = get_timestamp()
        return JsonResponse(re_dict)


    def get(self,request,*args,**kwargs):
        id = self.request.GET.get('id',None)
        size = request.GET.get("size", 10)
        pg = request.GET.get("pg", 1)
        try:
            info = get_merchant(id)
            data = pg_fun(info,size,pg)
            re_info = re_ok_func(data)
        except Exception as w:
            re_info = re_no_func(w)
        return JsonResponse(re_info)

