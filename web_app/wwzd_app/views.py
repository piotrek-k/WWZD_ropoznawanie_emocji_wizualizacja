import os.path
from pathlib import Path

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
    videos = Videos.objects.all()
    videos_count = Videos.objects.count()
    context = {
        "videos": videos,
        "videos_count": videos_count,
    }
    return render(request, "videos.html", context=context)


def home(request):

    return render(request, "home.html")


def analyze_video(request, id):
    v = Videos.objects.get(id=id)
    print(v.video.url)
    result = test_emotions_video_extraction(v.video.url)
    analyzed_video = AnalysisResult.objects.create(video=v, result=result)
    return redirect("/")
