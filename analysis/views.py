import json
from django.http import HttpResponse

from backend.settings import MIN_MSG_LEN
from ml_models.tv_nb_clr import get_tv_nb_clr

tv_nb_clr = get_tv_nb_clr()


def check(request):
    data = json.loads(request.body)
    if len(data['message']) < MIN_MSG_LEN:
        return HttpResponse('Too little information to tell')
    msg_mtx = tv_nb_clr[0].transform([data['message']])
    nb_p = tv_nb_clr[1].predict(msg_mtx.todense())
    return HttpResponse('Fake' if nb_p[0] == 'F' else 'Normal')


def report(request):
    data = json.loads(request.body)
    return HttpResponse()
