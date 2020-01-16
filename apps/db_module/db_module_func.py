# from operator import itemgetter

# from django.core.paginator import Paginator
# from django.db import transaction
# from db_module import models
# from utils.get_number import get_unique_num
# import time

# def get_timestamp():
#     return time.strftime('%Y-%m-%d %H:%M:%S')

# def create_merchant(data):
#     mer_name = data['mer_name']
#     cliaddress = data['cliaddress']
#     cliarea = data['cliarea']
#     introduction = data['introduction']
#     logo = data['logo']
#     father_mer_id = data['father_mer_id'] if data['father_mer_id'] else None
#     serial_number = data['serial_number'] if data['serial_number'] else 0
#     mer_no = get_unique_num()
#     try:
#         with transaction.atomic():
#             merchant = models.Merchant(
#                 mer_no=mer_no,
#                 mer_name=mer_name,
#                 cliaddress=cliaddress,
#                 cliarea=cliarea,
#                 introduction=introduction,
#                 logo=logo,
#                 father_mer_id=father_mer_id,
#                 serial_number=serial_number
#             )
#             merchant.save()
#     except Exception as w:
#         raise w
#     return 'ok'


# def pg_fun(info,size,pg):

#     p = Paginator(info, size)
#     next_page = None
#     previous_page = None
#     page1 = p.page(pg)
#     if page1.has_next():
#         next_page = page1.next_page_number()
#     if page1.has_previous():
#         previous_page = page1.previous_page_number()
#     data = {"result":"ok","count": p.count, "num_pages": p.num_pages, "next_page": next_page, "previous_page": previous_page,
#             "ret": page1.object_list}
#     return data


# def re_ok_func(data):
#     re_dict = {}
#     re_dict['status'] = 1
#     re_dict['data'] = data
#     re_dict['message'] = '成功'
#     re_dict['timestamp'] = get_timestamp()
#     return re_dict

# def re_no_func(w):
#     re_dict = {}
#     re_dict['status'] = -1
#     re_dict['error'] = str(w)
#     re_dict['message'] = '失败'
#     re_dict['timestamp'] = get_timestamp()
#     return re_dict


# def get_merchant(id):
#     try:
#         if id:
#             obj_set = models.Merchant.objects.filter(is_del=False, id=id).order_by('create_time')
#         else:
#             obj_set = models.Merchant.objects.filter(is_del=False)
#         if len(obj_set)==0:
#             raise Exception ('无此查询内容')
#         else:
#             re_list = []
#             for x in obj_set:
#                 re_dict = {}
#                 re_dict['id'] = x.id
#                 re_dict['mer_no'] = x.mer_no
#                 re_dict['mer_name'] = x.mer_name
#                 re_dict['cliaddress'] = x.cliaddress
#                 re_dict['cliarea'] = x.cliarea
#                 re_dict['introduction'] = x.introduction
#                 re_dict['logo'] = x.logo
#                 re_dict['father_mer_id'] = x.father_mer_id
#                 re_dict['serial_number'] = x.serial_number
#                 re_list.append(re_dict)
#     except Exception as w:
#         raise w
#     return re_list
