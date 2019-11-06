from django.db import models
from django.contrib.auth.models import User
from profiles.models import YEARS

TYPES = (
    ('m', 'Mandatory '),
    ('o', 'Optional'),
)


class Project(models.Model):
    name = models.CharField(max_length=150)
    summary = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=200)
    summary = models.TextField(max_length=600, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    credits = models.IntegerField(null=True, default=0)
    mandatory = models.BooleanField(default=True)
    year = models.IntegerField(choices=YEARS, default=1)
    #teacher

    def __str__(self):
        return self.name

    def get_type(self):
        if self.mandatory:
            return "M"
        else:
            return "O"


class Mark(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    mark = models.IntegerField(default=0)

    def __str__(self):
        return self.student + ' ' + self.course + ' ' + self.mark