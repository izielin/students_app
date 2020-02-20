from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from profiles.models import YEARS
from django.conf import settings
from django.utils import timezone
User = settings.AUTH_USER_MODEL


class Project(models.Model):
    name = models.CharField(max_length=150)
    summary = models.TextField(null=True, blank=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=200)
    summary = models.TextField(max_length=600, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    points = models.IntegerField(null=True, default=0)
    year = models.IntegerField(choices=YEARS, default=1)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class File(models.Model):
    file = models.FileField(upload_to='files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    course = models.IntegerField(default="")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True)


class Mark(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    mark = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(50)])
    date = models.DateTimeField(default=timezone.now, blank=True)

    def __str__(self):
        return 'Student' + ' ' + str(self.student) + ' ' + str(self.mark) +'/'+str(self.course.points)