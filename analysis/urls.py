from django.urls import path

from analysis.views import check, report, bot_check, dashboard

urlpatterns = [
    path('check/', check, name='check'),
    path('report/', report, name='report'),
    path('dashboard/', dashboard, name='dashboard'),
    path('bot_check/', bot_check, name='bot_check'),
]
