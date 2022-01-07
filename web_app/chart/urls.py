from django.urls import path
from . import views

app_name = 'chart'

urlpatterns = [
    path('', views.cummulative_chart, name='cumulative_chart'),
    # path('<int:id>', views.display_chart, name='display_chart'),
]