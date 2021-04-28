from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from pathlib import Path
from .utils import delete_junk_image
import os

# from ..webmanga_project.settings import BASE_DIR

BASE_DIR = Path(__file__).resolve().parent.parent


class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    avatar = models.ImageField(default="default.png", upload_to="avatar_image")

    def __str__(self): 
        return f"{self.user.username} Profile"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.avatar.path)
        if img.height > 100 or img.width > 100:
            size = (100, 100)
            img.thumbnail(size) 
            img.save(self.avatar.path)

   
            
           

            

            


       