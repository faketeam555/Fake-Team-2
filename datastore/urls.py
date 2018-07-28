from django.urls import path

from datastore.views import articles, article_detail

urlpatterns = [
    path('articles/', articles, name='articles'),
    path('article-detail/<int:article_id>/', article_detail, name='article_detail'),
]
