# Generated by Django 2.2 on 2019-06-08 23:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('calculadora', '0052_auto_20190608_2023'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ciudad',
            name='file_name',
        ),
        migrations.RemoveField(
            model_name='restaurante',
            name='file_name',
        ),
    ]