from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, MaxLengthValidator
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

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
    nombre = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text='Nombre del idioma',
        verbose_name='Idioma',
    )
    iso_639_1 = models.CharField(
        max_length=2,
        blank=False,
        null=False,
        unique=True,
        help_text='Indique el código del idioma en formato ISO 639-1 alpha-2. Por ejemplo, para el Español su codigo es "es"',
        verbose_name='ISO 639-1'
    )

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Idioma Oficial'
        verbose_name_plural = 'Idiomas Oficiales'
        ordering = ['nombre']


class MonedaOficial(models.Model):
    iso_4217 = models.CharField(
        max_length=3,
        blank=False,
        null=False,
        unique=True,
        help_text='Indique el código de la divisa en formato ISO 4217. Por ejemplo, para el peso argentino su codigo es "ARS"',
        verbose_name='Codigo ISO 4217'
    )
    iso_4217_numerico = models.IntegerField(
        blank=True,
        null=True,
        unique=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(999)
        ],
        help_text='Indique el código de la divisa en formato ISO 4217. Por ejemplo, para el peso argentino su codigo numérico es "32"',
        verbose_name='Codigo ISO 4217 Numérico'
    )
    nombre_divisa = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text='Indique el nombre de la moneda. Por ejemplo, la moneda de Argentina se llama "Peso argentino"',
        verbose_name='Moneda',
    )
    decimales = models.IntegerField(
        blank=True,
        null=True,
        help_text='Número de decimales de la moneda',
        verbose_name='Decimal',
    )
    simbolo = models.CharField(
        max_length=8,
        blank=True,
        null=True,
        help_text='Símbolo de la moneda',
        verbose_name='Símbolo',
    )

    def __str__(self):
        return self.nombre_divisa

    class Meta:
        verbose_name = 'Moneda Oficial'
        verbose_name_plural = 'Monedas Oficiales'
        ordering = ['nombre_divisa']


class Ciudad(models.Model):
    nombre = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        help_text='Ingrese el nombre de la ciudad',
        verbose_name='Nombre',
    )
    foto = models.ImageField(
        upload_to='ciudades',
        blank=True,
        null=True,
        help_text='Cargue una imagen representativa de la ciudad',
        verbose_name='Fotografía de la ciudad'
    )
    pais = models.ForeignKey(
        'Pais',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text='Seleccione el país al que pertenece esta ciudad',
        verbose_name='País',
    )
    
    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Ciudad'
        verbose_name_plural = 'Ciudades'
        ordering = ['nombre']


class Division(models.Model):
    nombre = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        help_text='Ingrese el nombre de la division',
        verbose_name='Nombre',
    )
    ciudad = models.ForeignKey(
        'Ciudad',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text='Seleccione la ciudad a la que pertenece esta region',
        verbose_name='Ciudad',
    )
    latitud = models.DecimalField(
        blank=True,
        null=True,
        unique=True,
        decimal_places=6,
        max_digits=9,
        validators=(
            MinValueValidator(-90.00000),
            MaxValueValidator(90.00000)
        ),
        help_text='La latitud está dada en grados decimales, entre 0° y 90 ° en el hemisferio Norte y entre 0° y -90° en el hemisferio Sur',
        verbose_name='Latitud'
    )
    longitud = models.DecimalField(
        blank=True,
        null=True,
        unique=True,
        decimal_places=6,
        max_digits=9,
        validators=[
            MinValueValidator(-180.00000),
            MaxValueValidator(180.00000)
        ],
        help_text='La longitud está dada en grados decimales, entre 0° y 180°, al este del meridiano de Greenwich y entre 0° y -180°, al oeste del meridiano de Greenwich.',
        verbose_name='Longitud'
    )
    
    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'División política de la ciudad'
        verbose_name_plural = 'División Política'


class Continente(models.Model):
    nombre =  models.CharField(
        max_length=25,
        blank=False,
        null=False,
        help_text='Nombre del continente',
        verbose_name='Continente'
    )
    codigo = models.CharField(
        max_length=3,
        unique=True,
        blank=False,
        help_text='Codigo del continente'
    )

    def __str__(self):
        return str(self.nombre).upper()

    class Meta:
        verbose_name = 'Continente'
        verbose_name_plural = 'Continentes'
        ordering = ['nombre']


class Pais(models.Model):
    nombre = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text='Ingrese el nombre del país',
        verbose_name='Nombre oficial',
    )
    iso_3166_1_2 = models.CharField(
        max_length=3,
        blank=True,
        null=True,
        help_text='Indique el código del país en formato ISO 3166-1 alpha-2. Por ejemplo, para la bandera de la República de El Salvador es SV',
        verbose_name='Codigo ISO 3166-1 alpha-2'
    )
    iso_3166_1_3 = models.CharField(
        max_length=3,
        blank=True,
        null=True,
        help_text='Indique el código del país en formato ISO 3166-1 alpha-3. Por ejemplo, para la bandera de la República de El Salvador es SLV',
        verbose_name='Codigo ISO 3166-1 alpha-3'
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
    continente = models.ForeignKey(
        Continente,
        related_name='continente',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        help_text='Contiente donde se ubica el país',
        verbose_name='Continente',
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
        return str(self.nombre).upper()
    
    class Meta:
        verbose_name = 'País'
        verbose_name_plural = 'Países'
        ordering = ['continente','nombre']


class TipoComida(models.Model):
    nombre = models.CharField(
        max_length=150,
        blank=False,
        null=False,
        help_text='Ingrese el nombre del tipo de comida',
        verbose_name='Nombre'
    )
    descripcion = models.CharField(
        max_length=250,
        blank=False,
        null=False,
        help_text='Ingrese una breve descripción de este tipo de comida',
        verbose_name='Descripción'
    )

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Tipo de Comida'
        verbose_name_plural = 'Tipos de Comida'
        ordering = ['nombre']


class Restaurante(models.Model):
    nombre = models.CharField(
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
    latitud = models.DecimalField(
        blank=True,
        null=True,
        decimal_places=6,
        max_digits=9,
        validators=(
            MinValueValidator(-90.00000),
            MaxValueValidator(90.00000)
        ),
        help_text='La latitud está dada en grados decimales, entre 0° y 90 ° en el hemisferio Norte y entre 0° y -90° en el hemisferio Sur',
        verbose_name='Latitud'
    )
    longitud = models.DecimalField(
        blank=True,
        null=True,
        decimal_places=6,
        max_digits=9,
        validators=[
            MinValueValidator(-180.00000),
            MaxValueValidator(180.00000)
        ],
        help_text='La longitud está dada en grados decimales, entre 0° y 180°, al este del meridiano de Greenwich y entre 0° y -180°, al oeste del meridiano de Greenwich.',
        verbose_name='Longitud'
    )
    direccion = models.CharField(
        max_length=200,
        blank=False,
        null=True,
        help_text='Ingrese la dirección física del restaurante',
        verbose_name='Dirección'
    )
    telefono = PhoneNumberField(
        null=False,
        help_text='Ingrese el número telefónico del restaurante en el formato +999999999',
        unique=True,
        verbose_name='Número de Telefono'
    )
    mapa = models.CharField(
        max_length=600,
        blank=True,
        null=True,
        help_text='Si lo desea, puede generar el mapa de su ubicación en Google Maps. Vea el tutorial para más información',
        verbose_name='Mapa'
    )
    barrio = models.ForeignKey(
        Division,
        related_name='ubicado_en',
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
        help_text='Seleccione el barrio o división política de su ciudad en la que está ubicado el restaurante.',
        verbose_name='Barrio/Division'
    )
    administrador = models.ForeignKey(
        User,
        related_name='es_registrado_por',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        help_text='Usuario que añadió este restaurante',
        verbose_name='¿Quién lo registró?'
    )
    tipo_comida = models.ManyToManyField(
        TipoComida,
        help_text='Seleccione el/los tipos de comida servidos en este restaurante',
        related_name='restaurantes',
        verbose_name='Tipo de comida',
        blank=False,
        null=False
    )

    def __str__(self):
        return self.nombre

    """def path_and_rename(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = 'logo{}.{}'.format(instance.nombre, ext)
        return os.path.join(
            self.ciudad.pais.continente.nombre,
            self.ciudad.pais.nombre,
            self.ciudad.nombre,
            'restaurantes',
            self.nombre,
            filename
        )"""

    class Meta:
        verbose_name = 'Restaurante'
        verbose_name_plural = 'Restaurantes'


class TipoCarta(models.Model):
    nombre = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        help_text='Ingrese el nombre de la carta',
        verbose_name='Nombre'
    )
    descripcion = models.CharField(
        max_length=150,
        blank=False,
        null=False,
        validators=[
            MinLengthValidator(50)
        ],
        help_text='Ingrese una breve descripción de esta carta (Entre 50 y 150 caracteres)',
        verbose_name='Descripción'
    )
    tipo_principal = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='subcartas',
        null=True,
        blank=True,
        help_text='Seleccione una carta sí la carta que está por registrar es un subconjunto de alguna carta ya existente',
        verbose_name='Carta Principal'
    )

    def __str__(self):
        return 'Carta de '+self.nombre

    class Meta:
        verbose_name = 'Tipo de Carta'
        verbose_name_plural = 'Tipos de Carta'


class Carta(models.Model):
    tipo = models.ForeignKey(
        TipoCarta,
        related_name='identificada_por',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        help_text='Seleccione el tipo de carta que posee este restaurante',
        verbose_name='Tipo de carta'
    )
    restaurante = models.ForeignKey(
        Restaurante,
        related_name='seccion',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        help_text='Restaurante al que pertenece esta carta',
        verbose_name='Restaurante'

    )

    def __str__(self):
        return self.tipo.nombre

    class Meta:
        verbose_name = 'Carta'
        verbose_name_plural = 'Cartas'


class Producto(models.Model):
    nombre = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text='Ingrese el nombre del producto',
        verbose_name='Nombre del producto'
    )
    descripcion = models.TextField(
        max_length=300,
        blank=True,
        null=True,
        validators=[
            MinLengthValidator(50)
        ],
        help_text='Ingrese una breve descripción de este producto (entre 50 y 300 caracteres)',
        verbose_name='Descripción del producto'
    )
    imagen = models.ImageField(
        upload_to='Productos/',
        blank=True,
        null=True,
        help_text='Cargue una foto representativa de su producto',
        verbose_name='Foto del producto'
    )
    precio_fijo = models.DecimalField(
        blank=True,
        null=True,
        decimal_places=2,
        max_digits=10,
        validators=[
            MinValueValidator(0.00),
        ],
        help_text='Ingrese el precio del producto fijado por el restaurante',
        verbose_name='Precio'
    )
    carta = models.ForeignKey(
        Carta,
        related_name='producto',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        help_text='Seleccione la carta a la que corresponde su producto'
    )

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'


class Precio(models.Model):
    monto = models.DecimalField(
        blank=False,
        null=False,
        decimal_places=2,
        max_digits=10,
        validators=[
            MinValueValidator(0.00),
        ],
        help_text='Ingrese el precio al cual encontró este producto en el restaurante',
        verbose_name='Precio'
    )
    fecha_adicion = models.DateTimeField(
        blank=True,
        null=False,
        auto_now_add=True,
        help_text='Fecha en la que se registró este nuevo precio',
        verbose_name='Fecha del registro'
    )
    aprobaciones = models.IntegerField(
        blank=True,
        null=True,
        default=0,
        validators=[MinValueValidator(0)],
        help_text='Se refiere al número de usuarios que han encontrado este producto a este mismo precio en dicho restaurante',
        verbose_name='Aprobaciones'
    )
    desaprobaciones = models.IntegerField(
        blank=True,
        null=True,
        default=0,
        validators=[MinValueValidator(0)],
        help_text='Se refiere al número de usuarios que han encontrado este producto a un precio diferente en dicho restaurante',
        verbose_name='Aprobaciones'
    )
    producto = models.ForeignKey(
        Producto,
        related_name='registra',
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        help_text='Producto que se presenta una variación en su precio',
        verbose_name='Producto'
    )
    moneda = models.ForeignKey(
        MonedaOficial,
        related_name='dado_en',
        on_delete=models.DO_NOTHING,
        blank=False,
        null=False,
        help_text='Moneda en la que se ha registrado este precio',
        verbose_name='Moneda'
    )
    usuario = models.ForeignKey(
        User,
        related_name='agregado_por',
        on_delete=models.DO_NOTHING,
        blank=False,
        null=False,
        help_text='Usuario que registró este precio',
        verbose_name='Agregado por'
    )

    def __str__(self):
        return str(self.monto)

    class Meta:
        verbose_name = 'Precio'
        verbose_name_plural = 'Precios'


class Compra(models.Model):
    total = models.DecimalField(
        blank=False,
        null=False,
        decimal_places=2,
        max_digits=20,
        validators=[
            MinValueValidator(0.00),
        ],
        help_text='Este es el monto total de la compra',
        verbose_name='Monto total'
    )
    fecha = models.DateTimeField(
        blank=True,
        null=False,
        auto_now_add=True,
        help_text='Fecha en la que se registró este compra',
        verbose_name='Fecha de la compra'
    )
    comprador = models.ForeignKey(
        User,
        related_name='realiza',
        on_delete=models.DO_NOTHING,
        blank=False,
        null=False,
        help_text='Usuario que realizó la compra',
        verbose_name='Comprador'
    )
    vendedor = models.ForeignKey(
        Restaurante,
        related_name='realizada_en',
        on_delete=models.DO_NOTHING,
        blank=False,
        null=False,
        help_text='Restaurante donde se realizó la compra',
        verbose_name='Restaurante'
    )

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'


class Detalle(models.Model):
    unidades = models.IntegerField(
        blank=False,
        null=False,
        validators=[MinValueValidator(1)],
        help_text='Unidades adquiridas del producto',
        verbose_name='Unidades'
    )
    sub_total = models.DecimalField(
        blank=False,
        null=False,
        decimal_places=2,
        max_digits=15,
        validators=[
            MinValueValidator(0.00001),
        ],
        help_text='Este es el monto facturado al adquirir "X" unidades del producto "Y" a "Z" unidades monetarias',
        verbose_name='Sub Total'
    )
    producto = models.ForeignKey(
        Producto,
        on_delete=models.DO_NOTHING,
        related_name='presente_en',
        blank=True,
        null=True,
        help_text='Producto "Y" que ha sido adquirido en "X" unidades a "Z" unidades monetarias',
        verbose_name='Producto'
    )
    compra = models.ForeignKey(
        Compra,
        on_delete=models.CASCADE,
        related_name='detallada_en',
        blank=False,
        null=False,
        help_text='Compra a la que pertenece este detalle',
        verbose_name='Compra'
    )

    def __str__(self):
        return str(self.sub_total)

    class Meta:
        verbose_name = 'Detalle de la Compra',
        verbose_name_plural = 'Detalles de Compra'


class RedSocial(models.Model):
    nombre = models.CharField(
        max_length=20,
        blank=False,
        null=False,
        help_text='Indica el nombre de la reda social',
        verbose_name='Red Social'
    )
    url = models.URLField(
        max_length=100,
        blank=False,
        null=False,
        help_text='Dirección URL de la red social, en el formato: "https://www.redsocial.com"',
        verbose_name='Dirección URL'
    )

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Red Social'
        verbose_name_plural = 'Redes Sociales'


class Perfil(models.Model):
    usuario = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text='Ingrese su nombre de usuario de esta red social'
    )
    url_perfil = models.URLField(
        max_length=100,
        blank=False,
        null=False,
        help_text='Dirección URL de su perfil de la red social, en el formato similar a: "https//www.redsocial.com/miperfil"',
        verbose_name='Dirección URL del perfil'
    )
    red_social = models.ForeignKey(
        RedSocial,
        related_name='red_social',
        on_delete=models.DO_NOTHING,
        blank=False,
        null=False,
        help_text='Seleccione la red social a la que corresponde este perfil',
        verbose_name='Red Social'
    )
    propietario = models.ForeignKey(
        User,
        related_name='es_propiedad_de',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text='Usuario al que le pertenece esta cuenta',
        verbose_name='Propietario'
    )
    restaurante = models.ForeignKey(
        Restaurante,
        related_name='es_administrada_por',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text='Restaurante al que le pertenece esta cuenta',
        verbose_name='Restaurante'
    )

    def __str__(self):
        return self.url_perfil

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'


class Aprobacion(models.Model):
    aprobado = models.BooleanField(
        blank=False,
        null=False,
        help_text='Detalla si el usuario aprueba o no el precio indicado',
        verbose_name='Aprobado'
    )
    usuario = models.ForeignKey(
        User,
        related_name='es_aprobado_por',
        on_delete=models.DO_NOTHING,
        blank=False,
        null=False,
        help_text='Usuario que aprueba o no el precio indicado',
        verbose_name='Usario'
    )
    precio = models.ForeignKey(
        Precio,
        related_name='requiere_de',
        on_delete=models.CASCADE,
        help_text='Precio en discución'
    )

    def __str__(self):
        if self.aprobado:
            return 'Aprobado'
        else:
            return 'Desaprobado'

    class Meta:
        verbose_name = 'Aprobación'
        verbose_name_plural = 'Aprobaciones'
