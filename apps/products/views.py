from django.db import transaction
from django.http import JsonResponse
from rest_framework.views import APIView
from apps.db_module import models
from apps.products.products_func import get_page
from utils.code.return_code import ReCode


class SpecificationsView(APIView):
    '''创建商品的基础规格单位'''
    def post(self,request,*args,**kwargs):
        name = self.request.data.get('name',None)
        serial_number = self.request.data.get('serial_number')
        merchant_employee_id = self.request.data.get('merchant_employee_id')
        merchant_id = self.request.data.get('merchant_id')

        assert name,(-101,'name为必传字段')
        assert merchant_employee_id, (-101, 'merchant_employee_id为必传字段')
        assert merchant_id, (-101, 'merchant_id为必传字段')

        obj = models.MerchantSpecification.objects.filter(name=name,merchant_id=merchant_id,is_del=False)
        if len(obj) != 0:
            return JsonResponse(ReCode().error_func(status=0,error='该属性名已创建'))
        else:
            try:
                with transaction.atomic():
                    specifications = models.MerchantSpecification(
                        name=name,
                        merchant_id=merchant_id,
                        serial_number=serial_number,
                        merchant_employee_id=merchant_employee_id
                    )
                    specifications.save()
            except Exception as w :
                return JsonResponse (ReCode().error_func(status=-1,error=str(w)))
            return JsonResponse (ReCode().success_func(data={}))

    def get(self,request,*args,**kwargs):
        id = self.request.GET.get('id',None)
        merchant_id = self.request.GET.get('merchant_id')
        size = self.request.GET.get("size", 10)
        pg = self.request.GET.get("pg", 1)

        assert merchant_id,(-101,'merchant_id为必须字段')
        try:
            if id:
                obj_set = models.MerchantSpecification.objects.filter(id=id,merchant_id=merchant_id,is_del=False)
            else:
                obj_set = models.MerchantSpecification.objects.filter(merchant_id=merchant_id,is_del=False)
            re_list = []
            for x in obj_set:
                re_dict = {}
                re_dict['id'] = x.id
                re_dict['name'] = x.name
                re_dict['merchant_employee'] = x.merchant_employee.name
                re_dict['serial_number'] = x.serial_number
                re_list.append(re_dict)
            # 排序
            re_list = sorted(re_list, key=lambda e: e.__getitem__('serial_number'))

            data = get_page(re_list,size,pg)
        except Exception as w:
            return JsonResponse(ReCode().error_func(status=-1,error=w))
        return JsonResponse(ReCode().success_func(data=data))

    def put(self,request,*args,**kwargs):
        pass
    def delete(self,request,*args,**kwargs):
        pass