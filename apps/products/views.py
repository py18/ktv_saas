from django.db import transaction
from django.http import JsonResponse
from django.utils import timezone
from rest_framework.views import APIView
from apps.db_module import models
from apps.products.products_func import get_page
from utils.code.return_code import ReCode


class SpecificationsView(APIView):
    '''创建商品的基础规格单位'''
    def post(self,request,*args,**kwargs):
        name = self.request.data.get('name',None)
        serial_number = self.request.data.get('serial_number',0)
        employee = self.request.employee
        print(employee)
        merchant_employee_id = employee.id
        merchant_id = employee.merchant_id

        assert name,(-37,'name为必传字段')

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
        employee = self.request.employee
        merchant_id = employee.merchant_id
        id = self.request.GET.get('id',None)

        size = self.request.GET.get("size", 10)
        pg = self.request.GET.get("pg", 1)

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
                re_dict['merchant_employee_id'] = x.merchant_employee.id
                re_dict['merchant_employee_name'] = x.merchant_employee.name
                re_dict['serial_number'] = x.serial_number
                re_list.append(re_dict)
            # 排序
            re_list = sorted(re_list, key=lambda e: e.__getitem__('serial_number'))

            data = get_page(re_list,size,pg)
        except Exception as w:
            return JsonResponse(ReCode().error_func(status=-1,error=str(w)))
        return JsonResponse(ReCode().success_func(data=data))

    def put(self,request,*args,**kwargs):
        employee = self.request.employee
        merchant_id = employee.merchant_id


        id = self.request.data.get('id',None)
        name = self.request.data.get('name',None)
        serial_number = self.request.data.get('serial_number',None)

        assert id is not None, (-9,'必传字段未传')

        update_dict = {'update_time':timezone.now()}
        if name:
            update_dict['name'] = name
        if serial_number:
            update_dict['serial_number'] = serial_number
        try:
            with transaction.atomic():
                models.MerchantSpecification.objects.filter(merchant_id=merchant_id,is_del=False,id=id).update(**update_dict)
        except Exception as w:
            return JsonResponse(ReCode().error_func(status=-1,error=str(w)))
        return JsonResponse(ReCode().success_func(data={}))


    def delete(self,request,*args,**kwargs):
        id = self.request.data.get('id',None)
        employee = self.request.employee
        merchant_id = employee.merchant_id
        merchant_employee_id = employee.id
        assert id,(-9,'id为必传字段')
        update_dict = {'update_time':timezone.now(),'is_del':True}
        try:
            with transaction.atomic():
                models.MerchantSpecification.objects.filter(merchant_id=merchant_id,id=id).update(**update_dict)
        except Exception as w:
            return JsonResponse(ReCode().error_func(status=-1, error=str(w)))
        return JsonResponse(ReCode().success_func(data={}))


class SpecificationValuesView(APIView):
    '''创建规格下面的规格值'''
    def post(self,request,*args,**kwargs):
        employee = self.request.employee
        merchant_id = employee.merchant_id
        merchant_employee_id = employee.id
        specification_id = self.request.data.get('specification_id')
        name = self.request.data.get('name') #name封装为[]
        #格式为[{'name':'冷','serial_number':0},{'name':'热','serial_number':1}]
        assert specification_id,(-39,'specification_id为必传字段')
        assert name,(-32,'name为必传字段')
        try:
            with transaction.atomic():
                for x in name:
                    serial_number=x.get('serial_number',0)
                    values_obj = models.MerchantSpecificationValues.objects.filter(specification_id=specification_id,merchant_id=merchant_id,name=x['name'],is_del=False)
                    if len(values_obj) != 0:
                        return JsonResponse(ReCode().error_func(status=-1,error=str(x['name']+'已存在')))

                    specification_value = models.MerchantSpecificationValues(
                        specification_id=specification_id,
                        name=x['name'],
                        merchant_employee_id=merchant_employee_id,
                        merchant_id=merchant_id,
                        serial_number=serial_number
                    )
                    specification_value.save()
        except Exception as w:
            return JsonResponse(ReCode().error_func(status=-1,error=str(w)))
        return JsonResponse(ReCode().success_func(data={}))

    def get(self,request,*args,**kwargs):
        specification_id = self.request.GET.get('specification_id')
        employee = self.request.employee
        merchant_id = employee.merchant_id
        assert specification_id,(-39,'specification_id为必传字段')
        obj_set = models.MerchantSpecificationValues.objects.filter(specification_id=specification_id,is_del=False,merchant_id=merchant_id)
        re_list = []
        for x in obj_set:
            re_dict = {}
            re_dict['id'] = x.id
            re_dict['name'] = x.name
            re_dict['merchant_employee_id'] = x.merchant_employee_id
            re_dict['merchant_employee_name'] = x.merchant_employee.name
            re_dict['serial_number'] = x.serial_number
            re_list.append(re_dict)
        re_list = sorted(re_list, key=lambda e: e.__getitem__('serial_number'))
        return JsonResponse(ReCode().success_func(data={'count':len(re_list),'ret':re_list}))
    def delete(self,request,*args,**kwargs):
        id = self.request.data.get('id')
        try:
            with transaction.atomic():
                models.MerchantSpecificationValues.objects.filter(id=id,is_del=False).update(is_del=True)
        except Exception as w:
            return JsonResponse(ReCode().error_func(status=-1,error=str(w)))
        return JsonResponse(ReCode().success_func(data={}))
    def put(self,request,*args,**kwargs):
        id = self.request.data.get('id')
        name = self.request.data.get('name',None)
        serial_number = self.request.data.get('serial_number',None)
        assert id,(-9,'id为必传字段')
        update_dict = {}
        if name:
            update_dict['name'] = name
        if serial_number:
            update_dict['serial_number'] = serial_number
        try:
            with transaction.atomic():
                models.MerchantSpecificationValues.objects.filter(id=id).update(**update_dict)
        except Exception as w:
            return JsonResponse(ReCode().error_func(status=-1,error=str(w)))
        return JsonResponse(ReCode().success_func(data={}))


class MerchantProductTypeView(APIView):
    '''商家商品分类信息表'''
    def post(self,request,*args,**kwargs):

        employee = self.request.employee
        merchant_id = employee.merchant_id
        merchant_employee_id = employee.id
        name = self.request.data.get('name')
        father_type_id = self.request.data.get('father_type_id',None)
        serial_number = self.request.data.get('serial_number',0)

        assert name,(-32,'商品分类名为必传字段')
        try:
            with transaction.atomic():
                product_type = models.MerchantProductType(
                    name=name,
                    father_type_id=father_type_id,
                    merchant_employee_id=merchant_employee_id,
                    merchant_id=merchant_id,
                    serial_number=serial_number
                )
                product_type.save()
        except Exception as w:
            return JsonResponse(ReCode().error_func(status=-1,error=str(w)))
        return JsonResponse(ReCode().success_func(data={}))

    def get(self,request,*args,**kwargs):

        id = self.request.GET.get('id') #有id查询单个类别
        father_type_id = self.request.GET.get('father_type_id') #有father_type_id查询该分类下的所有子分类_

        size = self.request.GET.get('size',100)
        pg = self.request.GET.get('pg',1)

        employee = self.request.employee
        merchant_id = employee.merchant_id

        try:
            if id:
                obj_set = models.MerchantProductType.objects.filter(is_del=False,id=id,merchant_id=merchant_id)
            elif father_type_id:
                obj_set = models.MerchantProductType.objects.filter(is_del=False,father_type_id=father_type_id,merchant_id=merchant_id)
            else:
                obj_set = models.MerchantProductType.objects.filter(is_del=False,merchant_id=merchant_id)
            re_list = []
            # print(obj_set)
            for x in obj_set:
                re_dict = {}
                re_dict['id'] = x.id
                re_dict['name'] = x.name
                re_dict['father_type_id'] = x.father_type_id
                if re_dict['father_type_id'] is None:
                    re_dict['father_type_name'] = None
                else:
                    re_dict['father_type_name'] = x.father_type.name
                re_dict['merchant_employee_id'] = x.merchant_employee_id
                re_dict['merchant_employee_name'] = x.merchant_employee.name
                re_dict['serial_number'] = x.serial_number
                re_list.append(re_dict)
            data = sorted(re_list, key=lambda e: e.__getitem__('serial_number'))
            re_list = get_page(data,size,pg)
        except Exception as w:
            return JsonResponse(ReCode().error_func(status=-1,error=str(w)))
        return JsonResponse(ReCode().success_func(data=re_list))

    def put(self,request,*args,**kwargs):
        id = self.request.data.get('id')
        name = self.request.data.get('name')
        father_type_id = self.request.data.get('father_type_id')
        serial_number = self.request.data.get('serial_number',0)
        assert id ,(-9,'关键参数，id未传')
        updata_dict = {"father_type_id":father_type_id}
        if name:
            updata_dict['name'] = name
        if father_type_id:
            updata_dict['father_type_id'] = father_type_id
        if serial_number:
            updata_dict['serial_number'] = serial_number
        try:
            with transaction.atomic():
                models.MerchantProductType.objects.filter(id=id).update(**updata_dict)
        except Exception as w:
            return JsonResponse(ReCode().error_func(status=-1,error=str(w)))
        return JsonResponse(ReCode().success_func(data={}))

    def delete(self,request,*args,**kwargs):
        id = self.request.data.get('id')
        assert id,(-9,'关键参数，id未传')
        try:
            with transaction.atomic():
                obj = models.MerchantProductType.objects.get(id=id)
                child_set = models.MerchantProductType.objects.filter(father_type=obj)
                if len(child_set) != 0:
                    return JsonResponse(ReCode().error_func(status=-1, error='请先删除该分类下的所有子类'))
                else:
                    models.MerchantProductType.objects.filter(id=id).update(is_del=True)
        except Exception as w:
            return JsonResponse(ReCode().error_func(status=-1, error=str(w)))
        return JsonResponse(ReCode().success_func(data={}))


class MerchantProductView(APIView):
    '''创建商品spu表'''
    def post(self,request,*args,**kwargs):
        employee = self.request.employee
        merchant_id = employee.merchant_id
        merchant_employee_id = employee.id

        name = self.request.data.get('name')
        images = self.request.data.get('images')
        product_type_id = self.request.data.get('product_type_id')
        serial_number = self.request.data.get('serial_number',0)

        assert name ,(-33,'商品spu名字为必传字段')
        assert images ,(-34,'商品spu图片为必传字段')
        assert product_type_id ,(-35,'商品spu分类id为必传字段')

        try:
            with transaction.atomic():
                product_spu = models.MerchantProduct(
                    name=name,
                    images=images,
                    product_type_id=product_type_id,
                    merchant_employee_id=merchant_employee_id,
                    merchant_id=merchant_id,
                    serial_number=serial_number
                )
                product_spu.save()
        except Exception as w:
            return JsonResponse (ReCode().error_func(status=-1,error=str(w)))
        return JsonResponse(ReCode().success_func(data={}))


    def get(self,request,*args,**kwargs):
        id = self.request.GET.get('id',None)
        product_type_id = self.request.GET.get('product_type_id')

        size = self.request.GET.get('size',100)
        pg = self.request.GET.get('pg',1)

        employee = self.request.employee
        merchant_id = employee.merchant_id
        merchant_employee_id = employee.id
        try:
            if id:
                obj_set = models.MerchantProduct.objects.filter(id=id,merchant_id=merchant_id)
            elif product_type_id:
                obj_set = models.MerchantProduct.objects.filter(product_type_id=product_type_id,is_del=False,merchant_id=merchant_id)
            else:
                obj_set = models.MerchantProduct.objects.filter(is_del=False,merchant_id=merchant_id)
            re_list = []
            for x in obj_set:
                re_dict = {}
                re_dict['id'] = x.id
                re_dict['name'] = x.name
                re_dict['images'] = x.images
                re_dict['product_type_id'] = x.product_type_id
                re_dict['product_type_name'] = x.product_type.name
                re_dict['merchant_employee_id'] = x.merchant_employee_id
                re_dict['merchant_employee_name'] = x.merchant_employee.name
                re_dict['serial_number'] = x.serial_number
                re_list.append(re_dict)
            data = sorted(re_list, key=lambda e: e.__getitem__('serial_number'))
            re_info = get_page(data,size,pg)
        except Exception as w:
            return JsonResponse(ReCode().error_func(status=-1,error=str(w)))
        return JsonResponse(ReCode().success_func(re_info))
    def put(self,request,*args,**kwargs):
        employee = self.request.employee
        merchant_id = employee.merchant_id
        merchant_employee_id = employee.id

        id = self.request.data.get('id')
        name = self.request.data.get('name')
        product_type_id = self.request.data.get('product_type_id')
        images = self.request.data.get('images')
        serial_number = self.request.data.get('serial_number')

        assert id,(-9,'必传参数未传')

        update_dict = {}
        if name:
            update_dict['name'] = name
        if images:
            update_dict['images'] = images
        if product_type_id:
            update_dict['product_type_id'] = product_type_id
        if serial_number:
            update_dict['serial_number'] = serial_number
        try:
            with transaction.atomic():
                models.MerchantProduct.objects.filter(id=id,is_del=False,merchant_id=merchant_id).update(**update_dict)
        except Exception as w:
            return JsonResponse(ReCode().error_func(status=-1,error=str(w)))
        return JsonResponse(ReCode().success_func(data={}))

    def delete(self,request,*args,**kwargs):
        id = self.request.data.get('id')
        employee = self.request.employee
        merchant_id = employee.merchant_id
        assert id,(-9,'必传字段未传')
        try:
            with transaction.atomic():
                models.MerchantProduct.objects.filter(id=id).update(is_del=True)
        except Exception as w:
            return JsonResponse(ReCode().error_func(status=-1,error=str(w)))
        return JsonResponse(ReCode().success_func(data={}))


class MerchantProductSpecsView(APIView):
    '''创建商品sku的视图，是商品的最后一层'''
    def post(self,request,*args,**kwargs):
        employee = self.request.employee
        merchant_id = employee.merchant_id
        merchant_employee_id = employee.id

        product_id = self.request.data.get('product_id') #商品id
        specification_values = self.request.data.get('specification_values') #属性值list，里面存放属性值id
        product_type = self.request.data.get('product_type') #是套餐还是商品
        price = self.request.data.get('price') #单价
        unit_id = self.request.data.get('unit_id') #单位id
        image = self.request.data.get('image') #图片地址
        introduction = self.request.data.get('introduction') #简介
        body = self.request.data.get('body') #文本
        is_low = self.request.data.get('is_low') #是否低消
        is_commission = self.request.data.get('is_commission') #是否提成
        is_discount = self.request.data.get('is_discount') #是否折扣
        merchant_print_position_id = self.request.data.get('merchant_print_position_id') #打印到某台打印机
        is_calculation = self.request.data.get('is_calculation') #参与库存计算
        is_raw_material = self.request.data.get('is_raw_material') #原料
        is_accessories = self.request.data.get('is_accessories') #是否有配品
        publish_status = self.request.data.get('publish_status') #是否上架
        serial_number = self.request.data.get('serial_number',0) #排序序列号

        assert product_id, (-50,'重要参数未传（{}）'.format('product_id'))
        assert specification_values, (-51,'重要参数未传（{}）'.format('specification_values'))
        assert product_type, (-52,'重要参数未传（{}）'.format('product_type'))
        assert price, (-53,'重要参数未传（{}）'.format('price'))
        assert unit_id, (-54,'重要参数未传（{}）'.format('unit_id'))
        assert image, (-55,'重要参数未传（{}）'.format('image'))
        assert introduction, (-56,'重要参数未传（{}）'.format('introduction'))
        assert body, (-57,'重要参数未传（{}）'.format('body'))
        assert is_low, (-58,'重要参数未传（{}）'.format('is_low'))
        assert is_commission, (-59,'重要参数未传（{}）'.format('is_commission'))
        assert is_discount, (-301,'重要参数未传（{}）'.format('is_discount'))
        assert merchant_print_position_id, (-302,'重要参数未传（{}）'.format('merchant_print_position_id'))
        assert is_calculation, (-303,'重要参数未传（{}）'.format('is_calculation'))
        assert is_raw_material, (-304,'重要参数未传（{}）'.format('is_raw_material'))
        assert is_accessories, (-305,'重要参数未传（{}）'.format('is_accessories'))
        assert publish_status, (-306,'重要参数未传（{}）'.format('publish_status'))

        try:
            with transaction.atomic():
                product_sku = models.MerchantProductSpecs(
                    product_id = product_id,
                    specification_values=specification_values,
                    product_type=product_type,
                    price=price,
                    unit_id=unit_id,
                    image=image,
                    introduction=introduction,
                    body=body,
                    is_low=is_low,
                    is_commission=is_commission,
                    is_discount=is_discount,
                    merchant_print_position_id=merchant_print_position_id,
                    is_calculation=is_calculation,
                    is_raw_material=is_raw_material,
                    is_accessories=is_accessories,
                    publish_status=publish_status,
                    merchant_employee_id=merchant_employee_id,
                    merchant_id=merchant_id,
                    serial_number=serial_number,
                )
                product_sku.save()
        except Exception as w:
            return JsonResponse(ReCode().error_func(status=-1,error=str(w)))
        return JsonResponse(ReCode().success_func(data={}))

    def get(self,request,*args,**kwargs):
        pass
    def put(self,request,*args,**kwargs):
        pass
    def delete(self,request,*args,**kwargs):
        id = self.request.data.get('id')
        employee = self.request.employee
        merchant_id = employee.merchant_id
        merchant_employee_id = employee.id
        assert id,(-9,'重要参数未传')
        try:
            with transaction.atomic():
                models.MerchantProductSpecs.objects.filter(id=id,merchant_id=merchant_id).update(is_del=True)
        except Exception as w:
            return JsonResponse(ReCode().error_func(status=-1,error=str(w)))
        return JsonResponse(ReCode().success_func(data={}))