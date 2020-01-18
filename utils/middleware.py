from django.http import JsonResponse, HttpResponse
from django.utils.deprecation import MiddlewareMixin
import json
import jwt

from utils.code.return_code import ReCode
from utils.config import ini
from apps.db_module import models

recode = ReCode()


class BlockedIpMiddleware(MiddlewareMixin):

    def process_request(self, request):
        if request.path_info == "/api/v1/merchant_file/login/" or request.path_info == "/api/v1/merchant_file/register/":
            return None
        try:
            jwt_token = request.META.get('HTTP_AUTHORIZATION')
            token = jwt.decode(jwt_token, ini.SecretCode, algorithm='HS256')
            user = models.MerchantEmployee.objects.get(id=token["id"])
            request.employee = user

        except Exception as e:
            re_data = recode.error_func(-2, "请登录:" + str(e))
            return JsonResponse(re_data)

    # def process_view(self, request, callback, callback_args, callback_kwargs):
    #     """
    #     如果有返回值，则不在继续执行，直接到最后一个中间件的response
    #     """

    def process_exception(self, request, exception):
        if str(exception) is None:
            return None
        else:
            try:
                if type(eval(str(exception))) == tuple:
                    aex = str(exception)[1:-1]
                    alist = aex.split(',')
                    re_data = recode.error_func(alist[0], alist[1])
                    return JsonResponse(re_data)

                else:
                    if str(exception) == '-101':
                        return JsonResponse({"code": -101, "message": "必填参数未填"})
                    else:
                        return None
            except Exception as e:
                print(e)
                return None

    def process_response(self, request, response):
        # print("中间件2返回：",json.loads(response.content))
        # print(request.user.u_id)
        # print(type(response),'---------------------')
        return response