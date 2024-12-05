

# Standard
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from django.core.cache import cache

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
from django.contrib.staticfiles import finders
import os

#App
from .DB_init_flipper import install_images


arch_images_data = [
    {
    'imgName': '_large_celtic-v-rangers.jpg',
    'title' : 'Celtic V Rangers',
    'description' : 'Celtic fans waiting to get into the pub to watch the Old firm game on New Years Day. 69cm x 40cm Watercolor. Prints £45'
    },

    {
    'imgName': '_large_Glasgow-Byres-Rd.jpg',
    'title' : 'Byres Road',
    'description' : 'A dreech Byers Rd in Glasgows West End, 60cm x 40cm Watercolor. Prints £45'
    },
    {
    'imgName': '_large_Washington-Arch.jpg',
    'title' : 'Washington Arch',
    'description' : 'Landmark in New York City.  60cm x 40cm Watercolor. Prints £45'
    },

    {
    'imgName': '_large_Hidden-In-Plain-Sight-Colour.jpg',
    'title' : 'Hidden in Plain Sight',
    'description' : 'Art fair on the railings. Botanical Gardens in Glasgow.  60cm x 40cm Watercolor. Prints £45'
    },    

    {
    'imgName': '_large_jintyMgintys.jpg',
    'title' : 'Jinty McGuintys',
    'description' : 'Irish pub on Ashton Lane.  60cm x 40cm Watercolor. Prints £45'
    },
    
    {
    'imgName': '_large_glasgow-cafe-wander.jpg',
    'title' : 'Cafe Wander',
    'description': 'Occasionally you might have found some of these pictures in this cafe at one time.  60cm x 40cm Watercolor. Prints £45'
    },
]


occult_images_data = [
    {
        'imgName': 'cthulu-girl-1000.jpg',
        'title' : 'Cthulu Ghirl',
        'description' : 'Octupus hair girl has much on her mind'
    },

    {
        'imgName': 'infinity-eternity-1000.jpg',
        'title' : 'Infinity Eternity',
        'description' : 'Space the final frontier ?'
    },

    {
        'imgName': 'invocation-1000.jpg',
        'title' : 'Invocation',
        'description': 'Summoning the avatar'
    },

    {
        'imgName': 'Rivers-Underworld-1000.jpg',
        'title' : 'Rivers Of The Underworld',
        'description' : 'Time travel is not so easy'
    },
    
    {
        'imgName': '_large_echo-reflection.jpg',
        'title' : 'Echo',
        'description' : 'Oil on Canvas. 1.5m x 1.5m'
    },

    {
        'imgName': '_large_Jessika-In-Oceana.jpg',
        'title' : 'Escape',
        'description': 'Ink on paper, 42cm x 29cm'
    },

    {
        'imgName': '_large_moments.jpg',
        'title' : 'Bubbles',
        'description' : 'Oil on board. 50cm x 30cm'
    },
]


music_images_data = [
    {
    'imgName': 'large_Blondie-Telephone.jpg',
    'title' : 'Blondie Telephone',
    'description' : 'Debbie Harry hangin on the telephephone'
    },

    {
    'imgName': '_large_Bolan-Hydra.jpg',
    'title' : 'Marc Bolan',
    'description': 'T-Rex hydra medusa'
    },

    {
    'imgName': '_large_Jimmy-Page-Double-Guitar.jpg',
    'title' : 'Jimmy Page',
    'description' : 'Led Zeppelin Stairway to Heaven'
    },
        
    {
    'imgName': '_large_Angus-Young-Art.jpg',
    'title' : 'AC/DC Angus',
    'description' : 'Angus Young of ACDC'
    },

    {
    'imgName': '_large_Keith-Richards-Dice.jpg',
    'title' : 'Keef Richards',
    'description' : 'Tumblin Dice'
    },
    
    {
    'imgName': '_large_freddie-mercuryII.jpg',
    'title' : 'Freddie Mercury',
    'description' : 'Queens Freedie Mercury'
    },
]


def db_admin(request):
    # If user is authenticated load db_admin
    if request.user.is_authenticated:
        return render(request, "hotdog_app/db_admin.html")
    else:
        # load login
        return render(request, "hotdog_app/verify/login.html")



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("hotdog_app:db_admin"))
        else:
            return render(request, "hotdog_app/verify/login.html", 
                            {"message": "Invalid username and/or password."
            })
    else:
        return render(request, "hotdog_app/verify/login.html")


def logout_view(request):      
    print(f"Logging Out")
    logout(request)
    return HttpResponseRedirect(reverse("hotdog_app:index"))



@login_required
def occult_images(request):
    Artworks.objects.all().delete()
    cache.clear()
    # Note finder is from staticfiles and depends on the staticfiles data
    # ie run ./manage.py collectstatic for this to work
    try:
        images_folder_path = finders.find('hotdog_app/images/pictures/occult')
    except:
        images_folder_path = None
    if images_folder_path and os.path.exists(images_folder_path):
        good = install_images(occult_images_data, images_folder_path)
        message = 'Pictures Installed' if good else 'Error installing pictures'

    cache.clear() # Fetch new images
    return render(request,'hotdog_app/db_admin.html', {'message':message})


@login_required
def music_images(request):
    Artworks.objects.all().delete()
    cache.clear()
    # Note finders is from staticfiles and depends on the staticfiles data
    # ie run ./manage.py collectstatic or copy files to the staticfiles folder manually for this to work
    try:
        images_folder_path = finders.find('hotdog_app/images/pictures/music')
    except:
        images_folder_path = None
    if images_folder_path and os.path.exists(images_folder_path):
        good = install_images(music_images_data, images_folder_path)
        message = 'Pictures Installed' if good else 'Error installing pictures'

    cache.clear()
    return render(request,'hotdog_app/db_admin.html', {'message':message})
    
    
@login_required
def arch_images(request):
    Artworks.objects.all().delete()
    cache.clear()
    # Note finders is from staticfiles and depends on the staticfiles data
    # ie run ./manage.py collectstatic or copy files to the staticfiles folder manually for this to work
    try:
        images_folder_path = finders.find('hotdog_app/images/pictures/architecture')
    except:
        images_folder_path = None
        
    if images_folder_path and os.path.exists(images_folder_path):
        good = install_images(arch_images_data, images_folder_path)
        message = 'Pictures Installed' if good else 'Error installing pictures'

    cache.clear()  # Ensure new data is loaded.
    return render(request,'hotdog_app/db_admin.html', {'message':message})


@login_required
def delete_all(request):
    print(f"##### delete artworks ####")
    Artworks.objects.all().delete()
    cache.clear()
    image_count = Artworks.objects.all().count()
    print(f"count = {image_count}")
    if(image_count > 0):
        db_status = "Pictures Deleted but DB not empty"
        print(f"remaining images .................")
        for artwork in Artworks.objects.all():
            print(f"name: {artwork.title}")
    else:
        db_status = "Pictures Deleted and DB Empty"

        
    return render(request,'hotdog_app/db_admin.html', {'message':db_status}) 

@login_required
def insert_all(request):
    print(f"##### delete artworks ####")
    Artworks.objects.all().delete()
    cache.clear()
    
    print(f"insert occult images")
    try:
        images_folder_path = finders.find('hotdog_app/images/pictures/occult')
    except:
        images_folder_path = None
    if images_folder_path and os.path.exists(images_folder_path):
        good = install_images(occult_images_data, images_folder_path)
        message = 'Pictures Installed' if good else 'Error installing occult pictures'

    print(f"installing music images")
    try:
        images_folder_path = finders.find('hotdog_app/images/pictures/music')
    except:
        images_folder_path = None
    if images_folder_path and os.path.exists(images_folder_path):
        good = install_images(music_images_data, images_folder_path)
        message = 'Pictures Installed' if good else 'Error installing music pictures'

    try:
        images_folder_path = finders.find('hotdog_app/images/pictures/architecture')
    except:
        images_folder_path = None
        
    if images_folder_path and os.path.exists(images_folder_path):
        good = install_images(arch_images_data, images_folder_path)
        message = 'Pictures Installed' if good else 'Error installing architecture pictures'

    cache.clear()  # Ensure new data is loaded.
    return render(request,'hotdog_app/db_admin.html', {'message':message})



    
    
@login_required    
def inactive(request):
    return render(request, 'network/db_admin.html', {'message':'Button Inactive'})



'''
 -------- Static Files in Views --------------------
Notes on accessing static files from within a View.

In your current setup, you're trying to access static files (images) from within a Django view, which is possible but requires correct configuration to ensure the static files are served properly. The error you're seeing regarding the path not existing could be related to how static files are handled in development vs. production environments, or how the path to the static directory is being constructed in the view.
Key Points for Accessing Static Files:

    Static Files in Views: Normally, static files (CSS, JS, images) are not meant to be handled directly in Django views but are served by the web server (or during development, by Django’s static file handling). To access these files in templates, you use the {% static %} template tag, but from a view, it requires the django.contrib.staticfiles app to resolve the correct static path.

    Using django.contrib.staticfiles: Django provides a helper function static() from django.contrib.staticfiles.storage.StaticFilesStorage, which helps resolve the URL of a static file within views. However, this resolves the URL, not the actual filesystem path.

    Filesystem Path: If you need to access the static files on the filesystem (for reading them or processing them, as in your case), you'll need to construct the absolute path yourself based on STATICFILES_DIRS or STATIC_ROOT.
    
Configuration Changes and Code Adjustment
Settings Update

Make sure that the static file setup is correct:

STATIC_URL = '/static/'
STATICFILES_DIRS = [
     os.path.join(BASE_DIR, 'hotdog_app/static/react_frontend'), 
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


Ensure that you have run collectstatic when DEBUG=False, as this command will collect all the static files into the STATIC_ROOT directory.
Accessing Static Files in a View

Here’s how you can update your code to ensure that the static files are accessed correctly from the view:

    Using finders to locate static files in the filesystem:

    Django’s staticfiles app includes a finders module that can be used to find the actual location of static files on the filesystem.

    This approach will search the staticfiles directories defined in your settings and find the actual filesystem path for the static directory you're trying to access.

    Adjusting install_images function:

    Since images_folder_path will now correctly resolve the folder on the filesystem, you can continue as you already are with the os.path.exists() check and loading the image files.

Notes on Production

In production (with DEBUG=False), Django does not serve static files itself. Make sure your web server (like Nginx or Apache) is properly configured to serve static files from the STATIC_ROOT directory.

    If you're using WhiteNoise, which is built for serving static files in production, ensure that the settings for WhiteNoise are correctly set up as per its documentation.

Conclusion

    In development, Django’s staticfiles app should be able to locate the static files if you configure STATICFILES_DIRS and use the finders utility to resolve the actual path.
    In production, ensure that the static files have been collected using collectstatic, and that your web server or WhiteNoise is configured to serve them correctly.

By using finders.find() to resolve the filesystem path, you should be able to access and manipulate static files from within your views.
'''

