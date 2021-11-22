from django.urls import path
from . import views

app_name = 'chart'

urlpatterns = [
    path('', views.cummulative_chart, name='cumulative_chart'),
]