
# Standard
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.urls import reverse
import re
import uuid
import time

# Authentication
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Database
from datetime import datetime
from django.db import IntegrityError, DatabaseError
from .models import *

# Javascript API
import json
from django.http import JsonResponse

# File Handling
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import SuspiciousFileOperation
import os
import tempfile
from zipfile import ZipFile

# Forms
from django.views.decorators.csrf import csrf_exempt
# from .forms import *

# Image Handling
from PIL import Image, ImageColor
from io import BytesIO


from django.core.files import File
from django.core.files.images import ImageFile

# Create your views here.

'''
    path("", views.entry, name="entry"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("index", views.index, name='index'),
'''



def index(request):
    return render(request, "hotdog_app/index.html")



@csrf_exempt
def get_first_pic(request):
    print(f"Django: get_pics()")
    print(f"Return first image in the database")
    time.sleep(1)
    
    if request.method == 'GET':
        print(f"received GET request: OK")
        try:
            first_instance = Artworks.objects.first().serialize()
            print(f"first_instance => {first_instance}")
            return JsonResponse({'new_image': first_instance}, status = 201)
        except Artworks.DoesNotExist:
            return JsonResponse(("No Images"), status = 404)
    else :
        return JsonResponse(("error: Request expects GET method"), status = 301)

@csrf_exempt
def get_next_pic(request, image_order_num):
    print('get_next_pic')
    if request.method == 'GET':
        try:
            image_exists = Artworks.objects.filter(order__gt = image_order_num).exists()
            if image_exists:
                new_image = Artworks.objects.filter(order__gt = image_order_num).first().serialize()
                return JsonResponse({'new_image': new_image}, status = 201)
            else:
                return JsonResponse({'last_pic':'bounce'}, status = 202)
        except Artworks.DoesNotExist:
            return JsonResponse(('error getting image'), status = 500)
    else:
        return JsonResponse(("error: Request expects GET method"), status = 301)
    
@csrf_exempt
def get_prev_pic(request, image_order_num):
    if request.method == 'GET':
        try:
            image_exists = Artworks.objects.filter(order__lt = image_order_num).exists()
            if image_exists:
                new_image = Artworks.objects.filter(order__lt = image_order_num).last().serialize()
                return JsonResponse({'new_image': new_image}, status = 201)
            else:
                return JsonResponse({'first_pic':'bounce'}, status = 202)
        except Artworks.DoesNotExist:
            return JsonResponse(('error getting image'), status = 500)
    else:
        return JsonResponse(("error: Request expects GET method"), status = 301)

