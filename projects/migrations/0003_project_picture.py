# Generated by Django 2.2.10 on 2020-03-01 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_remove_course_mandatory'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='picture',
            field=models.ImageField(default='default_project.jpg', upload_to='project_pics'),
        ),
    ]
