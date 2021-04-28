from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('novel_api', views.NovelView)
router.register('author_api', views.AuthorView)
router.register('novel_thumbnail_api', views.NovelIllustrationView)

urlpatterns = [
    path('index', views.index, name='novel-home'),
    path('', views.novel, name='novel-page'),
    path('authors', views.authors, name='authors'),
    path('author/<int:author_id>', views.author, name='author'),
    path('author_create', views.author_creation, name='author-creation'),
    path('author_deletion/<int:author_id>', views.author_deletion, name='author-deletion'),
    path('novel', views.novel, name='novel'), 
    path('create_novel/<int:author_id>', views.create_novel, name='novel-creation'),
    path('update_novel/<int:novel_id>', views.update_novel, name='novel-update'),
    path('delete_novel/<int:novel_id>', views.delete_novel, name='novel-deletion'),
    path('add_chapter/<int:novel_id>', views.adding_chapter, name='chapter-addition'),
    path('chapters/<int:novel_id>', views.chapters, name="chapters"),
    path('chapter/<int:chapter_id>', views.chapter, name="chapter"),
    path('update_chapter/<int:chapter_id>', views.update_chapter, name="chapter-update"),
    path('delete_chapter/<int:chapter_id>', views.delete_chapter, name="chapter-deletion"),
    path('add_view/<int:novel_id>', views.add_views, name="add-view"),
    path('search/<str:keyword>', views.searching, name="search-novel"),
    path('api/novels/', include(router.urls), name='api-novels')
]
