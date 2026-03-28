from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('cart/', views.cart, name='cart'),
    path('add/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('order/<int:id>/', views.place_order, name='place_order'),
    path('remove/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('logout/', views.user_logout, name='logout'),
]