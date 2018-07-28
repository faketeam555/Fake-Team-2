import json

import sys
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods

from backend.settings import MIN_MSG_LEN
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

    return JsonResponse({
        'label': 'F' if nb_p[0] == 'F' else 'N',
        'title': 'Under Construction',
        'description': 'The system is under construction',
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


@require_http_methods(['POST'])
def bot_check(request):
    data = json.loads(request.body)
    return JsonResponse({})
