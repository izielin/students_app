# Generated by Django 3.0 on 2019-12-10 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_auto_20191210_2223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='end_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='course',
            name='start_date',
            field=models.DateField(),
        ),
    ]
