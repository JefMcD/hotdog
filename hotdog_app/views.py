
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
from django.middleware.csrf import get_token
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

def contact_form(request):
    print(f"######### contact-form ############")
    if request.method == 'POST':
        print(f"received contact form. Processing POST and Returning Json")
         # Retrieving data from the FormData() sent in request
        # and is contained in a dictionary of key:value pairs 
        # 'get' is a dictionary method that will return the value for a specified key
        # https://www.w3schools.com/python/ref_dictionary_get.asp
    
        # Unpck POST formData
        formName    = request.POST.get('fullname')
        formEmail   = request.POST.get('email')
        formSubject = request.POST.get('subject')
        formMessage = request.POST.get('message')
        
        # Create new Instance for the contact data
        try:
            new_contact_message =  Messages(
            sender = formName,
            email = formEmail,
            subject = formSubject,
            msg_body = formMessage,
            )
            new_contact_message.save()
            confirm = new_contact_message.serialize()
            print(f"Message stored in database {confirm}")
        except DatabaseError as error:
            return JsonResponse({'message': error}, status=500)
        except Exception as error:
            return JsonResponse({'message': error}, status=501)

        
        return JsonResponse({'message': confirm}, status = 201)
    else:
        return JsonResponse({'message':'POST required'}, status = 301)
    
def ping(request):
    if request.method == 'GET':
        # Set CSRF token in the response headers
        csrf_token = get_token(request)
        print(f"csrfToken = ", csrf_token)
        response = JsonResponse({'message': 'By The Power Of Greyskull!'})
        response['X-CSRFToken'] = csrf_token
        return response
        # return JsonResponse({'message':'By The Power Of Greyskull!'}, status = 201)
    else:
        return JsonResponse({'message': 'GET required'}, status = 301)
    


@csrf_exempt
def get_first_pic(request):
    print(f"Django: get_first_pic()")
    print(f"Return first image in the database")
    print(f"BASE_DIR: {settings.BASE_DIR}")
    print(f"MEDIA_ROOT: {settings.MEDIA_ROOT}")
    print(f"MEDIA_URL: {settings.MEDIA_URL}")
    
    # mediaImage = os.path.join(settings.MEDIA_ROOT,'_large_celtic-v-rangers.jpg')
    # if os.path.exists(mediaImage):
    #     print(f"Image found {mediaImage}")
    # else:
    #     print(f"404: {mediaImage}")
    time.sleep(0.5)
    
    if request.method == 'GET':
        print(f"received GET request: OK")
        try:
            first_instance_exists = Artworks.objects.filter().exists()
            if first_instance_exists:
                print(f"First Instance Exists")
                first_instance = Artworks.objects.first().serialize()
                return JsonResponse({'new_image': first_instance}, status = 201)
            else:
                print(f"First Instance Not Found")
                # redirect to db_admin path
                return JsonResponse({'message': 'No Images'}, status = 500)


        except Exception as error:
            print(f"Database query returned error {error}")
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

