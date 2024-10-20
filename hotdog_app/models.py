
# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_delete, pre_delete
from django.dispatch.dispatcher import receiver
from django.conf import settings
import os


# Create your models here.
class User(AbstractUser):
    def __str__(self):
        return f"{self.pk}, {self.username}, {self.email}"
    
    
class Artworks(models.Model):
    media_url = settings.MEDIA_URL # /hotdog_app_media/
    flipper_images = 'flipper_images' # flipper_images/
    
    id          = models.AutoField(primary_key=True, db_index=True)
    picture     = models.ImageField(null=True, blank=True, upload_to = flipper_images)
    title       = models.CharField(null=False, blank=False, max_length=50)
    description = models.CharField(null=False, blank=False, max_length=512)
    order       = models.PositiveIntegerField(default=0, unique=True, db_index=True)
    
    class Meta:
        ordering = ['order'] # Queries will return items ordered by the order field
    
    def serialize(self):
        return{
            'id'            : self.id,
            'url'           : self.picture.url,
            'name'          : self.picture.name,
            'title'         : self.title,
            'description'   : self.description,
            'order'         : self.order,
        }
    
    # How instance will be shown on Django admin
    def __str__(self):
        return f"Artwork ID: {self.id}, image: {self.picture}, Title: {self.title}, Description: {self.description}  "
    

def _delete_file_from_fs(path):
    # Delete file from file system
    if os.path.isfile(path):
        os.remove(path)
        
@receiver(models.signals.post_delete, sender=Artworks)
def delete_image(sender, instance, *args, **kwargs):
    
    # Fetch all artworks with an order number greater than the one beign deleted
    artworks = Artworks.objects.filter(order__gt=instance.order)
    
    # Adjust the order of all the remaining instances
    for artwork in artworks:
        artwork.order -= 1
        artwork.save
    
    # Delete image from the file system
    if instance.picture:
        _delete_file_from_fs(instance.picture.path)