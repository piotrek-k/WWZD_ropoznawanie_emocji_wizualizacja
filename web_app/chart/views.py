import json

from django.templatetags.static import static
from django.shortcuts import render

from web_app.settings import BASE_DIR

def cummulative_chart(request):
    context = {
      'cummulative_chart': {
          'id':           1,
          'chartsource': static('cumulativeLineData.json'),
          'tick_values':  json.dumps([1078030800000,1122782400000,1167541200000,1251691200000]),
      }
    }
    return render(request, 'base.html', context)