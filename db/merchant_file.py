# from django.db import models
# from . import DefModels

# class Merchant(DefModels):

#     mer_no = models.CharField(max_length=64, verbose_name="商家编号")
#     mer_name = models.CharField(max_length=1024, verbose_name="商家名称")
#     cliaddress = models.CharField(max_length=255, verbose_name="商家详细地址")
#     cliarea = models.CharField(max_length=255, verbose_name="商家所在地区")
#     introduction = models.TextField(default='', verbose_name="商家简介")
#     logo = models.CharField(max_length=64, verbose_name="商家logo")
#     father_mer = models.ForeignKey(to='self', null=True, on_delete = models.DO_NOTHING, verbose_name="父级")

#     class Meta:
#         db_table = 'merchant'
#         managed = True
#         verbose_name = '商家基础表'

# class MerchantDefModels(DefModels):
#     merchant = models.ForeignKey("Merchant", on_delete=models.DO_NOTHING, verbose_name="商家外键")


# class MerchantApplication(DefModels):

#     merchant = models.ForeignKey("Merchant", on_delete=models.DO_NOTHING, verbose_name="商家外键")
#     application = models.ForeignKey("Application", on_delete=models.DO_NOTHING, verbose_name="应用外键")

#     class Meta:
#         db_table = 'merchant_application'
#         managed = True
#         # unique_together = ('merchant', 'application',)
#         verbose_name = '商家应用表'