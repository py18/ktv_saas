'''
    TODO: 子店信息管理
    功能：
    字段：门店名称，地址，街道地址，logo
'''

from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.db import transaction
from django.core.paginator import Paginator

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters

import uuid
import jwt
import base64
import time,datetime
import random

from werkzeug.security import generate_password_hash, check_password_hash

from apps.db_module import models
from utils.config import ini
from utils.code.return_code import ReCode
from utils import redis_cli
from app_funcs.merchant_file.child_manage import fcat_item,test,recursive_child

recode = ReCode()

class ChaildMerchantInfoManageView(APIView):

    def get(self, request, *args, **kwargs):
        '''
            TODO: 获取子店信息
            filter_values: 名称, 负责人姓名，负责人电话, 编号，创建时间
            id参数获取详情
        '''
        employee = request.employee
        id = request.GET.get("id", None)
        contact_person = request.GET.get("contact_person", None)
        contact_mobile = request.GET.get("contact_mobile", None)
        mer_no = request.GET.get("mer_no", None)
        mer_name = request.GET.get("mer_name", None)

        se_dict = {}
        if contact_person:
            se_dict["contact_person"] = contact_person
        if contact_mobile:
            se_dict["contact_mobile"] = contact_mobile
        if mer_no:
            se_dict["mer_no"] = mer_no
        if mer_name:
            se_dict["mer_name"] = mer_name
        se_dict["is_del"] = False
        try:
            # childs = models.Merchant.objects.filter(id=employee.merchant_id).values('merchant__id')
            # a_list = test([employee.merchant_id])
            a_list = [i for i in recursive_child([employee.merchant_id]) if i != None]
            se_dict["id__in"] = a_list
            childs_obj = models.Merchant.objects.filter(**se_dict)
            childs_list = []
            for i in childs_obj:
                childs_dict = {}
                childs_dict["id"] = i.id
                childs_dict["create_time"] = i.create_time
                childs_dict["update_time"] = i.update_time
                # childs_dict["is_del"] = i.is_del
                childs_dict["serial_number"] = i.serial_number
                childs_dict["mer_no"] = i.mer_no
                childs_dict["mer_name"] = i.mer_name
                childs_dict["cliarea"] = i.cliarea           
                childs_dict["cliaddress"] = i.cliaddress
                childs_dict["introduction"] = i.introduction
                childs_dict["logo"] = i.logo
                childs_dict["contact_person"] = i.contact_person
                childs_dict["contact_mobile"] = i.contact_mobile
                childs_dict["father_mer_id"] = i.father_mer_id

                childs_list.append(childs_dict)
            size = request.GET.get("size", 20)
            pg = request.GET.get("pg", 1)
            p = Paginator(childs_list, size)
            next_page = None
            previous_page = None
            page1 = p.page(pg)
            if page1.has_next():
                next_page = page1.next_page_number()
            if page1.has_previous():
                previous_page = page1.previous_page_number()
            data = {"count": p.count, "num_pages": p.num_pages, "next_page": next_page, "previous_page": previous_page,
                    "ret": page1.object_list}
            re_data = recode.success_func(data)
        except Exception as e:
            re_data = recode.error_func(-1,str(e))
        return JsonResponse(re_data)

    def post(self, request, *args, **kwargs):
        '''
            TODO: 新增分店
            test_json:{"mer_name":"测试分店","cliarea":"四川省,成都市,武侯区","cliaddress":"其他街道光明大厦奈何路58号","contact_person":"小李","contact_mobile":"13012345678"}
        '''
        employee = request.employee
        mer_name = request.data.get("mer_name", None)
        cliarea = request.data.get("cliarea", None)
        cliaddress = request.data.get("cliaddress", None)
        contact_person = request.data.get("contact_person", None)
        contact_mobile = request.data.get("contact_mobile", None)
        

        assert mer_name,(-14,"未填公司名")
        assert contact_person,(-15,"负责人未填")
        assert contact_mobile,(-16,"负责人电话未填")

        try:
            with transaction.atomic():
                mer = models.Merchant(mer_no = str(10000 + int(redis_cli.cache.incr('Regiester1'))), mer_name = mer_name, cliarea = cliarea, cliaddress = cliaddress,father_mer_id=employee.merchant_id,contact_person=contact_person,contact_mobile=contact_mobile)
                mer.save()
                mer_dep = models.MerchantDepartment(name="初始创建部",merchant=mer)
                mer_dep.save()
                mer_pos = models.MerchantPosition(name="初始创建者", merchant=mer, merchant_department=mer_dep)
                mer_pos.save()
                mer_emp = models.MerchantEmployee(name=contact_person,mobile=contact_mobile,merchant=mer,merchant_position=mer_pos,is_edit=True)
                mer_emp.save()
                data = {}
                re_data = recode.success_func(data)
        except Exception as e:
            re_data = recode.error_func(-1,str(e))
        return JsonResponse(re_data)

    def put(self, request, *args, **kwargs):
        '''
            TODO: 修改分店资料  
        '''
        employee = request.employee
        id = request.data.get("id", None)
        mer_name = request.data.get("mer_name", None)
        cliarea = request.data.get("cliarea", None)
        cliaddress = request.data.get("cliaddress", None)
        # contact_person = request.data.get("contact_person", None)
        # contact_mobile = request.data.get("contact_mobile", None)

        up_dict = {}
        if mer_name:
            up_dict["mer_name"] = mer_name
        if cliarea:
            up_dict["cliarea"] = cliarea
        if cliaddress:
            up_dict["cliaddress"] = cliaddress
        up_dict["update_time"] = datetime.datetime.now()
        try:
            with transaction.atomic():
                models.Merchant.objects.filter(id=id).update(**up_dict)
                re_data = recode.success_func(data={})
        except Exception as e:
            re_data = recode.error_func(-1,str(e))
        return JsonResponse(re_data)

    def delete(self, request, *args, **kwargs):
        '''
            TODO: 删除分店
        '''
        employee = request.employee
        id = request.data.get("id", None)
        try:
            with transaction.atomic():
                up_dict = {}
                up_dict["is_del"] = True
                up_dict["update_time"] = datetime.datetime.now()
                models.Merchant.objects.filter(id=id).update(**up_dict)
                re_data = recode.success_func(data={})
        except Exception as e:
            re_data = recode.error_func(-1,str(e))
        return JsonResponse(re_data)