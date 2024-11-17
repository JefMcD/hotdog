
from .models import *
from django.conf import settings
from django.core.files import File
import os
import stat

from django.contrib.staticfiles.storage import staticfiles_storage


#
#   flipper_images - array of objects containing details of the images to be inserted into the database (The Upload details)
#   images-folder - the path to where the source images are stored on the filesystem (The Upload images)
#
def install_images(flipper_images, images_folder):
    print(f"################ install images ################")
    installed_success = True
    # set path to images folder
    # image_folder = os.path.join(settings.MEDIA_ROOT, 'images/pics') # default images to be loaded into DB
    
    print (f"---------> MEDIA_ROOT = {settings.MEDIA_ROOT}")
    print (f"---------> BASE_DIR = {settings.BASE_DIR}")
    print (f"---------> image_folder = {images_folder}")
    
    # delete all from artworks
    Artworks.objects.all().delete()
    
    # install pictures into database
    order_number = Artworks.objects.count()
    for pic in flipper_images:
        image_path = os.path.join(images_folder, pic['imgName'])
        if os.path.exists(images_folder):
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
                
                # Set Permissions on uploaded Media
                # pic being saved on pythonanywhere hotdog_app_media/...
                # pic save 'locked' --w----r-T making it unreadable to the app
                # Set file permissions to be more accessible (e.g., 664)
                # image_path = os.path.join(settings.MEDIA_ROOT, 'flipper_images', pic['imgName']) # MEDIA image stored in /hotdog_app_media/flipper_images/imageName.jpg
                image_path = os.path.join(settings.MEDIA_ROOT, pic['imgName']) # MEDIA image stored in /hotdog_app_media/imageName.jpg
                os.chmod(image_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)  # 644 permissions
                order_number += 1
        else:
            print(f"image_path does not exist: {image_path}")
            installed_success = False
            
    return installed_success




