import os.path
from pathlib import Path
from django.db.models.expressions import Exists, OuterRef

from django.shortcuts import render, redirect
from .forms import VideoForm
from .models import Videos, AnalysisResult
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import sys
import json
import pandas as pd

sys.path.append("..")
from emotion_recognition.main import test_emotions_video_extraction

# def upload_video(request):
#     if request.method == "POST" and request.FILES["myfile"]:
#         myfile = request.FILES["myfile"]
#         fs = FileSystemStorage()
#         filename = fs.save(myfile.name, myfile)
#         uploaded_file_url = fs.url(filename)
#         return render(request, "upload.html", {"uploaded_file_url": uploaded_file_url})
#     return render(request, "upload.html")


def model_form_upload(request):
    if request.method == "POST":
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

    else:
        form = VideoForm()
    return render(request, "videos_form.html", {"form": form})


def videos(request):
    # videos not analyzed (left join)
    not_analyzed_videos = Videos.objects.filter(analysisresult__isnull=True)
    videos_count = Videos.objects.count()
    # videos analyzed (join)
    analyzed_videos = AnalysisResult.objects.select_related("video")
    context = {
        "not_analyzed_videos": not_analyzed_videos,
        "videos_count": videos_count,
        "analyzed_videos": analyzed_videos,
    }
    return render(request, "videos.html", context=context)


def home(request):

    return render(request, "home.html")


def analyze_video(request, id):
    try:
        was_analyzed = AnalysisResult.objects.get(video=id)
    except AnalysisResult.DoesNotExist:
        was_analyzed = None
    print(was_analyzed)
    if was_analyzed is not None:
        print("test")
    v = Videos.objects.get(id=id)
    print(v.video.url)
    result = test_emotions_video_extraction(v.video.url).to_json()
    analyzed_video = AnalysisResult.objects.create(video=v, result=result)
    return redirect("/")
