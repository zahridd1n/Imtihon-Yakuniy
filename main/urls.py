from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('category/create/', views.category_create, name='category_create'),
    path('category/list/', views.category_list, name='category_list'),
    path('category/edit/<int:id>', views.category_edit, name='category_edit'),
    path('category/delete/<int:id>', views.category_delete, name='category_delete'),

    path('product/create/', views.product_create, name='product_create'),
    path('product/list/', views.product_list, name='product_list'),
    path('product/detail/<str:code>', views.product_detail, name='product_detail'),
    path('product/edit/<str:code>', views.product_edit, name='product_edit'),
    path('product/delete/<str:code>', views.product_delete, name='product_delete'),

    path('enter-product/create/', views.enter_product_create, name='enter_product_create'),
    path('enter-product/list/', views.enter_product_list, name='enter_product_list'),
    path('enter-product/edit/<str:code>/', views.enter_product_edit, name='enter_product_edit'),

    path('export-product/create/', views.export_product_create, name='export_product_create'),
    path('export-product/list/', views.export_product_list, name='export_product_list'),
    path('export-product/edit/<str:code>/', views.export_product_edit, name='export_product_edit'),

    path('return-product/create/', views.return_product, name='return_product'),
    path('return-product/list/', views.return_product_list, name='return_product_list'),
    path('return-product/edit/<str:code>/', views.return_product_edit, name='return_product_edit'),

    path('log-in/', views.log_in, name='log_in'),
    path('log-out/', views.log_out, name='log_out'),

    path('query/',views.query, name='query'),

]