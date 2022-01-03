"""web_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from wwzd_app.views import model_form_upload, home, videos, analyze_video

urlpatterns = [
    path("admin/", admin.site.urls),
    path("chart/", include("chart.urls", namespace="chart")),
    # path("upload/", upload_video, name="upload"),
    path("upload_form/", model_form_upload, name="upload_form"),
    path("", home, name="home"),
    path("videos/", videos, name="videos"),
    path("analyze_video/<int:id>", analyze_video, name="analyze_video"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
