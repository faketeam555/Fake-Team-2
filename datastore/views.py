import json

from django.core.signing import JSONSerializer
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.core import serializers

from datastore.models import Article


@require_http_methods(['POST'])
def articles(request):
    data = json.loads(request.body)
    result = []
    for article in Article.objects.filter(users__phone=data['phone']):
        result.append({
            'title': article.title,
            'content': article.content,
            'label': article.label,
            'created_at': article.created_at,
            'updated_at': article.updated_at
        })
    return JsonResponse(result)


@require_http_methods(['GET'])
def article_detail(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
        return JsonResponse({
            'title': article.title,
            'content': article.content,
            'label': article.frequent.label,
            'created_at': article.created_at,
            'updated_at': article.updated_at,
            'f_count': article.frequent.count,
            'f_location': article.frequent.location
        })
    except:
        response = HttpResponse(json.dumps({
            'error': 'nf',
            'message': 'Not found'
        }), content_type='application/json')
        response.status_code = 404
        return response
