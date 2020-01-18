from django.conf.urls import url, include
from django.urls import re_path

from apps.products import views as product
urlpatterns = [  
    re_path('^specifications/$',product.SpecificationsView.as_view()),
    re_path('^specifications_values/$',product.SpecificationValuesView.as_view()),
    re_path('^product_type/$',product.MerchantProductTypeView.as_view())
]