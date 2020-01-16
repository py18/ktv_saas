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


class LoginView(APIView):

    def post(self,request,*args,**kwargs):
        '''
            TODO: 登录
        '''
        mobile = request.data.get('mobile', None)
        password = request.data.get('password', None)

        assert mobile,(-11,"手机号必填")
        assert password,(-12,"密码必填")

        try:

            inval_password = check_password_hash(user.password, password) is False: