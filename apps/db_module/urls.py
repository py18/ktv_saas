from django.urls import re_path
from db_module import views as v

urlpatterns = [
    re_path('merchant', v.CreateMerchant.as_view()),
]