from django.urls import path

from analysis.views import check, report

urlpatterns = [
    path('check/', check, name='check'),
    path('report/', report, name='report'),
]
