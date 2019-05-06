from django.db import models

class Contacto(models.Model):
    apellidos = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text='Ingrese sus apellidos',
        verbose_name='Apellidos'
    )
    nombre = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text='Ingrese su nombre',
        verbose_name='Nombre'
    )
    email = models.EmailField(
        blank=False,
        null=False,
        help_text='Ingrese su correo electrónico',
        verbose_name='Correo Electrónico'
    )

    def __str__(self):
        return (self.apellidos + ', ' + self.nombre)

    class Meta:
        verbose_name = 'Contacto'
        verbose_name_plural = 'Contactos'

class Motivo(models.Model):
    motivo = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        help_text='Ingrese el motivo de la consulta',
        verbose_name='Motivo de consulta'
    )
    descripcion = models.TextField(
        max_length=200,
        blank=False,
        null=False,
        help_text='Realice una breve descripción del motivo',
        verbose_name='Descripción del motivo'
    )

    def __str__(self):
        return self.motivo

    class Meta:
        verbose_name = 'Motivo de Consulta'
        verbose_name_plural = 'Motivos'

class Consulta(models.Model):
    usuario = models.ForeignKey(
        Contacto,
        on_delete=models.CASCADE,
        help_text='Datos del usuario',
        verbose_name='Usuario'
    )
    tema = models.ForeignKey(
        Motivo,
        on_delete=models.CASCADE,
        help_text='Seleccion un tema relacionado a su consulta',
        verbose_name='Tema de consulta'
    )
    mensaje = models.TextField(
        max_length=500,
        blank=False,
        null=False,
        help_text='Ingrese su mensaje, no olvide detalles relevantes',
        verbose_name='¿En qué podemos ayudarte?'
    )

    def __str__(self):
        return self.mensaje

    class Meta:
        verbose_name = 'Consulta'
        verbose_name_plural = 'Consultas'

