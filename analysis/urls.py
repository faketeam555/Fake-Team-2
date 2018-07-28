from django.urls import path

from analysis.views import check, report, bot_check

urlpatterns = [
    path('check/', check, name='check'),
    path('bot_check/', bot_check, name='bot_check'),
    path('report/', report, name='report'),
]
