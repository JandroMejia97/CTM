# Generated by Django 2.2 on 2019-05-13 01:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calculadora', '0021_auto_20190512_2229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurante',
            name='barrio',
            field=models.ForeignKey(help_text='Seleccione el barrio o división política de su ciudad en la que está ubicado el restaurante.', on_delete=django.db.models.deletion.DO_NOTHING, related_name='ubicado_en', to='calculadora.Division', verbose_name='Barrio/Division'),
        ),
    ]
