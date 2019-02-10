from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import path, re_path
from just_shop.settings import MY_WEBSITE_NAME

from .views import shop, cart, cart_empty, cart_checkout
from .views_products import product_list, product_view, product_create, product_update, product_delete
from .views_categories import category_list, category_create, category_update, category_delete

urlpatterns = [
    re_path(r'^(?P<category_id>[0-9]+)/$', shop, name='shop'),
    path('', shop, name='shop'),
    path('cart/', cart, name='cart'),
    path('cart/empty/', cart_empty, name='cart_empty'),
    path('cart/checkout/', cart_checkout, name='cart_checkout'),
    #
    path('products/', product_list, name='product_list'),
    path('products/new/', product_create, name='product_create'),
    path('products/view/<int:product_id>/', product_view, name='product_view'),
    path('products/update/<int:product_id>/', product_update, name='product_update'),
    path('products/delete/<int:product_id>/', product_delete, name='product_delete'),
    #
    path('categories/', category_list, name='category_list'),
    path('categories/new/', category_create, name='category_create'),
    path('categories/update/<int:category_id>/', category_update, name='category_update'),
    path('categories/delete/<int:category_id>/', category_delete, name='category_delete'),
]
