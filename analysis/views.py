import json

import sys
from django.http import JsonResponse, HttpResponse
from django.template import loader
from django.views.decorators.http import require_http_methods

from backend.settings import MIN_MSG_LEN
from datastore.models import Frequent
from ml_models.tv_nb_clr import get_tv_nb_clr

if 'runserver' in sys.argv:
    tv_nb_clr = get_tv_nb_clr()


@require_http_methods(['POST'])
def check(request):
    data = json.loads(request.body)
    if len(data['message']) < MIN_MSG_LEN:
        response = HttpResponse(json.dumps({
            'error': 'tts',
            'message': 'Text too short'
        }), content_type='application/json')
        response.status_code = 202
        return response

    msg_mtx = tv_nb_clr[0].transform([data['message']])
    nb_p = tv_nb_clr[1].predict(msg_mtx.todense())

    label = 'F' if nb_p[0] == 'F' else 'N'
    title = ('Looks like a malicious message' if nb_p[0] == 'F' else
             'Looks like a normal message')

    return JsonResponse({
        'label': label,
        'title': title,
        'description': 'There will be a description here soon',
        'frequent': None
    })


@require_http_methods(['POST'])
def report(request):
    data = json.loads(request.body)
    return JsonResponse({
        'label': 'UC',
        'title': 'Under Construction',
        'description': 'The system is under construction',
        'frequent': None
    })


def dashboard(request):
    """
    dupes = Literal.objects.values('name')
                           .annotate(Count('id'))
                           .order_by()
                           .filter(id__count__gt=1)
    Literal.objects.filter(name__in=[item['name'] for item in dupes])
    """

    frequents_list = Frequent.objects.order_by('-updated_at')[:100]
    template = loader.get_template('analysis/dashboard.html')
    return HttpResponse(
        template.render({'frequents_list': frequents_list}, request)
    )


@require_http_methods(['POST'])
def bot_check(request):
    data = json.loads(request.body)
    return JsonResponse({})
