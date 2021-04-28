from rest_framework import serializers
from .models import (
    Novel, Novel_Illustration, Chapter,
    Author, Chapter_Illutrations
)

class Novel_IllustrationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Novel_Illustration
        fields = ("id", "url", "image", "novel")
        depth = 2
        
class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Author
        fields = ("id", "url" , "name", "dob", "description")

class NovelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Novel
        fields = ("id", "title", "genre", "posted_date", "content", "status", "views", "author")
        depth = 1
        


 