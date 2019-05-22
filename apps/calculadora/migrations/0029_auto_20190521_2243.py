# Generated by Django 2.2 on 2019-05-22 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calculadora', '0028_auto_20190521_1630'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoComida',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(help_text='Ingrese el nombre del tipo de comida', max_length=150, verbose_name='Nombre')),
                ('descripcion', models.CharField(help_text='Ingrese una breve descripción de este tipo de comida', max_length=250, verbose_name='Descripción')),
            ],
            options={
                'verbose_name': 'Tipo de Comida',
                'verbose_name_plural': 'Tipos de Comida',
                'ordering': ['nombre'],
            },
        ),
        migrations.AddField(
            model_name='restaurante',
            name='tipo_comida',
            field=models.ManyToManyField(help_text='Seleccione el/los tipos de comida servidos en este restaurante', related_name='restaurantes', to='calculadora.TipoComida', verbose_name='Tipo de comida'),
        ),
    ]
