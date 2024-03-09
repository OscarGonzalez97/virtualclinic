from django.contrib import admin

from base.models import Usuario
from consultorio.forms import UsuarioForm
from consultorio.models import Consultorio, TipoEstudio, Laboratorio


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    form = UsuarioForm
    list_display = ('username', 'email', 'full_name', 'consultorio')


@admin.register(Consultorio)
class ConsultorioAdmin(admin.ModelAdmin):
    pass


@admin.register(TipoEstudio)
class TipoEstudioAdmin(admin.ModelAdmin):
    pass


@admin.register(Laboratorio)
class LaboratorioAdmin(admin.ModelAdmin):
    pass
