from django.urls import path
from django.urls import re_path
from . import views
from . import db_admin

app_name = 'hotdog_app'
urlpatterns = [
    # views paths
    path("", views.entry, name="entry"),
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("index", views.index, name='index'),
    
    # API
    path("get_first_pic", views.get_first_pic, name = "get_first_pic"),
    path("get_next_pic/<int:image_order_num>", views.get_next_pic, name = "get_next_pic"),   
    path("get_prev_pic/<int:image_order_num>", views.get_prev_pic, name = "get_prev_pic"), 
 
   #  re_path(r'^.*$', views.index, name='index'),  # Catch-all URL for React routes


    # db_admin paths
    path('db_admin', db_admin.db_admin, name='db_admin'),
    path('insert_images', db_admin.insert_images, name='insert_images'),
    path('delete_all', db_admin.delete_all, name='delete_all'),  
    path('inactive', db_admin.inactive, name='inactive'), 
]


