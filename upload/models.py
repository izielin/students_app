from django.db import models
from projects.models import Course
from django.conf import settings
User = settings.AUTH_USER_MODEL


class File(models.Model):
    file = models.FileField(upload_to='files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    course = models.IntegerField(default="")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
