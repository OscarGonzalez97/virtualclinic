from django import forms
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.contrib.auth.models import Group

from base.models import Usuario
from consultorio.constants import TIPOS_USERS
from consultorio.models import Consultorio, Paciente, Consulta, Laboratorio, TipoEstudio, Estudio


class UsuarioForm(forms.ModelForm):
    consultorio = forms.ModelChoiceField(queryset=Consultorio.objects.all())

    class Meta:
        model = Usuario
        fields = '__all__'


class PacienteForm(forms.ModelForm):

    class Meta:
        model = Paciente
        exclude = ['usuario', 'consultorio', 'nombre_completo']
        widgets = {
            'nombre': forms.TextInput(),
            'apellido': forms.TextInput(),
            'sexo': forms.Select(attrs={'class': 'form-select'}),
            'nro_telefono': forms.TextInput(),
            'nro_documento': forms.TextInput(),
            'fecha_nacimiento': forms.TextInput(
                attrs={'class': 'datepicker'})
        }


class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ('fecha', 'proxima_consulta', 'observacion', 'receta', 'receta_foto')
        widgets = {
            'paciente': forms.HiddenInput(),
            'proxima_consulta': forms.TextInput(attrs={'class': 'datepicker'}),
            'observacion': forms.Textarea(),
            'receta': forms.Textarea(),
            'fecha': forms.TextInput(attrs={'class': 'datepicker'}),

        }


class GeneralEstudioForm(forms.ModelForm):
    tipo_estudio = forms.ModelChoiceField(
        queryset=TipoEstudio.objects.all(),
        widget=forms.Select,
        label='Tipo de estudio'
    )
    laboratorio = forms.ModelChoiceField(
        queryset=Laboratorio.objects.all(),
        widget=forms.Select,
        label='Laboratorio'
    )

    def __init__(self, consultorio, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['paciente'].queryset = consultorio.pacientes.all().order_by('nombre')
        self.fields['tipo_estudio'].queryset = consultorio.tipos_estudios.all().order_by('tipo')
        self.fields['laboratorio'].queryset = consultorio.laboratorios.all().order_by('nombre')

    class Meta:
        model = Estudio
        fields = ('fecha', 'proxima_consulta', 'resultado', 'tipo_estudio', 'laboratorio', 'paciente')
        widgets = {
            'paciente': forms.Select(attrs={'class': 'form-select'}),
            'fecha': forms.TextInput(attrs={'class': 'datepicker'}),
            'proxima_consulta': forms.TextInput(attrs={'class': 'datepicker'}),
            'resultado': forms.FileInput(),
            'tipo_estudio': forms.Select(attrs={'class': 'form-select'}),
            'laboratorio': forms.Select(attrs={'class': 'form-select'}),
        }


class EstudioForm(forms.ModelForm):
    tipo_estudio = forms.ModelChoiceField(
        queryset=TipoEstudio.objects.all(),
        widget=forms.Select,
        label='Tipo de estudio'
    )
    laboratorio = forms.ModelChoiceField(
        queryset=Laboratorio.objects.all(),
        widget=forms.Select,
        label='Laboratorio'
    )

    def __init__(self, consultorio, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['paciente'].queryset = consultorio.pacientes.all().order_by('nombre')
        self.fields['tipo_estudio'].queryset = consultorio.tipos_estudios.all().order_by('tipo')
        self.fields['laboratorio'].queryset = consultorio.laboratorios.all().order_by('nombre')

    class Meta:
        model = Estudio
        fields = ('fecha', 'proxima_consulta', 'resultado', 'tipo_estudio', 'laboratorio', 'paciente')
        widgets = {
            'paciente': forms.HiddenInput(),
            'fecha': forms.TextInput(attrs={'class': 'datepicker'}),
            'proxima_consulta': forms.TextInput(attrs={'class': 'datepicker'}),
            'resultado': forms.FileInput(),
            'tipo_estudio': forms.Select(attrs={'class': 'form-select'}),
            'laboratorio': forms.Select(attrs={'class': 'form-select'}),
        }


class TipoEstudioForm(forms.ModelForm):
    class Meta:
        model = TipoEstudio
        fields = ('tipo', )


class ConsultorioForm(forms.ModelForm):
    class Meta:
        model = Consultorio
        fields = ('ruc', 'email', 'direccion', 'ubicacion', 'telefono', 'telefono_urgencia')


class LaboratorioForm(forms.ModelForm):
    class Meta:
        model = Laboratorio
        fields = ('nombre', 'telefono', 'doctor_encargado', 'direccion')


class UsuarioConsultorioForm(forms.ModelForm):
    grupo = forms.ModelChoiceField(
        queryset=Group.objects.filter(name__in=['Doctor']),
        widget=forms.Select,
        label='Grupo'
    )

    class Meta:
        model = Usuario
        fields = ('first_name', 'last_name', 'email', 'nro_documento', 'nro_telefono', 'grupo', 'direccion', 'username')
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
        }


class UsuarioConsultorioRegisterForm(forms.ModelForm):
    # Define el campo tipo con las opciones filtradas
    tipo = forms.ChoiceField(choices=[(key, value) for key, value in TIPOS_USERS if key != 'paciente'], label='Tipo profesional')

    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'username', 'email', 'nro_documento', 'tipo']
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'username': 'Username',
            'email': 'Email',
            'nro_documento': 'Nro. documento',
        }

    # Campos del consultorio
    nombre_consultorio = forms.CharField(label='Nombre del consultorio', max_length=250)
    ruc = forms.CharField(label='RUC', max_length=20)

    def save(self, commit=True):
        usuario_instance = super().save(commit=False)
        if commit:
            usuario_instance.save()
        return usuario_instance


class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Username'
    }))


class UserSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Nueva Contraseña'
    }), label="Nueva Contraseña")
    new_password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Confirmar Nueva Contraseña'
    }), label="Confirmar Nueva Contraseña")


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Contraseña anterior'
    }), label='Old Password')
    new_password1 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Nueva contraseña'
    }), label="New Password")
    new_password2 = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'placeholder': 'Confirmar nueva contraseña'
    }), label="Confirm New Password")


class ConfirmDeleteForm(forms.Form):
    pass
