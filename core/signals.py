from django.db.models.signals import post_save
from .models import User
from django.dispatch import receiver
from profiles.models import StudentProfile, TeacherProfile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if User.is_teacher is True:
            TeacherProfile.objects.create(user=instance)
        elif User.is_student is True:
            StudentProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    if User.is_teacher is True:
        instance.teacherprofile.save()
    elif User.is_student is True:
        instance.studentprofile.save()