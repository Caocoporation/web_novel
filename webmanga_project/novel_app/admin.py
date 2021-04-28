from django.contrib import admin
from .models import (
    Novel, Author, Chapter, Chapter_Illutrations, 
    Notification, Novel_Illustration
)

# Register your models here.

admin.site.register(Novel)
admin.site.register(Novel_Illustration)
admin.site.register(Author)
admin.site.register(Chapter)
admin.site.register(Chapter_Illutrations)
admin.site.register(Notification)
 