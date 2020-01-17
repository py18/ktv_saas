'''
    TODO: 子店信息管理
    功能：
    字段：门店名称，地址，街道地址，logo
'''

from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.db import transaction

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

        try:
            childs = models.Merchant.objects.get(id=user.merchant_id).ship.all().values()
            print(childs)

        except Exception as e:
            print(e)
        return JsonResponse({"code":1})