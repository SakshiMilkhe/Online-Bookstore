from django.urls import path,include
from . import views


urlpatterns = [
    path('<int:pk>/',views.Cart,name='user-cart'),
    path('list/<int:pk>/',views.wishList,name='user-wish'),
    path('order/<int:pk>/',views.order,name='user-order'),
    path('buyOrder/<int:pk>/', views.buyOrder, name='user-buyOrder'),
    path('order/list/<int:pk>/',views.orderList,name='user-orderList'),
    path('order/reviewed',views.orderReviewed,name='user-orderReviewed'),
    path('',views.register,name='register'),
    path('profile/',views.profile,name='user-profile'),
    path('profile/address/',views.address,name='user-address'),
    path('profile/address/create/',views.address_create,name='user-address-create'),
    path('profile/address/update/<int:pk>/',views.address_update,name='user-address-update'),
    path('profile/address/delete/<int:pk>/',views.address_delete,name='user-address-delete'),
    path('rate/<int:pk>/',views.rate,name='user-rating'),


]

