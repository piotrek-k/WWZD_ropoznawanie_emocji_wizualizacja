from django.shortcuts import render
from wwzd_app.models import AnalysisResult
from django.conf import settings
import os
from io import StringIO
import pandas as pd
import numpy as np

def display_chart(request, id):
  result = AnalysisResult.objects.get(video=id)
  title = result.video.title
  video_id = result.video.id

  result_string = StringIO("result_number" + result.result)
  ec_df = pd.read_csv(result_string) 
  ec_df = ec_df.fillna(0)

  new_row = []
  for i in range(ec_df.shape[1]):
    new_row.append(0)

  for i in range(0, ec_df.iloc[-1]['frame0'] + 1):
    exists = i in ec_df["frame0"].values
    if not exists:
      column_idx = ec_df.columns.get_loc("frame0")
      new_row[column_idx] = i
      new_df = pd.DataFrame(np.array([new_row]), columns=ec_df.columns)
      ec_df = ec_df.append([new_df], ignore_index=False)

  ec_df = ec_df.sort_values("frame0", ascending = True)

  for column in ec_df.columns:
    if column.startswith("box"):
      ec_df.drop(column, inplace=True, axis=1)

  ec_df.drop('result_number', inplace=True, axis=1)
  for column in ec_df.columns:
    if column != "frame0" and column.startswith("frame"):
      ec_df.drop(column, inplace=True, axis=1)

  for column in ec_df.columns:
    if column != "angry0" and column.startswith("angry"):
      ec_df["angry0"] = round((ec_df["angry0"] + ec_df[column])/2, 2)
      ec_df.drop(column, inplace=True, axis=1)

  for column in ec_df.columns:
    if column != "disgust0" and column.startswith("disgust"):
      ec_df["disgust0"] = round((ec_df["disgust0"] + ec_df[column])/2, 2)
      ec_df.drop(column, inplace=True, axis=1)

  for column in ec_df.columns:
    if column != "fear0" and column.startswith("fear"):
      ec_df["fear0"] = round((ec_df["fear0"] + ec_df[column])/2, 2)
      ec_df.drop(column, inplace=True, axis=1)

  for column in ec_df.columns:
    if column != "happy0" and column.startswith("happy"):
      ec_df["happy0"] = round((ec_df["happy0"] + ec_df[column])/2, 2)
      ec_df.drop(column, inplace=True, axis=1)

  for column in ec_df.columns:
    if column != "sad0" and column.startswith("sad"):
      ec_df["sad0"] = round((ec_df["sad0"] + ec_df[column])/2, 2)
      ec_df.drop(column, inplace=True, axis=1)

  for column in ec_df.columns:
    if column != "surprise0" and column.startswith("surprise"):
      ec_df["surprise0"] = round((ec_df["surprise0"] + ec_df[column])/2, 2)
      ec_df.drop(column, inplace=True, axis=1)

  for column in ec_df.columns:
    if column != "neutral0" and column.startswith("neutral"):
      ec_df["neutral0"] = round((ec_df["neutral0"] + ec_df[column])/2, 2)
      ec_df.drop(column, inplace=True, axis=1)

  cols = ec_df.columns.tolist()
  cols = cols[-1:] + cols[:-1]
  ec_df = ec_df[cols]

  pie_chart_string = []
  for column in list(ec_df.columns):
    pie_chart_string.append(column)
    pie_chart_string.append(',')
  pie_chart_string.pop(-1)
  pie_chart_string.append('\n')

  for column in list(ec_df.columns):
    column_sum = round(ec_df[column].sum(), 2)
    # pie_chart_string.append(str(round((column_sum / len(ec_df.index)), 2)))
    pie_chart_string.append(str(column_sum))
    pie_chart_string.append(',')

  pie_chart_string.pop(-1)
  pc_df = pd.read_csv(StringIO(''.join(pie_chart_string)))  
  pc_df.drop('frame0', inplace=True, axis=1)

  ec_df.rename(columns = {'frame0':'frame', 'angry0':'angry','disgust0':'disgust','fear0':'fear', 'happy0':'happy',
                              'sad0':'sad', 'surprise0':'surprise','neutral0':'neutral',}, inplace = True)
  pc_df.rename(columns = {'frame0':'frame', 'angry0':'angry','disgust0':'disgust','fear0':'fear', 'happy0':'happy',
                              'sad0':'sad', 'surprise0':'surprise','neutral0':'neutral',}, inplace = True)

  emotions_filename = f'{video_id}_{title}_emotions_chart.csv'
  emotions_filepath = os.path.join(settings.BASE_DIR, 'chart/static/', emotions_filename)
  ec_df.to_csv(emotions_filepath, index=False)

  pie_chart_filename = f'{video_id}_{title}_pie_chart.csv'
  pie_chart_filepath = os.path.join(settings.BASE_DIR, 'chart/static/', pie_chart_filename)
  pc_df.to_csv(pie_chart_filepath, index=False)

  return render(request, 'chart.html', {"emotions_filename": emotions_filename,
                                        "pie_chart_filename": pie_chart_filename})