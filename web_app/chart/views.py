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
  ec_df = pd.read_csv(result_string) 
  ec_df.drop('box', inplace=True, axis=1)
  
  pie_chart_string = []
  for column in list(ec_df.columns):
    pie_chart_string.append(column)
    pie_chart_string.append(',')
  pie_chart_string.pop(-1)
  pie_chart_string.append('\n')

  for column in list(ec_df.columns):
    column_sum = ec_df[column].sum()
    # pie_chart_string.append(str(round((column_sum / len(ec_df.index)), 2)))
    pie_chart_string.append(str(column_sum))
    pie_chart_string.append(',')

  pie_chart_string.pop(-1)
  pc_df = pd.read_csv(StringIO(''.join(pie_chart_string)))  
  pc_df.drop('frame', inplace=True, axis=1)

  emotions_filename = f'{video_id}_{title}_emotions_chart.csv'
  emotions_filepath = os.path.join(settings.BASE_DIR, 'chart/static/', emotions_filename)
  ec_df.to_csv(emotions_filepath, index=False)

  pie_chart_filename = f'{video_id}_{title}_pie_chart.csv'
  pie_chart_filepath = os.path.join(settings.BASE_DIR, 'chart/static/', pie_chart_filename)
  pc_df.to_csv(pie_chart_filepath, index=False)

  return render(request, 'chart.html', {"emotions_filename": emotions_filename,
                                        "pie_chart_filename": pie_chart_filename})