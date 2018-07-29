from django.urls import path

from analysis.views import check, report, bot_check, dashboard, flag_as_fake

urlpatterns = [
    path('check/', check, name='check'),
    path('report/', report, name='report'),
    path('dashboard/', dashboard, name='dashboard'),
    path('flag-fake/<int:id>', flag_as_fake, name='flag_as_fake'),
    path('bot-check/', bot_check, name='bot_check'),
]
