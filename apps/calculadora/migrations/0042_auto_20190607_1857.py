# Generated by Django 2.2 on 2019-06-07 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculadora', '0041_auto_20190606_1308'),
    ]

    operations = [
        migrations.AddField(
            model_name='ciudad',
            name='file_name',
            field=models.CharField(blank=True, help_text='Nombre del archivo de imagen', max_length=100, null=True, verbose_name='Archivo'),
        ),
        migrations.AddField(
            model_name='restaurante',
            name='file_name',
            field=models.CharField(blank=True, help_text='Ingrese el nombre del backgroud del restaurante', max_length=50, null=True, verbose_name='Background del Restaurante'),
        ),
    ]
