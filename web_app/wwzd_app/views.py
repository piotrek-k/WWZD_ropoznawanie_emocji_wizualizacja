import os.path
from pathlib import Path

from django.shortcuts import render, redirect
from .forms import VideoForm
from .models import Videos
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from emotion_recognition.main import load_video_then_analise, sha256sum, generate_sha


def upload_video(request):
    if request.method == "POST" and request.FILES["myfile"]:
        myfile = request.FILES["myfile"]
        fs = FileSystemStorage()

        checksum = generate_sha(request.FILES["myfile"])
        print("checksum of file:", checksum)

        emotions = ""

        possible_cache_file = Path("./media/" + checksum + ".cache")
        if not possible_cache_file.is_file():
            # taki film nie był wcześniej wgrywany, rozpocznij analizę

            extension = os.path.splitext(myfile.name)

            filename = fs.save(checksum + extension[1], myfile)
            uploaded_file_path = "./" + fs.url(filename)

            print(uploaded_file_path)

            emotions = load_video_then_analise(uploaded_file_path).to_json()

            with open("./media/" + checksum + ".cache", "w") as text_file:
                text_file.write(emotions)

        else:
            # plik był wcześniej analizowany, zwróć cache

            with open("./media/" + checksum + ".cache", "r") as text_file:
                emotions = str(text_file.read())

        return render(request, "upload.html", {"data": emotions})

    return render(request, "upload.html")


def model_form_upload(request):
    if request.method == "POST":
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

    else:
        form = VideoForm()
    return render(request, "videos_form.html", {"form": form})

# def display(request):

#     videos = Videos.objects.all()
#     context = {
#         "videos": videos,
#     }

#     return render(request, "videos.html", context)
