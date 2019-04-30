from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    foto = models.ImageField(
        upload_to='users/',
        blank=True,
        null=True,
        help_text='Cargue una foto de perfil',
        verbose_name='Foto de perfil'
    )
    fecha_nacimiento = models.DateField(
        blank=True,
        null=True,
        help_text='Seleccione su fecha de nacimiento',
        verbose_name='Fecha de Nacimiento'
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'


class IdiomaOficial(models.Model):
    nombre_idioma = models.CharField(
        max_length=20,
        blank=False,
        null=False,
        help_text='Nombre del idioma',
        verbose_name='Idioma Oficial',
    )
    descripcion_idioma = models.TextField(
        max_length=200,
        blank=False,
        null=False,
        help_text='Breve descripción del idioma',
        verbose_name='Descripción del Idioma',
    )

    def __str__(self):
        return self.nombre_idioma

    class Meta:
        verbose_name = 'Idioma Oficial'
        verbose_name_plural = 'Idiomas Oficiales'


class MonedaOficial(models.Model):
    codigo_moneda = models.CharField(
        max_length=3,
        blank=False,
        null=False,
        unique=True,
        help_text='Codigo de 3 letras',
        verbose_name='Código',
    )
    nombre_divisa = models.CharField(
        max_length=20,
        blank=False,
        null=False,
        help_text='Divisa',
        verbose_name='Nombre divisa',
    )
    decimales = models.IntegerField(
        blank=True,
        null=True,
        help_text='Número de decimales de la moneda',
        verbose_name='Decimal',
    )
    signo = models.CharField(
        max_length=1,
        blank=False,
        null=False,
        help_text='Signo de la moneda',
        verbose_name='Signo',
    )

    def __str__(self):
        return self.nombre_moneda

    class Meta:
        verbose_name = 'Moneda Oficial'
        verbose_name_plural = 'Monedas Oficiales'


class Ciudad(models.Model):
    nombre_ciudad = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        help_text='Ingrese el nombre de la ciudad',
        verbose_name='Nombre',
    )
    pais = models.ForeignKey(
        'Pais',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text='Seleccione el país al que pertenece esta ciudad',
        verbose_name='País',
    )
    ubicacion = models.CharField(
        max_length=30,
        blank=False,
        null=False,
        help_text='Ingrese las coordenadas GPS de la ciudad',
        verbose_name='Ubicacion (GPS)',
    )

    def __str__(self):
        return self.nombre_ciudad

    class Meta:
        verbose_name = 'Ciudad'
        verbose_name_plural = 'Ciudades'


class Pais(models.Model):
    nombre_pais = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        help_text='Ingrese el nombre del país',
        verbose_name='Nombre oficial',
    )
    capital = models.OneToOneField(
        'Ciudad',
        related_name='capital',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        help_text='Capital del país',
        verbose_name='Capital',
    )
    moneda = models.ForeignKey(
        MonedaOficial,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        help_text='Moneda de circulación',
        verbose_name='Moneda oficial',
    )
    idioma = models.ForeignKey(
        IdiomaOficial,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        help_text='Lengua Oficial',
        verbose_name='Idioma Oficial',
    )

    def __str__(self):
        return self.nombre_pais
    
    class Meta:
        verbose_name = 'País'
        verbose_name_plural = 'Países'


class Restaurante(models.Model):
    nombre_restaurante = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        help_text='Ingrese el nombre del restaurante',
        verbose_name='Nombre del Restaurante',
    )
    logo = models.ImageField(
        upload_to='restaurantes/',
        blank=True,
        null=True,
        help_text='Cargue el logotipo que identifica a su restaurante',
        verbose_name='Logotipo'
    )
    ubicacion = models.CharField(
        max_length=30,
        blank=False,
        null=False,
        help_text='Ingrese las coordenadas GPS del restaurante',
        verbose_name='Ubicacion (GPS)',
    )
    direccion = models.CharField(
        max_length=200,
        blank=False,
        null=True,
        help_text='Ingrese la dirección física del restaurante',
        verbose_name='Dirección'
    )
    telefono_regex = RegexValidator(
        regex='^\+?1?\d{9,15}$', 
        message='El número de teléfono se debe ingresar en el formato: "+999999999". Se admiten hasta 15 dígitos.'
    )
    telefono = PhoneNumberField(
        null=False,
        help_text='Ingrese el número telefónico del restaurante en el formato +999999999',
        unique=True,
        verbose_name='Número de Telefono'
    )

    def __str__(self):
        return self.nombre_restaurante

    class Meta:
        verbose_name = 'Restaurante'
        verbose_name_plural = 'Restaurantes'