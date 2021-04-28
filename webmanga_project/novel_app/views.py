from django.shortcuts import render, redirect
from django.http import (HttpRequest, JsonResponse, HttpResponse, Http404)
from django.contrib import messages

from .models import (
    Favorite, Novel, Notification, 
    Novel_Illustration, Chapter, 
    Chapter_Illutrations, Author  
)

from django.contrib.auth.models import User

from .forms import (
    AuthorCreationForm,
    NovelCreationForm, 
    NovelUpdateForm,
    NovelIllustrationForm,  
    ChapterCreationForm, 
    ChapterIllustrationForm, 
    Comment
)

from pathlib import Path
from .utils import create_directory, resize_image, title_convertor
from PIL import Image
import os, shutil, stat
import json

from .serializers import (
    NovelSerializer, AuthorSerializer,
    Novel_IllustrationSerializer,
)

#django rest framework
from rest_framework import viewsets, status
from rest_framework.test import APIRequestFactory
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions

#extract docx file
import docx


BASE_DIR = Path(__file__).resolve().parent.parent
novel_name_outside = ""

class NovelIllustrationView(viewsets.ModelViewSet):
    queryset = Novel_Illustration.objects.all()
    serializer_class = Novel_IllustrationSerializer

class NovelView(viewsets.ModelViewSet):
    queryset = Novel.objects.all()
    serializer_class = NovelSerializer

class AuthorView(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

@api_view(["GET"])
def index(request, *args, **kwargs):
    queryset = Novel.objects.all()
    serializer = NovelSerializer(queryset, many=True)

    return Response(serializer.data, status=200)


    # context = {
    #     "novel": Novel.objects.all(),
    #     "novel_illustration": Novel_Illustration.objects.all()
    # }

    # return render(request, template_name="index.htm", context=context)

def authors(request):
    try: 
        authors = Author.objects.all()

    except Author.DoesNotExist:
        raise Http404

    context = {"authors": authors}
    return render(request, template_name="authors.htm", context=context)

def author(request, author_id):
    try:
        author = Author.objects.filter(id=author_id).first()

    except Author.DoesNotExist:
        raise Http404

    context = { "author":  author}
    return render(request, template_name="author.htm", context=context)

def author_creation(request):
    if request.method == "POST":   
        a_form = AuthorCreationForm(request.POST)
      
        pen_name = request.POST.get("name")
        if Author.objects.filter(name=pen_name).first():
            messages.error(
                request, 
                message="This Author Has Already Existed! Please select another one."
            )
            a_form = AuthorCreationForm()

        else:
            messages.success( request,  message="New Author Has Been Created!")
            a_form.save()
            a_form.clean()

            return redirect(to="authors")

    else:
        a_form = AuthorCreationForm()

    form = {"a_form": a_form }

    return render(request, template_name="author_creation.htm", context=form)

def author_deletion(request, author_id):
    try:
        author = Author.objects.filter(id=author_id).first()
        author.delete()
    except Author.DoesNotExist:
        raise Http404
        
    messages.success(request, message="Author has been deleted !")

    return redirect(to="authors")

    # return JsonResponse(data={"status": 200})

def novel(request):
    try:
        novels = Novel.objects.all().order_by("-id")
        thumbnails = Novel_Illustration.objects.all().order_by("-id")
        popular_novels = Novel.objects.all().order_by("-views")[:10]

    except Novel.DoesNotExist or Novel_Illustration.DoesNotExist:
        raise Http404

    popular_novel_thumbanails = []

    orders = [i + 1 for i in range(len(popular_novels))]

    for popular_novel in popular_novels:
        novel_thumbnail =  popular_novel.novel_illustration_set.first()
        popular_novel_thumbanails.append(novel_thumbnail)

    novel_data = list(zip(novels, thumbnails))
    popular_novel_data = list(zip(orders, popular_novels, popular_novel_thumbanails))

    context = { "novel_data": novel_data, "popular_novels": popular_novel_data }

    return render(request, template_name="novels.htm", context=context)

def create_novel(request, author_id):
    if request.method == "POST":
        n_form = NovelCreationForm(request.POST)
        i_form = NovelIllustrationForm(request.POST, request.FILES)

        novel_title = request.POST.get("title")     
        rename_novel_title = "_".join(str(novel_title).split())
        image_name = ""

        create_directory(file_name=rename_novel_title, directory="media/novel_images")
        novel_dir = os.path.join(BASE_DIR, "media/novel_images/{0}".format(rename_novel_title))
        
        image_name =  request.FILES["image"]
        image_name = "_".join(str(image_name).split())

        if n_form.is_valid() and i_form.is_valid():    
            title = request.POST.get("title")
            content = request.POST.get("content")
            genre = request.POST.get("genre")
            novel_cover = request.FILES["image"]
            author = Author.objects.filter(id=author_id).first()

            novel_check = Novel.objects.filter(title=novel_title).first()

            if not novel_check:
                novel = Novel(title=title, content=content, genre=genre, author=author)
                novel.save()

                image_url = "media/novel_images/{0}/{1}".format(rename_novel_title, image_name)
                novel = list(Novel.objects.filter(author=author).all())[-1]
                image = Novel_Illustration(novel=novel, image=novel_cover)
                image.save()

            return redirect(to="novel-page")

    else:
        n_form = NovelCreationForm()
        i_form = NovelIllustrationForm()

    context = {  "n_form": n_form,  "i_form": i_form }

    return render(request, template_name="create_novel.htm", context=context)

def update_novel(request, novel_id):
    novel = Novel.objects.filter(id=novel_id).first()
    novel_thumbnail = Novel_Illustration.objects.filter(novel=novel).first()

    u_form = NovelUpdateForm(instance=novel)
    i_form = NovelIllustrationForm(instance=novel_thumbnail)

    if request.method == "POST":
        n_form = NovelCreationForm(request.POST)
        i_form = NovelIllustrationForm(request.POST, request.FILES)

        novel.title = request.POST.get("title")
        novel.content = request.POST.get("content")
        novel.posted_date = request.POST.get("posted_date")
        novel.status = request.POST.get("status")
        novel.save(update_fields=["title", "content", "status", "posted_date"])

        thumbnail_path = novel_thumbnail.image.path

        if os.path.exists(thumbnail_path):
            os.remove(thumbnail_path)

        novel_thumbnail.image = request.FILES["image"]
        novel_thumbnail.save(update_fields=["image"])
          
        return redirect(to="novel")

    forms = {  "u_form" : u_form, "i_form" : i_form }

    return render(request, template_name="novel_update.htm", context=forms)

def delete_novel(request, novel_id):
    if request.method == "POST":
        user_id = request.user.id
        if User.objects.filter(id=user_id).first().is_staff == 1:
            novel = Novel.objects.filter(id=novel_id).first()
            novel_title = "_".join((novel.title).split()) 
            novel_path = os.path.join(BASE_DIR, "media/novel_images/", novel_title)
        
            if os.path.exists(novel_path):
                files = [ i for i in os.listdir(novel_path) if os.path.isfile(os.path.join(novel_path, i))] 

                for file in files:
                    os.remove(os.path.join(novel_path, file))
                
                folders = os.listdir(novel_path)

                for folder in folders:
                    chapter_path = os.path.join(BASE_DIR, "media/novel_images/", novel_title, folder)
                    folder_files = os.listdir(chapter_path)
                    delete_files = [os.remove(os.path.join(chapter_path, i)) for i in folder_files]
                    os.chmod(chapter_path, stat.S_IWRITE)
                    os.rmdir(chapter_path)

                os.chmod(novel_path, stat.S_IWRITE)
                os.rmdir(novel_path)
                Novel.objects.filter(id=novel_id).delete()

            return JsonResponse(data={"status": 200})

        else: return Http404

def add_views(request, novel_id):
    if request.method == "POST":
        try: 
            novel = Novel.objects.filter(id=novel_id).first()
        except Novel.DoesNotExist:
            raise Http404

        add_views =novel.views + 1
        novel.views = add_views
        novel.save()

    return JsonResponse(data={"status" : 200 })

def chapters(request, novel_id):
    try:
        novel = Novel.objects.filter(id=novel_id).first()
    except Novel.DoesNotExist:
        raise Http404

    add_views =novel.views + 1
    novel.views = add_views
    novel.save()

    context = { "chapters": novel.chapter_set.all(), "novel_id": novel_id }
    return render(request, template_name="chapters.htm", context=context)

def chapter(request, chapter_id):
    try:
        chapter = Chapter.objects.filter(id=chapter_id).first()

    except Chapter.DoesNotExist:
        raise Http404

    if chapter.content.path:
        doc_content = docx.Document(chapter.content.path)
        chapter_content = []

        for paragraph in doc_content.paragraphs:
            chapter_content.append(paragraph.text)

    context = { 
        "chapter": chapter,
        "chapter_thumbnail": chapter.chapter_illutrations_set.first(),
        "chapter_content": chapter_content
    }

    return render(request, template_name="chapter.htm", context=context)

def adding_chapter(request, novel_id):
    if request.method == "POST":
        c_form = ChapterCreationForm(request.POST)
        i_form = ChapterIllustrationForm(request.POST, request.FILES)

        novel = Novel.objects.filter(id=novel_id).first()
        
        if c_form.is_valid() and i_form.is_valid():
            check_existed_chapter = Chapter.objects.filter(title=request.POST.get("title")).first()

            if not check_existed_chapter:
                chapter = Chapter(
                    title = request.POST.get("title"),
                    content = request.FILES.get("content"),
                    novel = novel
                )

                chapter.save()
        
                novel_title = title_convertor(title=novel.title)
                chapter_title =  title_convertor(title=request.POST.get("title"))
                create_directory(file_name=chapter_title, directory="media/novel_images/{0}".format(novel_title))

                image = request.FILES["illustrations"]
                image_name = "_".join(str(image).split())

                chapter = Chapter.objects.filter(title=request.POST.get("title")).first()
 
                illustration_chapter = Chapter_Illutrations(
                    illustrations = image,
                    chapter = chapter
                )

                illustration_chapter.save()

            messages.success(request, message="A New Chapter Is Created.")

            return redirect(to="chapters", novel_id=novel_id)

    else:
        c_form = ChapterCreationForm()
        i_form = ChapterIllustrationForm()

    form = {"c_form" : c_form, "i_form" : i_form }

    return render(request, template_name="chapter_creation.htm", context=form)

def update_chapter(request, chapter_id):
    try:
        chapter = Chapter.objects.filter(id=chapter_id).first()
        chapter_thumbnail = Chapter_Illutrations.objects.filter(chapter=chapter).first()
    except Chapter.DoesNotExist or Chapter_Illutrations.DoesNotExist:
        raise Http404
    
    c_form = ChapterCreationForm(instance=chapter)
    i_form = ChapterIllustrationForm(instance=chapter_thumbnail)

    if request.method == "POST":

        c_form = ChapterCreationForm(request.POST)
        i_form = ChapterIllustrationForm(request.POST, request.FILES)

        chapter.title = request.POST.get("title")
        chapter.content = request.POST.get("content")
        chapter.save(update_fields=["title", "content"])

        if request.FILES["illustrations"]:
            chapter_thumbnail_path = chapter_thumbnail.illustrations.path
            if os.path.exists(chapter_thumbnail_path):
                os.remove(chapter_thumbnail_path)

            chapter_thumbnail.illustrations = request.FILES["illustrations"]
            chapter_thumbnail.save()

        return redirect(to="chapter", chapter_id=chapter_id)

    forms = { "c_form": c_form, "i_form": i_form }
    
    return render(request, template_name="update_chapter.htm", context=forms)

def delete_chapter(request, chapter_id):
    try:
        chapter = Chapter.objects.filter(id = chapter_id).first()

    except Chapter.DoesNotExist:
        raise Http404

    novel_title = title_convertor(chapter.novel.title)
    chapter_title = title_convertor(chapter.title)
    chapter_folder = os.path.join(BASE_DIR, "media/novel_images", novel_title, chapter_title)

    if os.path.exists(chapter_folder):
        if os.listdir(chapter_folder):
            contents = os.listdir(chapter_folder)
            for content in contents:
                os.remove(os.path.join(chapter_folder, content))
            
            os.chmod(chapter_folder, stat.S_IWRITE)
            os.rmdir(chapter_folder)

    chapter.delete()

    return JsonResponse(data={ "status" : 200 })

def searching(request, keyword):
    if request.method == "POST":
        novels = Novel.objects.filter(title__contains = keyword).all()
        results = []
        data = {}

        for novel in novels:
            result = {}
            pos = ((novel.title).lower()).find(keyword.lower())
            result["kepos"] = int(pos)
            result["id"] = novel.id
            result["title"] = novel.title
            results.append(result)

        results = sorted(results, key=lambda i: i.get("kepos"))

        for index, novel in enumerate(results):
            data[index] = novel

        return JsonResponse(data=data) 
    
    return JsonResponse(data={"status" : "400"})