from django.urls import path
from django.urls import re_path
from . import views
from . import db_admin

app_name = 'hotdog_app'
urlpatterns = [
    # views paths
    path("", views.index, name='index'),
    path("index", views.index, name='index'),
    
    # API
    path("get_first_pic", views.get_first_pic, name = "get_first_pic"),
    path("get_next_pic/<int:image_order_num>", views.get_next_pic, name = "get_next_pic"),   
    path("get_prev_pic/<int:image_order_num>", views.get_prev_pic, name = "get_prev_pic"), 
    path("ping", views.ping, name="ping"),
    path("contact_form", views.contact_form, name="contact_form"),
    # re_path(r'^.*$', views.index, name='index'),  # Catch-all URL for React routes

    # db_admin paths
    # path("register", views.register, name="register"),
    path('db_admin', db_admin.db_admin, name='db_admin'),
    path("login", db_admin.login_view, name="login_view"),
    path("logout", db_admin.logout_view, name="logout_view"),

    path('occult_images', db_admin.occult_images, name='occult_images'),
    path('music_images', db_admin.music_images, name='music_images'),
    path('arch_images', db_admin.arch_images, name='arch_images'),
    path('delete_all', db_admin.delete_all, name='delete_all'),  
    path('insert_all', db_admin.insert_all, name='insert_all'),
    path('inactive', db_admin.inactive, name='inactive'), 
]


