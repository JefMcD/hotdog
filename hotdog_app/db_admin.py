

# Standard
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from .DB_init_flipper import install_images


# Maths
import random

# Authentication
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Database
from django.db import IntegrityError
from datetime import date
from .models import *

# File Handling
from django.core.files.storage import default_storage
from django.core.exceptions import SuspiciousFileOperation
import re
import os


def db_admin(request):
    return render(request, 'hotdog_app/db_admin.html')

def insert_images(request):
    install_images()
    return render(request,'hotdog_app/db_admin.html', {'message':'Pictures Installed'})

def delete_all(request):
    Artworks.objects.all().delete()
    return render(request,'hotdog_app/db_admin.html', {'message':'All Pictures Deleted'})
     
def inactive(request):
    return render(request, 'network/db_admin.html', {'message':'Button Inactive'})