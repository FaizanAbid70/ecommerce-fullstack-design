from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_view, name='cart'),
    path('add/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('update/<int:item_id>/', views.update_quantity, name='update_quantity'),
    path('remove/<int:item_id>/', views.remove_item, name='remove_item'),
    path('remove-all/', views.remove_all, name='remove_all'),
    path('save/<int:item_id>/', views.save_for_later, name='save_for_later'),
    path('move/<int:item_id>/', views.move_to_cart, name='move_to_cart'),
]
