from django.urls import path
from . import views

urlpatterns = [
    path('grid/', views.product_grid, name='product_grid'),
    path('list/', views.product_list, name='product_list'),
    path('detail/<int:pk>/', views.product_detail, name='product_detail'),
]
