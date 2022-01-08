from django.urls import path
from . import views

app_name = 'chart'

urlpatterns = [
    path('<int:id>', views.display_chart, name='display_chart'),
]