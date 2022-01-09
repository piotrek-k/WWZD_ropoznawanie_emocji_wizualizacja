from django.shortcuts import render
from wwzd_app.models import AnalysisResult
from django.conf import settings
import os
from io import StringIO
import pandas as pd

def display_chart(request, id):
  result = AnalysisResult.objects.get(video=id)
  title = result.video.title
  video_id = result.video.id

  result_string = StringIO('frame' + result.result)
  df = pd.read_csv(result_string) 
  df.drop('box', inplace=True, axis=1)
  
  filename = f'{video_id}_{title}_result.csv'
  filepath = os.path.join(settings.BASE_DIR, 'chart/static/', filename)
  df.to_csv(filepath, index=False)

  return render(request, 'chart.html', {"filename": filename})