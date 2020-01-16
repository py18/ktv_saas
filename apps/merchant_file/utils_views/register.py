from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from django.db import transaction

from rest_framework.views import APIView

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

class RegistView(APIView):

    def post(self, request, *args, **kwargs):
        '''
            TODO: 商家注册
            test_json post: {"mer_no":"115465545445554,"mer_name":"测试公司,"cliarea":"四川成都","cliaddress":"天府三街","mobile":"13412561234","password":"a123456"}
        '''
        
        mer_name = request.data.get("mer_name", None)
        cliarea = request.data.get("cliarea", None)
        cliaddress = request.data.get("cliaddress", None)
        mobile = request.data.get("mobile", None)
        password = request.data.get("password", None)

        print(mer_name)

        assert mer_name,(-14,"未填公司名")
        assert mobile,(-11,"手机号未填")
        assert password,(-12,"密码未填")

        try:
            with transaction.atomic():
                mer = models.Merchant(mer_no = str(10000 + int(redis_cli.cache.incr('Regiester1'))), mer_name = mer_name, cliarea = cliarea, cliaddress = cliaddress)
                mer.save()
                mer_dep = models.MerchantDepartment(name="初始创建部",merchant=mer)
                mer_dep.save()
                mer_pos = models.MerchantPosition(name="初始创建者", merchant=mer, merchant_department=mer_dep)
                mer_pos.save()
                mer_emp = models.MerchantEmployee(name="管理员",mobile=mobile,merchant=mer,merchant_position=mer_pos,is_edit=True,password=generate_password_hash(password))
                mer_emp.save()
                data = {}
                re_data = recode.success_func(data)
        except Exception as e:
            re_data = recode.error_func(-1,str(e))
        return JsonResponse(re_data)