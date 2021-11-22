from django.shortcuts import render, redirect
from .forms import VideoForm
from .models import Videos
from django.conf import settings
from django.core.files.storage import FileSystemStorage


def upload_video(request):
    if request.method == "POST" and request.FILES["myfile"]:
        myfile = request.FILES["myfile"]
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, "upload.html", {"uploaded_file_url": uploaded_file_url})
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
