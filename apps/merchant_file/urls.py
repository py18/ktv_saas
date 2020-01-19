from django.conf.urls import url, include

from apps.merchant_file.utils_views import login_view
from apps.merchant_file.utils_views import register
from apps.merchant_file.utils_views import child_manage
from apps.merchant_file.utils_views import staff_manage

urlpatterns = [
    # 登录
    url(r'^login/$',login_view.LoginView.as_view()),
    # 注册
    url(r'^register/$',register.RegistView.as_view()),
    # 子店管理
    url(r'^child_mer/$',child_manage.ChaildMerchantInfoManageView.as_view()),
    # 部门管理
    # url(r'^department_manage/$',staff_manage.DepartmentManageView.as_view()),
    # # 职位管理
    # url(r'^position_manage/$',staff_manage.PositionManageView.as_view()),
    # # 员工管理
    # url(r'^staff_manage/$',staff_manage.StaffManageView.as_view()),
]