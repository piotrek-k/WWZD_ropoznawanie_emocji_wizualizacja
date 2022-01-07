from django.shortcuts import render
from wwzd_app.models import AnalysisResult


def display_chart(request, id):
  result = AnalysisResult.objects.get(video=id)
  print(result.result)

  return render(request, 'chart.html', {'result': result})