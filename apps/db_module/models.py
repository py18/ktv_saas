from django.db import models

# Create your models here.

from django.db import models
import ast

from werkzeug.security import generate_password_hash, check_password_hash

# 自定义一个ListFiled,继承与TextField这个类
class ListFiled(models.TextField):
    description = "just a listfiled"

    # 继承TextField
    def __init__(self, *args, **kwargs):
        super(ListFiled, self).__init__(*args, **kwargs)
    # 读取数据库的时候调用这个方法
    def from_db_value(self, value, expression, conn, context):
        # print('from_db_value')
        if not value:
            value = []
        if isinstance(value, list):

            return value
        # print('value type ', type(value))
        # 直接将字符串转换成python内置的list
        return ast.literal_eval(value)

    # 保存数据库的时候调用这个方法
    def get_prep_value(self, value):
        # print("get_prep_value")
        if not value:
            return value
        # print('value type ', type(value))
        return str(value)


class DefModels(models.Model):

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    is_del = models.BooleanField(default=False)
    serial_number = models.IntegerField(default=0, verbose_name="序号")

    class Meta:
        abstract = True

class DefRecordModel(models.Model):

    create_time = models.DateTimeField(auto_now_add=True)
    create_user_id = models.IntegerField(default=0)
    update_time = models.DateTimeField(auto_now=True)
    last_update_user_id = models.IntegerField(default=0)
    is_del = models.BooleanField(default=False)

    class Meta:
        abstract = True

class Application(DefModels):

    name = models.CharField(max_length=255, verbose_name="应用名")
    introduction = models.TextField(default='', verbose_name="应用简介")
    rep_url = models.CharField(max_length=255, verbose_name="应用url")

    class Meta:
        db_table = 'application'
        managed = True
        verbose_name = '应用表'

class ApplocationMenu(DefModels):

    application = models.ForeignKey("Application", on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=255, verbose_name="功能菜单名")

    class Meta:
        db_table = 'application_menu'
        managed = True
        verbose_name = 'app菜单表'

class ApplocationMenuFunc(DefModels):

    application_menu = models.ForeignKey("ApplocationMenu", on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=255, verbose_name="功能菜单方法名")
    request_path = models.CharField(max_length=255, verbose_name="功能方法请求地址")
    request_method = models.CharField(max_length=16, verbose_name="功能方法请求方式")

    class Meta:
        db_table = 'application_menu_func'
        managed = True
        verbose_name = 'app菜单方法表'
        


class Merchant(DefModels):

    mer_no = models.CharField(max_length=64, verbose_name="商家编号")
    mer_name = models.CharField(max_length=1024, verbose_name="商家名称")
    cliaddress = models.CharField(max_length=255, verbose_name="商家街道地址")
    cliarea = models.CharField(max_length=255, verbose_name="商家所在地区")
    introduction = models.TextField(default='', verbose_name="商家简介")
    logo = models.CharField(max_length=64, verbose_name="商家logo")
    
    contact_person = models.CharField(max_length=255, verbose_name="联系人", default="")
    contact_mobile = models.CharField(max_length=12, verbose_name="联系电话", default='')

    father_mer = models.ForeignKey(to='self', null=True, on_delete = models.DO_NOTHING, verbose_name="父级")

    class Meta:

        db_table = 'merchant'
        managed = True
        verbose_name = '商家基础表'

class MerchantDefModels(models.Model):
    merchant = models.ForeignKey("Merchant", on_delete=models.DO_NOTHING, verbose_name="商家外键")
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    is_del = models.BooleanField(default=False)
    serial_number = models.IntegerField(default=0, verbose_name="序号")

    class Meta:
        abstract = True



class MerchantApplication(MerchantDefModels):

    application = models.ForeignKey("Application", on_delete=models.DO_NOTHING, verbose_name="应用外键")

    class Meta:
        db_table = 'merchant_application'
        managed = True
        # unique_together = ('merchant', 'application',)
        verbose_name = '商家应用表'

class MerchantDepartment(MerchantDefModels):

    name = models.CharField(max_length=255, verbose_name="部门名称")
    remark = models.CharField(max_length=2000, verbose_name="备注")

    class Meta:
        db_table = 'merchant_department'
        managed = True
        verbose_name = '商家部门表'

class MerchantPosition(MerchantDefModels):

    name = models.CharField(max_length=255, verbose_name="职位名称")
    merchant_department = models.ForeignKey("MerchantDepartment", on_delete=models.DO_NOTHING, verbose_name="部门外键")
    is_leader = models.BooleanField(default=False, verbose_name="是否部门领导")
    remark = models.CharField(max_length=2000, verbose_name="备注")
    # 默认推卡提成百分比
    # 默认订单提成百分比
    class Meta:
        db_table = 'merchant_position'
        managed = True
        verbose_name = '职位表'

class MerchantEmployee(MerchantDefModels):

    mobile = models.CharField(max_length=11, unique=True, verbose_name="手机号")
    name = models.CharField(max_length=255, verbose_name="姓名")
    sex_choice = ((1,"男"),(2,"女"),(3,"保密"))
    sex = models.SmallIntegerField(choices=sex_choice, default=3, verbose_name="性别")
    identity_number = models.CharField(max_length=18, default='', verbose_name="身份证号")

    merchant_position = models.ForeignKey("MerchantPosition", on_delete=models.DO_NOTHING, verbose_name="职位")
    password = models.CharField(max_length=255, verbose_name="密码", default=generate_password_hash("123456"))
    # 负责人
    is_edit = models.BooleanField(default=False, verbose_name="是否负责人")

    class Meta:
        db_table = 'merchant_employee'
        managed = True
        verbose_name = '商家员工表'
        

class MerchantEmployeePermissions(MerchantDefModels):

    merchant_employee = models.ForeignKey("MerchantEmployee", on_delete=models.DO_NOTHING, verbose_name="商家员工外键")
    # 商家应用
    merchant_application = models.ForeignKey("MerchantApplication", on_delete=models.DO_NOTHING, verbose_name="商家应用外键")
    # 权限
    permissions_list = ListFiled(default="")

    class Meta:
        db_table = 'merchant_employee_permissions'
        managed = True
        verbose_name = '商家员工权限表'

class MerchantUnit(MerchantDefModels):

    name = models.CharField(max_length=255, verbose_name="单位名称")

    class Meta:
        db_table = 'merchant_unit'
        managed = True
        verbose_name = '商家单位表'

class MerchantProductType(MerchantDefModels):

    name = models.CharField(max_length=255, verbose_name="分类名称")
    father_type = models.ForeignKey(to='self', null=True, on_delete = models.DO_NOTHING, verbose_name="父级分类")
    merchant_employee = models.ForeignKey("MerchantEmployee", on_delete=models.DO_NOTHING) # 操作人

    class Meta:
        db_table = 'merchant_product_type'
        managed = True
        verbose_name = '商家商品分类表'

class MerchantProduct(MerchantDefModels): # 商品SPU

    name = models.CharField(max_length=255, verbose_name="商品名称")
    images = models.CharField(max_length=255, verbose_name="封面图片")
    product_type = models.ForeignKey("MerchantProductType", models.DO_NOTHING, verbose_name="商品类型")
    merchant_employee = models.ForeignKey("MerchantEmployee", on_delete=models.DO_NOTHING) # 操作人

    class Meta:
        db_table = 'merchant_product'
        managed = True
        verbose_name = '商家商品表（SPU）'

class MerchantSpecification(MerchantDefModels):

    name = models.CharField(max_length=255, verbose_name="规格名称")
    merchant_employee = models.ForeignKey("MerchantEmployee", on_delete=models.DO_NOTHING) # 操作人

    class Meta:
        db_table = 'merchant_specification'
        managed = True
        verbose_name = '商家规格表'


class MerchantSpecificationValues(MerchantDefModels):

    specification = models.ForeignKey("MerchantSpecification", on_delete=models.DO_NOTHING, verbose_name="规格外键")
    name = models.CharField(max_length=255, verbose_name="规格值名称")
    merchant_employee = models.ForeignKey("MerchantEmployee", on_delete=models.DO_NOTHING) # 操作人

    class Meta:
        db_table = 'merchant_specification_values'
        managed = True
        verbose_name = '商家规格值表'


# 店铺分区
class MerchantZoneDivision(MerchantDefModels):

    name = models.CharField(max_length=255, verbose_name="店铺位置名称")
    zone_type_choice = ((1,"客区"),(2,"私区"),(3,"公共区域"))
    zone_type = models.SmallIntegerField(choices=zone_type_choice, default=1)
    merchant_employee = models.ForeignKey("MerchantEmployee", on_delete=models.DO_NOTHING) # 操作人

    class Meta:
        db_table = 'merchant_zone_division'
        managed = True
        verbose_name = '商家店铺分区'

# 客坐形式 （包间、散座、卡座）
class MerchantGuestSittingForm(MerchantDefModels):

    name = models.CharField(max_length=255, verbose_name="客座形式名")
    merchant_employee = models.ForeignKey("MerchantEmployee", on_delete=models.DO_NOTHING) # 操作人

    class Meta:
        db_table = 'merchant_guest_sitting_form'
        managed = True
        verbose_name = '商家客坐形式表'

class MerchantGuestSittingFormType(MerchantDefModels):

    name = models.CharField(max_length=255, verbose_name="类型名")
    guest = models.ForeignKey("MerchantGuestSittingForm", on_delete=models.DO_NOTHING, verbose_name="客坐形式外键")
    merchant_employee = models.ForeignKey("MerchantEmployee", on_delete=models.DO_NOTHING) # 操作人

    class Meta:
        db_table = 'merchant_guest_sitting_form_type'
        managed = True
        verbose_name = '商家客坐形式类型表'

class MerchantGuestSitting(MerchantDefModels):

    name = models.CharField(max_length=255, verbose_name="客座名称")
    guest_sitting_form_type = models.ForeignKey("MerchantGuestSittingFormType", on_delete=models.DO_NOTHING)
    merchant_zone_division = models.ForeignKey("MerchantZoneDivision", on_delete=models.DO_NOTHING)
    # 面积
    area = models.DecimalField(max_digits=3, decimal_places=2, default=0, verbose_name="面积")
    # 适用人数
    people_num = models.IntegerField(default=1, verbose_name="适用人数")
    # 默认计费规则
    # 照片
    images = ListFiled(default='', verbose_name="图片集")
    # 视频
    video = models.CharField(max_length=255, verbose_name="视频", default="")
    # 是否加入低消
    is_low = models.BooleanField(default=False, verbose_name="是否参与低消")
    merchant_employee = models.ForeignKey("MerchantEmployee", on_delete=models.DO_NOTHING) # 操作人

    class Meta:
        db_table = 'merchant_guest_sitting'
        managed = True
        verbose_name = '商家客坐表'

# 打印机设置
class MerchantPrinterSettings(MerchantDefModels):

    name = models.CharField(max_length=255, verbose_name="打印机名称")
    merchant_zone_division = models.ForeignKey("MerchantZoneDivision", on_delete=models.DO_NOTHING, verbose_name="打印机放置外键")
    ip_url = models.CharField(max_length=255,verbose_name="请求地址")
    login_user = models.CharField(max_length=255,verbose_name="登录管理后台的账号名")
    login_key = models.CharField(max_length=255,verbose_name="注册账号后生成的UKEY")
    printer_number = models.CharField(max_length=255,verbose_name="打印机编号")
    is_default = models.BooleanField(default=False, verbose_name="是否为默认")
    merchant_employee = models.ForeignKey("MerchantEmployee", on_delete=models.DO_NOTHING) # 操作人

    class Meta:
        db_table = 'merchant_printer_settings'
        managed = True
        verbose_name = '商家打印机设置'

# 原料表
class MerchantRawMaterial(MerchantDefModels):

    name = models.CharField(max_length=255, verbose_name="原料名称")
    unit = models.ForeignKey("MerchantUnit", on_delete=models.DO_NOTHING, verbose_name="单位外键")
    merchant_employee = models.ForeignKey("MerchantEmployee", on_delete=models.DO_NOTHING) # 操作人

    class Meta:
        db_table = 'merchant_raw_material'
        managed = True
        verbose_name = '商家原料表'

class MerchantProductSpecs(MerchantDefModels): # 商品SKU

    product = models.ForeignKey("MerchantProduct", on_delete=models.DO_NOTHING, verbose_name="商品外键")
    specification_values = ListFiled() #混合规格值的id

    product_type_choice = ((1,"普通商品"),(2,"套餐商品"))
    product_type = models.SmallIntegerField(choices=product_type_choice, default=1)

    # 售价
    price = models.BigIntegerField(default=0, verbose_name="售价")
    unit = models.ForeignKey("MerchantUnit", on_delete=models.DO_NOTHING, verbose_name="单位外键")
    # 销售总数量

    # 图片
    image = models.CharField(max_length=255, verbose_name="图片地址")
    # 简介
    introduction = models.CharField(max_length=2000, verbose_name="简介")
    # 文本
    body = models.TextField(default='', verbose_name="文本")

    # 是否低消
    is_low = models.BooleanField(default=False, verbose_name="是否参与抵消")
    # 是否提成
    is_commission = models.BooleanField(default=False, verbose_name="是否提成")
    # 是否折扣
    is_discount = models.BooleanField(default=False, verbose_name="是否折扣")
    # 打印到某台打印机
    merchant_print_position = models.ForeignKey("MerchantPrinterSettings", on_delete=models.DO_NOTHING, verbose_name="打印到某台打印机", blank=True, null=True) # 当未设置时不打印

    # 是否参与库存计算
    is_calculation = models.BooleanField(default=False, verbose_name="是否参与库存计算")
    # 原料
    is_raw_material = models.BooleanField(default=False, verbose_name="是否有原料")
    # 配品
    is_accessories = models.BooleanField(default=False, verbose_name="是否有配品")
    # 是否上架
    publish_status = models.BooleanField(default=0, verbose_name="上架状态")
    merchant_employee = models.ForeignKey("MerchantEmployee", on_delete=models.DO_NOTHING) # 操作人

    class Meta:
        db_table = 'merchant_product_specs'
        managed = True
        verbose_name = '商家商品SPU表'

class MerchantProductRawMaterial(MerchantDefModels):

    product_sku = models.ForeignKey("MerchantProductSpecs", on_delete=models.DO_NOTHING, verbose_name="商品SPU外键")
    raw_material = models.ForeignKey("MerchantRawMaterial", on_delete=models.DO_NOTHING, verbose_name="原料外键")
    quantity = models.IntegerField(default=0, verbose_name="数量")
    merchant_employee = models.ForeignKey("MerchantEmployee", on_delete=models.DO_NOTHING) # 操作人

    class Meta:
        db_table = 'merchant_product_raw_material'
        managed = True
        verbose_name = '商家商品原料详情表'

class MerchantAccessoriesDetails(MerchantDefModels):

    # Product_spu_id = models.IntegerField()
    product_s = models.ForeignKey("MerchantProductSpecs", on_delete=models.DO_NOTHING, verbose_name="商品SPU外键1", related_name='bProduct_spu')
    accessories = models.ForeignKey("MerchantProductSpecs", on_delete=models.DO_NOTHING, verbose_name="商品SPU外键2", related_name='acProduct_spu')
    quantity = models.IntegerField(default=0, verbose_name="数量")
    merchant_employee = models.ForeignKey("MerchantEmployee", on_delete=models.DO_NOTHING) # 操作人

    class Meta:
        db_table = 'merchant_accessories_details'
        managed = True
        verbose_name = '商家商品配品详情表'

# 原料库存
class MerchantRawMaterialStock(MerchantDefModels):

    # 原料外键（一对一）
    merchant_raw_material = models.OneToOneField("MerchantRawMaterial", on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(default=0, verbose_name="库存数量")
    number_alerts = models.IntegerField(default=0, verbose_name="警报数量")
    merchant_employee = models.ForeignKey("MerchantEmployee", on_delete=models.DO_NOTHING) # 操作人

    class Meta:
        db_table = 'merchant_raw_material_stock'
        managed = True
        verbose_name = '商家原料库存表'

# 商品SKU库存
class MerchantProductSpecsStock(MerchantDefModels):

    merchant_product_specs = models.OneToOneField("MerchantProductSpecs", on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(default=0, verbose_name="库存数量")
    number_alerts = models.IntegerField(default=0, verbose_name="警报数量")
    merchant_employee = models.ForeignKey("MerchantEmployee", on_delete=models.DO_NOTHING) # 操作人

    class Meta:
        db_table = 'merchant_product_specs_stock'
        managed = True
        verbose_name = '商家商品SKU库存表'

class MerchantInventory(MerchantDefModels):

    product_sku = models.ForeignKey("MerchantProductSpecs", on_delete=models.DO_NOTHING, verbose_name="商品SPU外键")
    # 库存数量
    quantity = models.BigIntegerField(default=0, verbose_name="数量")
    # 成本价
    cost_price = models.BigIntegerField(default=0, verbose_name="成本价")
    # 安全数量
    gensafetyqty = models.IntegerField(default=0, verbose_name="安全数量")
    merchant_employee = models.ForeignKey("MerchantEmployee", on_delete=models.DO_NOTHING) # 操作人

    class Meta:
        db_table = 'merchant_inventory'
        managed = True
        verbose_name = '商家商品库存表'

class MerchantOutbound(MerchantDefModels):

    # 出库总价
    outbound_price = models.BigIntegerField(default=0, verbose_name="出库总价")
    # 签字人
    signatory = models.ForeignKey("MerchantEmployee", on_delete=models.DO_NOTHING, related_name='bsignatory')
    # 库管
    treasury = models.ForeignKey("MerchantEmployee", on_delete=models.DO_NOTHING, related_name='btreasury')
    # 取货人
    pickup = models.ForeignKey("MerchantEmployee", on_delete=models.DO_NOTHING, related_name='bpickup')
    merchant_employee = models.ForeignKey("MerchantEmployee", on_delete=models.DO_NOTHING) # 操作人

    class Meta:
        db_table = 'merchant_outbound'
        managed = True
        verbose_name = '商家出库表'

# class OutboundInfo(MerchantDefModels):

#     # 类型 商品  原料  物品
#     # 商品
#     # 数量
#     # 总价

#     class Meta:
#         db_table = 'outbound_info'
#         managed = True
#         verbose_name = '出库详情表'

# class Storage(DefModels):

#     class Meta:
#         db_table = 'storage'
#         managed = True
#         verbose_name = '入库表'

# class StorageInfo(DefModels):

#     class Meta:
#         db_table = 'storage_info'
#         managed = True
#         verbose_name = '入库详情表'

# 盘点主表
# 盘点明细表
#

