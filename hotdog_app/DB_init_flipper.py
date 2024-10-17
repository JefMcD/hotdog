
from .models import *
from django.conf import settings
from django.core.files import File
import os
import stat



def install_images():
    print(f"################ install images ################")
    flipper_images = [
            {
            'imgName': 'cthulu-girl-1000.jpg',
            'title' : 'Cthulu Ghirl',
            'description' : 'Octupus haor girl has much on her mind, what with all the scandals and persecutions that have been going on especially since world war three broke out'
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
            'imgName': 'celtic-v-rangers-1000.jpg',
            'title' : 'Celtic Fans',
            'description' : 'Sunday Football Fams on New Years Day'
            },    
        
            {
            'imgName': 'Rivers-Underworld-1000.jpg',
            'title' : 'Rivers Of The Underworld',
            'description' : 'Time travel is not so easy'
            },
    ]
    # set path to images folder
    image_folder = os.path.join(settings.MEDIA_ROOT, 'images/pics') # default images to be loaded into DB
    print (f"---------> MEDIA_ROOT = {settings.MEDIA_ROOT}")
    print (f"---------> BASE_DIR = {settings.BASE_DIR}")
    print (f"---------> image_folder = {image_folder}")
    
    # delete all from artworks
    Artworks.objects.all().delete()
    
    # install pictures into database
    order_number = Artworks.objects.count()
    for pic in flipper_images:
        image_path = os.path.join(image_folder, pic['imgName'])
        if os.path.exists(image_folder):
            new_pic = Artworks(
                title = pic['title'],
                description = pic['description'],
                order = order_number
            )
            new_pic.save()
            
            # open the image file and save it to the database
            with open(image_path, 'rb') as image_file:
                # Cast the opened file to the File() class
                # It then has all the associated methods and variables of this class
                new_image_file = File(image_file)
                
                # Save the image to the Artworks model
                new_pic.picture.save(pic['imgName'], new_image_file)
                
                # pic being saved on pythonanywhere hotdog_app_media/flipper_images
                # pic save 'locked' --w----r-T making it unreadable to the app
                # Set file permissions to be more accessible (e.g., 644)
                image_path = os.path.join(settings.MEDIA_ROOT, 'flipper_images', pic['imgName']) # MEDIA image
                os.chmod(image_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)  # 644 permissions
                order_number += 1
        else:
            print(f"image_path does not exist: {image_path}")




