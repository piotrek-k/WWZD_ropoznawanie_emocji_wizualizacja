from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.


class Videos(models.Model):
    title = models.CharField(max_length=100)
    video = models.FileField(upload_to="videos/")

    class Meta:
        verbose_name = "video"
        verbose_name_plural = "videos"

    def __str__(self):
        return self.title


class AnalysisResult(models.Model):
    video = models.OneToOneField(Videos, on_delete=CASCADE, primary_key=True)
    # result = models.TextField()
    result = models.JSONField()

