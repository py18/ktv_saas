from django.shortcuts import render
from django.http import JsonResponse,HttpResponse

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

recode = ReCode()


class LoginView(APIView):

    def post(self,request,*args,**kwargs):
        '''
            TODO: 登录
            test_json post: {"mobile":"13412561232","password":"a123456"}
        '''
        mobile = request.data.get('mobile', None)
        password = request.data.get('password', None)

        assert mobile,(-11,"手机号必填")
        assert password,(-12,"密码必填")

        try:
            user = models.MerchantEmployee.objects.get(mobile=mobile)
            inval_password = check_password_hash(user.password, password)
            assert inval_password == True,(-13,"密码错误")
            # 返回所有menu_list
            # 返回公司名称,id,logo  user_name
            # 生成token
            token_data = {
                    'mobile':user.mobile,
                    'id':user.id,
                    'exp':datetime.datetime.now() + datetime.timedelta(days=ini.ExpireDate)
                }
            token = jwt.encode(token_data, ini.SecretCode, algorithm='HS256')
            data = {}
            data["user_name"] = user.name
            data["merchant_name"] = user.merchant.mer_name
            data["merchant_id"] = user.merchant_id
            data["merchant_logo"] = user.merchant.logo
            data["token"] = token.decode('utf8')
            data["menu_list"] = []
            re_data = recode.success_func(data)
        except Exception as e:
            re_data = recode.error_func(-1,str(e))
        return JsonResponse(re_data)