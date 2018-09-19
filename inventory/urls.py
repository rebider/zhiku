"""thinking_library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import xadmin
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    path("city", views.city_list, name="city_list"),
    path("city_edit", views.city_edit, name='city_edit'),
    path("city_country",views.city_country, name="city_country"),
    path("country", views.country_list, name="country_list"),
    path("country_edit", views.country_edit, name='country_edit'),
    path("goods", views.goods_list, name="goods_list"),
    path("goods_edit", views.goods_edit, name='goods_edit'),
    path("goods_category", views.goods_category_list, name="goods_category_list"),
    path("goods_category_edit", views.goods_category_edit, name='goods_category_edit'),
    path("goods_unit", views.goods_unit_list, name="goods_unit_list"),
    path("goods_unit_edit", views.goods_unit_edit, name='goods_unit_edit'),
    path("nation", views.nation_list, name="nation_list"),
    path("nation_edit", views.nation_edit, name='nation_edit'),
    path("nation_province", views.nation_province, name='nation_province'),
    path("province_city", views.province_city, name='province_city'),
    path("province", views.province_list, name='province_list'),
    path("province_city", views.province_edit, name='province_edit'),
    path("industry", views.industry_list, name="industry_list"),
    path("industry_edit", views.industry_edit, name='industry_edit'),
    path("supplier", views.supplier_list, name="supplier_list"),
    path("supplier_edit", views.supplier_edit, name='supplier_edit'),
    path("supplier_category", views.supplier_category_list, name="supplier_category_list"),
    path("supplier_category_edit", views.supplier_category_edit, name='supplier_category_edit'),
    path("supplier_linkman", views.supplier_linkman, name='supplier_linkman'),
    path("supplier_contact", views.supplier_contact, name='supplier_contact'),
    path("supplier_detail", views.supplier_detail, name='supplier_detail'),
    path("linkman_detail", views.linkman_detail, name="linkman_detail"),
    path("upload_goods_photo", views.goods_photo, name="goods_photo"),
    path("upload_goods_code", views.goods_code, name="goods_code"),
    path("upload_linkman_photo", views.linkman_photo, name="linkman_photo"),
    path("upload_linkman_card", views.linkman_card, name="linkman_card"),
    path("upload_supplier_photo", views.supplier_photo, name="supplier_photo"),
    path("upload_supplier_licence", views.supplier_licence, name="supplier_licence"),
    path("upload_attach", views.supplier_attach, name="supplier_attach"),
    path("upload_attach", views.goods_attach, name="goods_attach"),
    path("upload_attach", views.linkman_attach, name="linkman_attach"),
    path("upload_attach", views.contact_attach, name="contact_attach"),


]