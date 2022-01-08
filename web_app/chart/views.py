from django.shortcuts import render
from wwzd_app.models import AnalysisResult
import json
import csv
from django.conf import settings
import os

def display_chart(request, id):
  result = AnalysisResult.objects.get(video=id)
  title = result.video.title
  video_id = result.video.id

  result_string = 'frame ' + result.result 
  rows = result_string.split('\n')
  rows.pop(-1)
  rows.pop(-1)

  splitted_rows = []
  for row in rows:
    row = row.split()
    splitted_rows.append(row)

  header = splitted_rows.pop(0)

  filename = os.path.join(settings.BASE_DIR, f'chart/static/{video_id}_{title}_result.csv')
  with open(filename, 'w') as file:
    for header_item in header:
      if header_item != 'box':
        file.write(header_item + ', ')
    file.write('\n')

    for row in splitted_rows:
      for index in range(len(row)):
        if not index in [1,2,3,4] :
          file.write(row[index] + ', ')
      file.write('\n')


  print(splitted_rows)
       


  return render(request, 'chart.html', {"result":result})