# Generated by Django 2.2 on 2019-05-13 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculadora', '0022_auto_20190512_2231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurante',
            name='mapa',
            field=models.CharField(blank=True, help_text='Si lo desea, puede generar el mapa de su ubicación en Google Maps. Vea el tutorial para más información', max_length=600, null=True, verbose_name='Mapa'),
        ),
    ]
