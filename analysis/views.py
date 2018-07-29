import hashlib
import json

import sys

from django.http import JsonResponse, HttpResponse
from django.template import loader
from django.utils import timezone
from django.views.decorators.http import require_http_methods

from backend.settings import MIN_MSG_LEN, CONTACT_MESSAGE
from datastore.models import Frequent, Message
from ml_models.tv_nb_clr import get_tv_nb_clr
from ml_models.utils import normalize

if 'runserver' in sys.argv:
    tv_nb_clr = get_tv_nb_clr()


@require_http_methods(['POST'])
def check(request):
    data = json.loads(request.body)
    message = data['message'].strip()
    normalized_text = normalize(message)
    hash_value = hashlib.sha256(normalized_text.encode('utf-8')).hexdigest()

    if len(message) < MIN_MSG_LEN:
        response = HttpResponse(json.dumps({
            'error': 'tts',
            'message': 'Text too short'
        }), content_type='application/json')
        response.status_code = 202
        return response

    msg_mtx = tv_nb_clr[0].transform([message])
    nb_p = tv_nb_clr[1].predict(msg_mtx.todense())

    label = 'F' if nb_p[0] == 'F' else 'N'
    title = ('Looks like a malicious message' if nb_p[0] == 'F' else
             'Looks like a normal message')

    description = CONTACT_MESSAGE
    frequent = None
    messages = Message.objects.filter(normalized_text=normalized_text)
    if messages:
        frequent = Frequent.objects.get_or_create(
            normalized_text=normalized_text,
            hash_value=hash_value,
            count=len(messages) + 1
        )

    return JsonResponse({
        'label': label,
        'title': title,
        'description': description,
        'frequent': frequent
    })


@require_http_methods(['POST'])
def report(request):
    data = json.loads(request.body)
    message = data['message'].strip()
    normalized_text = normalize(message)
    hash_value = hashlib.sha256(normalized_text.encode('utf-8')).hexdigest()

    if len(message) < MIN_MSG_LEN:
        response = HttpResponse(json.dumps({
            'error': 'tts',
            'message': 'Text too short'
        }), content_type='application/json')
        response.status_code = 202
        return response

    msg_mtx = tv_nb_clr[0].transform([message])
    nb_p = tv_nb_clr[1].predict(msg_mtx.todense())

    label = 'F' if nb_p[0] == 'F' else 'N'
    title = ('Looks like a malicious message' if nb_p[0] == 'F' else
             'Looks like a normal message')

    description = CONTACT_MESSAGE
    messages = Message.objects.filter(normalized_text=normalized_text)
    if messages:
        frequent = Frequent.objects.get_or_create(
            normalized_text=normalized_text,
            hash_value=hash_value,
            count=len(messages) + 1
        )
    else:
        frequent = Frequent.objects.get(
            normalized_text=normalized_text,
            count=1
        )
        new_message = Message.objects.create(
            full_text=message,
            normalized_text=normalized_text,
            hash_value=hash_value,
            updated_at=timezone.now(),
            is_real=True,
            label='R'
        )
        frequent.messages.add(new_message)
        frequent.save()

    return JsonResponse({
        'label': label,
        'title': title,
        'description': description,
        'frequent': frequent,
        'message': 'Successfully reported'
    })


def dashboard(request):
    """
    dupes = Literal.objects.values('name')
                           .annotate(Count('id'))
                           .order_by()
                           .filter(id__count__gt=1)
    Literal.objects.filter(name__in=[item['name'] for item in dupes])
    """

    frequents_list = Frequent.objects.order_by('count')[:100]
    template = loader.get_template('analysis/dashboard.html')
    return HttpResponse(
        template.render({'frequents_list': frequents_list}, request)
    )


def flag_as_fake(request):
    frequents_list = Frequent.objects.order_by('count')[:100]
    template = loader.get_template('analysis/dashboard.html')
    return HttpResponse(
        template.render({'frequents_list': frequents_list}, request)
    )


@require_http_methods(['POST'])
def bot_check(request):
    data = json.loads(request.body)
    return JsonResponse({})
