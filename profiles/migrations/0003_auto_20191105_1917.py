# Generated by Django 2.2.6 on 2019-11-05 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20191103_1332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='picture',
            field=models.ImageField(default='default.jpg', upload_to='profile_pics'),
        ),
    ]