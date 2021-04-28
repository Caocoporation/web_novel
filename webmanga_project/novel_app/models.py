from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image
from pathlib import Path
from .utils import title_convertor, resize_image
from .storages import ProtectedStorage
from django.conf import settings
import os

BASE_DIR = Path(__file__).resolve().parent.parent

def debug_storage_mode():
    if settings.DEBUG:
        return ProtectedStorage() 

    return ProtectedStorage()

class Author(models.Model):
    name = models.CharField(max_length=100)
    dob = models.DateField(null=True)
    description = models.TextField()

    def __str__(self):
        if self.name is None:
            return "no author name"
        
        return self.name

def get_novel_thumbnail_path(instance, filename):
    novel_title = title_convertor(str(instance.novel.title))
    return os.path.join("novel_images" , novel_title, filename)

class Novel(models.Model):
    title = models.CharField(max_length=100)
    genre = models.TextField(null=True)
    posted_date = models.DateField(default=timezone.now)
    content = models.TextField(null=True)
    current_chapters = models.IntegerField(default=0)
    status = models.CharField(max_length=50, default="ongoing")
    views = models.IntegerField(default=0)
    author = models.ForeignKey(to=Author, on_delete=models.CASCADE)

    def __str__(self):
        if self.title is not None:
            return self.title

        return "no novel title"


class Novel_Illustration(models.Model): 
    image = models.ImageField(upload_to=get_novel_thumbnail_path, default="no_image.png")
    novel = models.ForeignKey(to=Novel, on_delete=models.CASCADE)

    def save(self):
        super().save()
        img = Image.open(self.image.path)
        resize_image(img=img, saving_path=self.image.path, size=(300, 300))

    def __str__(self):
        if self.image.name is None:
            return "no image"
            
        return self.image.name

class Favorite(models.Model):
    id_novel = models.IntegerField()
    notification = models.IntegerField()
    adding_date = models.DateField(default=timezone.now)    
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    novel = models.ForeignKey(to=Novel, on_delete=models.CASCADE, default="")

def create_chapter_path(instance, filename):
    chapter_title = title_convertor(str(instance.title))
    novel_title = title_convertor(str(instance.novel.title))
    return os.path.join(novel_title, chapter_title, filename)

class Chapter(models.Model):
    title = models.CharField(max_length= 100, null=True)
    posted_date = models.DateField(default=timezone.now)
    content = models.FileField(storage=ProtectedStorage, upload_to=create_chapter_path, null=True, blank=True)
    novel = models.ForeignKey(to=Novel, on_delete=models.CASCADE, default="")

    def __str__(self):
        if self.title is not None: 
            return self.title

        return "no value"

def get_chapter_thumbnail_path(instance, filename):
    novel_title = title_convertor(str(instance.chapter.novel.title))
    chapter_title = title_convertor(str(instance.chapter.title))
    return os.path.join("novel_images" , novel_title, chapter_title, filename)

class Chapter_Illutrations(models.Model):
    illustrations = models.ImageField(upload_to=get_chapter_thumbnail_path, null=True)
    chapter = models.ForeignKey(to=Chapter, on_delete=models.CASCADE)

    def save(self):
        super().save()
        img = Image.open(self.illustrations.path)
        resize_image(img=img, saving_path=self.illustrations.path, size=(300, 300))

 
class Notification(models.Model):
    status = models.IntegerField()
    message = models.TextField()
    date_notification = models.DateTimeField(default = timezone.now)
    time_stamp = models.DateTimeField(auto_now_add=True, null=True)
    nofication_from = models.IntegerField(default=0)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

class Comment(models.Model):
    content = models.TextField()
    likes = models.IntegerField()
    date_comment = models.DateTimeField(default = timezone.now)
    time_stamp = models.DateTimeField(auto_now_add=True, null=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

class Like(models.Model):
    status = models.IntegerField(default=0)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    comment = models.ForeignKey(to=Comment, on_delete=models.CASCADE, default="")

    def __str__(self):
        return str(self.id_novel)

