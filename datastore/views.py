import json
from django.http import JsonResponse


def articles(request):
    article_list = [
        {
            'title': 'Article 1 title',
            'brief': 'Brief description of article 1 etc etc',
            'images': 'Link to image 1'
        },
        {
            'title': 'Article 2 title',
            'brief': 'Brief description of article 2 etc etc',
            'images': 'Link to image 2'
        }
    ]
    return JsonResponse(article_list)


def article_detail(request, article_id):
    return JsonResponse({
        'id': 'article_id',
        'title': 'Article headline',
        'verified_by': 'authority',
        'content': 'Content of the article',
        'images': [
            'image link 1',
            'image link 2'
        ],
        'published': 'publication time',
        'updated': 'updation time'
    })
