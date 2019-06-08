# Generated by Django 2.2 on 2019-06-08 23:23

from django.db import migrations, models
import storage_backends


class Migration(migrations.Migration):

    dependencies = [
        ('calculadora', '0051_auto_20190608_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ciudad',
            name='foto',
            field=models.ImageField(blank=True, help_text='Cargue una imagen representativa de la ciudad', null=True, storage=storage_backends.PublicMediaStorage(), upload_to='ciudades', verbose_name='Fotografía de la ciudad'),
        ),
        migrations.AlterField(
            model_name='restaurante',
            name='background',
            field=models.ImageField(blank=True, help_text='Cargue una fotografía de su restaurante. Esta se usará como background', null=True, storage=storage_backends.PublicMediaStorage(), upload_to='restaurantes/', verbose_name='Fotografía'),
        ),
        migrations.AlterField(
            model_name='user',
            name='foto',
            field=models.ImageField(blank=True, help_text='Cargue una foto de perfil', null=True, storage=storage_backends.PrivateMediaStorage(), upload_to='', verbose_name='Foto de perfil'),
        ),
    ]