from django.urls import path

from datastore.views import (
    articles, article_detail, frequents, frequent_detail
)

urlpatterns = [
    path('articles/', articles, name='articles'),
    path('article_detail/', article_detail, name='article_detail'),
    path('frequents/', frequents, name='frequents'),
    path('frequent_detail/', frequent_detail, name='frequent_detail'),
]
