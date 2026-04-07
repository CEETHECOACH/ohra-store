from django.urls import path
from . import views

urlpatterns = [
    # Public
    path('', views.storefront, name='storefront'),

    # Auth
    path('admin-login/',  views.admin_login,  name='admin_login'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),

    # Admin panel
    path('admin-panel/', views.admin_panel, name='admin_panel'),

    # REST API
    path('api/products/',              views.api_products_list,   name='api_products_list'),
    path('api/products/create/',       views.api_product_create,  name='api_product_create'),
    path('api/products/<int:pk>/',     views.api_product_detail,  name='api_product_detail'),
]
