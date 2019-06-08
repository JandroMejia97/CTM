# Generated by Django 2.2 on 2019-06-08 15:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calculadora', '0045_auto_20190607_2057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carta',
            name='restaurante',
            field=models.ForeignKey(blank=True, help_text='Restaurante al que pertenece esta carta', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='seccion', to='calculadora.Restaurante', verbose_name='Restaurante'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='carta',
            field=models.ForeignKey(blank=True, help_text='Seleccione la carta a la que corresponde su producto', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='producto', to='calculadora.Carta'),
        ),
        migrations.AlterField(
            model_name='restaurante',
            name='administrador',
            field=models.ForeignKey(blank=True, help_text='Usuario que añadió este restaurante', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='es_registrado_por', to=settings.AUTH_USER_MODEL, verbose_name='¿Quién lo registró?'),
        ),
    ]