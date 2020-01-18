'''
    TODO: 新增分店
    字段：门店名称，联系人，联系电话，门店地址，街道地址
    新增门店超级管理员初始密码为：123456
'''

from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.db import transaction
from django.core.paginator import Paginator

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import filters
from flask_restful import reqparse

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

recode = ReCode()

parser = reqparse.RequestParser()
parser.add_argument('mobile', required=True, type=str)
parser.add_argument('name', required=True, type=str)
parser.add_argument('sex', required=True, type=int)
parser.add_argument('identity_number', required=True, type=str)
parser.add_argument('merchant_position_id', required=True, type=int)


class DepartmentManageView(APIView):

    def get(self, request, *args, **kwargs):
        '''
        TODO: 获取部门列表
        filter_values: 可根据分店id来获取, name
        '''
        employee = request.employee
        mer_id = request.GET.get("mer_id", employee.merchant_id)
        name = request.GET.get("name", None)
        id = request.GET.get("id", None)

        se_dict = {}
        se_dict["merchant_id"] = mer_id
        se_dict["is_del"] = False
        if name:
            se_dict["name__icontains"] = name
        if id:
            se_dict["id"] = id
        try:
            dep_obj = list(models.MerchantDepartment.objects.filter(**se_dict).values())
            size = request.GET.get("size", 20)
            pg = request.GET.get("pg", 1)
            p = Paginator(dep_obj, size)
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
        TODO: 新增部门
        '''
        employee = request.employee
        name = request.data.get("name", None)
        remark = request.data.get("remark", '')

        try:
            with transaction.atomic():
                # 判断部门是否存在
                dep_old = models.MerchantDepartment.objects.filter(is_del=False, merchant_id=employee.merchant_id, name=name)
                assert not dep_old,(-17, "部门已存在")
                dep = models.MerchantDepartment(name=name,remark=remark,merchant_id=employee.merchant_id)
                dep.save()
                re_data = recode.success_func(data={})
        except Exception as e:
            re_data = recode.error_func(-1,str(e))
        return JsonResponse(re_data)
    
    def put(self, request, *args, **kwargs):
        '''
        TODO: 修改部门
        '''
        employee = request.employee
        id = request.data.get("id", None)
        assert id,(-9,"关键参数，id未传")
        name = request.data.get("name", None)
        remark = request.data.get("remark", None)

        up_dict = {}
        if name:
            up_dict["name"] = name
        if remark:
            up_dict["remark"] = remark
        try:
            with transaction.atomic():
                # 查看修改的部门名称是否存在
                a_obj = models.MerchantDepartment.objects.get(id=id)
                assert a_obj.is_del == False,(-22, "该内容不存在")
                dep_old = models.MerchantDepartment.objects.filter(merchant_id=a_obj.merchant_id,name=name, is_del=False).exclude(id=id)
                assert len(dep_old) == 0,(-23,"该部门已存在")
                up_dict["update_time"] = datetime.datetime.now()
                models.MerchantDepartment.objects.filter(id=id).update(**up_dict)
                re_data = recode.success_func(data={})
        except Exception as e:
            re_data = recode.error_func(-1,str(e))
        return JsonResponse(re_data)

    def delete(self, request, *args, **kwargs):
        '''
        TODO: 删除部门
        '''
        employee = request.employee
        id = request.data.get("id", None)
        assert id,(-9,"关键参数，id未传")
        try:
            with transaction.atomic():
                # 判断该部门下是否有未删职位
                dep_old = models.MerchantPosition.objects.filter(merchant_department_id=id, merchant_id=employee.merchant_id,is_del=False)
                assert len(dep_old) == 0,(-18,"当前部门下存在职位，无法删除")
                up_dict = {}
                up_dict["update_time"] = datetime.datetime.now()
                up_dict["is_del"] = True
                models.MerchantDepartment.objects.filter(id=id).update(**up_dict)
                re_data = recode.success_func(data={})
        except Exception as e:
            re_data = recode.error_func(-1,str(e))
        return JsonResponse(re_data)


class PositionManageView(APIView):

    def get(self, request, *arga, **kwargs):
        '''
        TODO: 获取职位列表 根据id获取单条详细
        filter_values: 部门， 职位名, name
        '''
        employee = request.employee
        id = request.GET.get("id", None)
        assert id,(-9,"关键参数，id未传")
        name = request.GET.get("name", None)
        merchant_department_id = request.GET.get("merchant_department_id", None)
        mer_id = request.GET.get("mer_id", employee.merchant_id)

        se_dict = {}
        se_dict["is_del"] = False
        se_dict["merchant_id"] = mer_id
        if id:
            se_dict["id"] = id
        if name:
            se_dict["name__icontains"] = name
        if merchant_department_id:
            se_dict["merchant_department_id"] = merchant_department_id
        
        try:
            posi_obj = list(models.MerchantPosition.objects.filter(**se_dict).values())
            size = request.GET.get("size", 20)
            pg = request.GET.get("pg", 1)
            p = Paginator(posi_obj, size)
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
        TODO: 新建职位
        '''
        employee = request.employee
        name = request.data.get("name", None)
        merchant_department_id = request.data.get("merchant_department_id", None)
        is_leader = request.data.get("is_leader", False)
        remark = request.data.get("remark", None)

        assert name,(-19,"部门名称未填")
        assert merchant_department_id,(-20,"部门未填")

        try:
            with transaction.atomic():
                # 查看职位名称是否存在
                posi_old = models.MerchantPosition.objects.filter(merchant_department_id=merchant_department_id, name=name, is_del=False)
                assert not posi_old,(-21, "职位已存在")
                models.MerchantPosition.objects.create(name=name,merchant_department_id=merchant_department_id,is_leader=is_leader,remark=remark,merchant_id=employee.merchant_id)
                re_data = recode.success_func(data={})
        except Exception as e:
            re_data = recode.error_func(-1,str(e))
        return JsonResponse(re_data)
    
    def put(self, request, *args, **kwargs):
        '''
        TODO: 修改职位
        '''
        employee = request.employee
        id = request.data.get("id", None)
        assert id,(-9,"关键参数，id未传")
        name = request.data.get("name", None)
        is_leader = request.data.get("is_leader", None)
        remark = request.data.get("remark", None)

        up_dict = {}
        if name:
            up_dict["name"] = name
        if type(is_leader) == int:
            up_dict["is_leader"] = int(is_leader)
        if remark:
            up_dict["remark"] = remark
        try:
            with transaction.atomic():
                # 查看修改之后名字是否重复 除开自己
                p_obj = models.MerchantPosition.objects.get(id=id)
                assert p_obj.is_del == False,(-22, "该内容不存在")
                posi_old = models.MerchantPosition.objects.get(merchant_department_id=p_obj.merchant_department_id, name=name, is_del=False).exclude(id=id)
                assert not posi_old,(-21, "职位已存在")
                up_dict["update_time"] = datetime.datetime.now()
                models.MerchantPosition.objects.filter(id=id).update(**up_dict)
                re_data = recode.success_func(data={})
        except Exception as e:
            re_data = recode.error_func(-1,str(e))
        return JsonResponse(re_data)

    def delete(self, request, *args, **kwargs):
        '''
        TODO: 删除职位
        '''
        employee = request.employee
        id = request.data.get("id", None)
        assert id,(-9,"关键参数，id未传")
        try:
            with transaction.atomic():
                p_old = models.MerchantEmployee.objects.filter(merchant_position_id=id, merchant_id=employee.merchant_id,is_del=False)
                assert len(p_old) == 0,(-18,"当前部门下存在员工，无法删除")
                up_dict = {}
                up_dict["update_time"] = datetime.datetime.now()
                up_dict["is_del"] = True
                models.MerchantPosition.objects.filter(id=id).update(**up_dict)
                re_data = recode.success_func(data={})
        except Exception as e:
            re_data = recode.error_func(-1,str(e))
        return JsonResponse(re_data)


class StaffManageView(APIView):

    def get(self, request, *args, **kwargs):
        '''
            TODO: 获取员工列表 , 可根据店id（可看分店员工）
            filter_values: 员工姓名，员工电话，创建时间， 性别, 身份证号, 职位, 部门
        '''
        employee = request.employee
        mer_id = request.GET.get("mer_id", employee.merchant_id)
        mobile = request.GET.get("mobile", None)
        name = request.GET.get("name", None)
        sex = request.GET.get("sex", None)
        identity_number = request.GET.get("identity_number", None)
        merchant_position_id = request.GET.get("merchant_position_id", None)
        merchant_department_id = request.GET.get("merchant_department_id", None)

        se_dict = {}
        se_dict["merchant_id"] = mer_id
        se_dict["is_del"] = False
        if mobile:
            se_dict["mobile"] = mobile
        if name:
            se_dict["name__icontains"] = name
        if sex:
            se_dict["sex"] = sex
        if identity_number:
            se_dict["identity_number"] = identity_number
        if merchant_position_id:
            se_dict["merchant_position_id"] = merchant_position_id
        if merchant_department_id:
            se_dict["merchant_position__merchant_department_id"] = merchant_department_id

        try:
            s_obj = list(models.MerchantEmployee.objects.filter(**se_dict).values())
            size = request.GET.get("size", 20)
            pg = request.GET.get("pg", 1)
            p = Paginator(s_obj, size)
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
        TODO: 新增员工
        '''
        employee = request.employee
        
        # mobile = request.data.get("mobile", None)
        # name = request.data.get("name", None)
        # sex = request.data.get("sex", None)
        # identity_number = request.data.get("identity_number", None)
        # merchant_position_id = request.data.get("merchant_position_id", None)
        # merchant_department_id = request.data.get("merchant_department_id", None)

        args = parser.parse_args()
        try:
            with transaction.atomic():
                ep_obj = models.MerchantEmployee(
                    mobile = args.mobile,
                    name = args.name,
                    sex = args.sex,
                    identity_number = args.identity_number,
                    merchant_position_id = args.merchant_position_id,
                    merchant_id = employee.merchant_id,
                )
                ep_obj.save()
                re_data = recode.success_func(data={})
        except Exception as e:
            re_data = recode.error_func(-1,str(e))
        return JsonResponse(re_data)