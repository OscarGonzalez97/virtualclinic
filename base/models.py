from django.contrib.auth.models import AbstractUser
from django.db import models

from consultorio.constants import TIPOS_USERS


class Usuario(AbstractUser):

    full_name = models.CharField('Nombre y Apellido', max_length=200, blank=True)
    nro_documento = models.CharField('Número de documento', max_length=80, null=True, blank=True)
    tipo = models.CharField(max_length=30, choices=TIPOS_USERS)
    consultorio = models.ForeignKey('consultorio.Consultorio', related_name='usuarios', null=True, blank=True,
                                    on_delete=models.SET_NULL)
    direccion = models.TextField('Dirección', null=True, blank=True)
    nro_telefono = models.CharField('Número de teléfono', max_length=80, null=True, blank=True)

    class Meta:
        ordering = ['-is_active', 'username']

    def __str__(self):
        if not self.full_name:
            return self.first_name + ' ' + self.last_name
        return self.full_name

    def save(self, *args, **kwargs):
        self.full_name = self.first_name + ' ' + self.last_name
        super().save(*args, **kwargs)
