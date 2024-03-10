from django.db import models
from django.utils import timezone

from base.models import Usuario
from consultorio.constants import SEX


class Consultorio(models.Model):
    nombre = models.CharField(max_length=250)
    ruc = models.CharField(max_length=20, null=True, blank=True)
    razon_social = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    direccion = models.TextField('Dirección', null=True, blank=True)
    ubicacion = models.URLField('Ubicación maps', null=True, blank=True)
    telefono = models.CharField('Número de teléfono', max_length=80, null=True, blank=True)
    telefono_urgencia = models.CharField('Teléfono urgencia', max_length=80, null=True, blank=True)

    def __str__(self):
        return self.nombre


class Paciente(models.Model):
    nombre = models.CharField('Nombre', max_length=50)
    apellido = models.CharField('Apellido', max_length=50)
    nombre_completo = models.CharField('Nombre y apellido', max_length=100)
    sexo = models.CharField(max_length=12, choices=SEX)
    fecha_nacimiento = models.DateField('Fecha de nacimiento', null=True, blank=True)
    nro_telefono = models.CharField('Número de teléfono', max_length=80, null=True, blank=True)
    email = models.EmailField('Email', blank=True, null=True)
    consultorio = models.ForeignKey(Consultorio, related_name='pacientes', null=True, blank=True,
                                    on_delete=models.SET_NULL)
    usuario = models.OneToOneField(Usuario, related_name='usuario', null=True, blank=True, on_delete=models.SET_NULL)
    nro_documento = models.CharField('Número de documento', max_length=80, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre_completo}".strip()

    def estudios_totales(self):
        total_estudios = 0
        for estudio in self.estudios.all():
            total_estudios += 1
        return total_estudios

    def save(self, *args, **kwargs):
        self.nombre_completo = self.nombre + ' ' + self.apellido
        super().save(*args, **kwargs)


class Consulta(models.Model):
    fecha = models.DateTimeField(default=timezone.now)
    observacion = models.TextField('Observación', null=True, blank=True)
    proxima_consulta = models.DateTimeField('Próxima consulta', null=True, blank=True)
    receta = models.TextField('Receta', null=True, blank=True)
    receta_foto = models.ImageField('Receta Foto', null=True, blank=True)
    paciente = models.ForeignKey(Paciente, related_name='consultas', on_delete=models.CASCADE)
    creado_por = models.ForeignKey(Usuario, related_name='consultas_creados', on_delete=models.SET_NULL,
                                   null=True, blank=True)
    actualizado_por = models.ForeignKey(Usuario, related_name='consultas_actualizados', on_delete=models.SET_NULL,
                                        null=True, blank=True)

    def __str__(self):
        return str(self.fecha) + ' ' + str(self.paciente)


class ArchivoConsulta(models.Model):
    consulta = models.ForeignKey(Consulta, related_name='archivos', on_delete=models.CASCADE)
    archivo = models.FileField()

    def __str__(self):
        return str(self.archivo)


class TipoEstudio(models.Model):
    tipo = models.CharField('Tipo de estudio', max_length=200)
    consultorio = models.ForeignKey(Consultorio, related_name='tipos_estudios', null=True, blank=True,
                                    on_delete=models.SET_NULL)

    def __str__(self):
        return self.tipo


class Laboratorio(models.Model):
    nombre = models.CharField('Nombre laboratorio', max_length=250)
    direccion = models.TextField('Dirección', null=True, blank=True)
    telefono = models.CharField('Número de teléfono', max_length=80, null=True, blank=True)
    doctor_encargado = models.CharField('Nombre encargado', max_length=100, null=True, blank=True)
    consultorio = models.ForeignKey(Consultorio, related_name='laboratorios', null=True, blank=True,
                                    on_delete=models.SET_NULL)

    def __str__(self):
        return self.nombre


class Estudio(models.Model):
    fecha = models.DateTimeField('Fecha estudio', default=timezone.now)
    proxima_consulta = models.DateTimeField(null=True, blank=True)
    notificado = models.BooleanField(default=False)
    resultado = models.FileField(null=True, blank=True)
    paciente = models.ForeignKey(Paciente, related_name='estudios', on_delete=models.CASCADE)
    tipo_estudio = models.ForeignKey(TipoEstudio, related_name='estudios', on_delete=models.PROTECT)
    laboratorio = models.ForeignKey(Laboratorio, related_name='estudios', null=True, blank=True, on_delete=models.SET_NULL)
    creado_por = models.ForeignKey(Usuario, related_name='estudios_creados', on_delete=models.SET_NULL,
                                   null=True, blank=True)
    actualizado_por = models.ForeignKey(Usuario, related_name='estudios_actualizados', on_delete=models.SET_NULL,
                                        null=True, blank=True)

    def __str__(self):
        return str(self.fecha) + ' ' + str(self.tipo_estudio) + ' ' + str(self.paciente)
