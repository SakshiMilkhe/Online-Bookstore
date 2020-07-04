from django.urls import path,include,re_path
from . import views



urlpatterns = [

    path('', views.home, name='book-home'),
    path('admin/home/', views.adminHome, name='book-adminHome'),
    path('admin/main/', views.adminMain, name='book-adminMain'),
    path('admin/userList/', views.userList, name='admin-userList'),
    path('admin/addBook/', views.addBook, name='admin-addBook'),
    path(r'^search/$', views.bookfilter, name='search'),
    path('detail/<int:pk>/', views.detail, name='book-detail'),
    path('user/',include('user.urls'),name='user-buyOrder'),
    path('detail/update/<int:pk>/', views.bookUpdate, name='book-update'),
    path('admin/detail/<int:pk>/', views.adminDetail, name='book-adminDetail'),
    path('detail/<int:pk>/cart/', include('user.urls'), name='user-cart'),
    path('detail/<int:pk>/wishList/', include('user.urls'), name='user-wish'),
    #path('type/<int:book>/<int:rat>/',views.ratings, name='book-rat'),
    path('type/<int:book>/',views.filter, name='book-filter'),
    #path('type/<int:book>/<int:rating>/',views.filter, name='book-filter-ratings'),
    path('about/', views.about, name='book-about'),

]