from operator import itemgetter

from admin_material.forms import LoginForm
from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail, EmailMultiAlternatives
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from base.models import Usuario
from consultorio.forms import PacienteForm, ConfirmDeleteForm, ConsultaForm, EstudioForm, GeneralEstudioForm, \
    TipoEstudioForm, LaboratorioForm, UserPasswordResetForm, UserSetPasswordForm, ConsultorioForm, \
    UserPasswordChangeForm, UsuarioConsultorioForm, UsuarioConsultorioRegisterForm
from consultorio.models import Paciente, Consulta, Estudio, TipoEstudio, Laboratorio, Consultorio, ArchivoConsulta


def is_doc_or_admin(user):
    return user.groups.filter(name__in=['Doctor', 'Administrador']).exists()


@user_passes_test(is_doc_or_admin)
def dashboard_view(request):
    cantidad_estudios = 0
    fecha_actual = timezone.now().date()
    proximas_consultas = Consulta.objects.filter(proxima_consulta__gt=fecha_actual)
    proximos_estudios = Estudio.objects.filter(proxima_consulta__gt=fecha_actual)
    consultorio = request.user.consultorio

    proximos_eventos = []

    for consulta in proximas_consultas:
        proximos_eventos.append({
            'fecha': consulta.proxima_consulta,
            'trabajo': 'Consulta',
            'paciente': consulta.paciente.nombre,
            'telefono': consulta.paciente.nro_telefono,
        })
    for estudio in proximos_estudios:
        proximos_eventos.append({
            'fecha': estudio.proxima_consulta,
            'trabajo': 'Estudio',
            'paciente': estudio.paciente.nombre,
            'telefono': estudio.paciente.nro_telefono,
        })

    proximos_eventos = sorted(
        proximos_eventos,
        key=itemgetter('fecha')
    )

    for paciente in Paciente.objects.filter(consultorio=consultorio):
        cantidad_estudios += paciente.estudios_totales()

    context = {
        'segment': 'inicio',
        'pacientes_total': Paciente.objects.filter(consultorio=consultorio).count(),
        'usuarios': consultorio.usuarios.count(),
        'estudios': cantidad_estudios,
        'notificaciones': proximos_eventos,
        'consultorio': consultorio
    }
    return render(request, 'consultorio/dashboard.html', context)


class ClienteList(PermissionRequiredMixin, ListView):
    model = Consulta
    template_name = 'consultorio/dashboard-cliente.html'
    context_object_name = 'consultas'
    permission_required = 'consultorio.list_consulta'

    def get_queryset(self):
        return self.request.user.paciente.consultas.order_by('-fecha')


# ------------------ Seccion Cliente ----------------------

class ClienteEstudioList(PermissionRequiredMixin, ListView):
    model = Estudio
    template_name = 'consultorio/cliente/estudio/list.html'
    context_object_name = 'estudios'
    permission_required = 'consultorio.list_estudio'

    def get_queryset(self):
        return Estudio.objects.filter(paciente=self.request.user.paciente).order_by('-fecha')


# ------------------ Fin Seccion Cliente ----------------------


class CreateMixin:
    def form_valid(self, form):
        form.instance.creado_por = self.request.user
        return super().form_valid(form)


class UpdateMixin:
    def form_valid(self, form):
        form.instance.actualizado_por = self.request.user
        return super().form_valid(form)


# ------------------ Seccion Consultorio ----------------------


class ConsultorioDetail(PermissionRequiredMixin, DetailView):
    permission_required = 'consultorio.view_consultorio'
    model = Consultorio
    template_name = 'consultorio/consultorio/detail.html'
    context_object_name = 'consultorio'

    def get_object(self, queryset=None):
        return self.request.user.consultorio


class ConsultorioUpdate(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Consultorio
    form_class = ConsultorioForm
    success_url = reverse_lazy('consultorio')
    permission_required = 'consultorio.change_consultorio'
    template_name = 'consultorio/consultorio/update.html'
    success_message = "El consultorio se ha actualizado correctamente."

    def get_object(self, queryset=None):
        return self.request.user.consultorio


# ------------------- Fin Seccion Consultorio -------------------


# ------------------ Seccion Tipo Analisis ----------------------


class TipoEstudioList(PermissionRequiredMixin, ListView):
    model = TipoEstudio
    template_name = 'consultorio/tipoestudio/list.html'
    context_object_name = 'tipoestudios'
    permission_required = 'consultorio.list_tipoestudio'
    ordering = 'tipo'

    def get_queryset(self):
        return self.request.user.consultorio.tipos_estudios.all().order_by('tipo')


class TipoEstudioCreateOrUpdateMixin:
    model = TipoEstudio
    form_class = TipoEstudioForm
    template_name = 'consultorio/tipoestudio/add.html'
    success_url = reverse_lazy('tipoestudio')

    def form_valid(self, form):
        form.instance.consultorio = self.request.user.consultorio
        return super().form_valid(form)


class TipoEstudioCreate(PermissionRequiredMixin, TipoEstudioCreateOrUpdateMixin, SuccessMessageMixin, CreateView):
    permission_required = 'consultorio.add_tipoestudio'
    success_message = "El tipo estudio se ha guardado correctamente."


class TipoEstudioUpdate(PermissionRequiredMixin, TipoEstudioCreateOrUpdateMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'consultorio.change_tipoestudio'
    success_message = "El tipo estudio se ha actualizado correctamente."
    pk_url_kwarg = 'tipoestudio_id'


class TipoEstudioDelete(SuccessMessageMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'consultorio.delete_tipoestudio'
    template_name = 'consultorio/tipoestudio/delete.html'
    success_message = "El tipo estudio se ha eliminado correctamente."
    success_url = reverse_lazy('tipoestudio')

    def get_object(self, queryset=None):
        return TipoEstudio.objects.get(id=self.kwargs['tipoestudio_id'])

    def get(self, request, *args, **kwargs):
        tipoestudio = self.get_object()
        confirm_delete_form = ConfirmDeleteForm(initial={'tipoestudio_id': tipoestudio.id})

        context = {
            'object': tipoestudio,
            'confirm_delete_form': confirm_delete_form,
        }
        return render(request, self.template_name, context)

    def form_valid(self, form):
        success_url = self.get_success_url()
        estudios_relacionados = Estudio.objects.filter(tipo_estudio=self.object)

        if estudios_relacionados.exists():
            messages.success(self.request, "Existen Estudios con este tipo de estudio")
            return redirect(reverse('tipoestudio-delete', kwargs={'tipoestudio_id': self.object.pk}))
        else:
            messages.success(self.request, self.success_message)
        self.object.delete()
        return redirect(success_url)


# ------------------ Fin Seccion  Tipo Analisis ------------------

# ------------------ Seccion Laboratorios ----------------------


class LaboratorioList(PermissionRequiredMixin, ListView):
    model = Laboratorio
    template_name = 'consultorio/laboratorio/list.html'
    context_object_name = 'laboratorios'
    permission_required = 'consultorio.list_laboratorio'
    ordering = 'nombre'

    def get_queryset(self):
        return self.request.user.consultorio.laboratorios.all().order_by('nombre')


class LaboratorioCreateOrUpdateMixin:
    model = Laboratorio
    form_class = LaboratorioForm
    template_name = 'consultorio/laboratorio/add.html'
    success_url = reverse_lazy('laboratorios')

    def form_valid(self, form):
        form.instance.consultorio = self.request.user.consultorio
        return super().form_valid(form)


class LaboratorioCreate(PermissionRequiredMixin, LaboratorioCreateOrUpdateMixin, SuccessMessageMixin, CreateView):
    permission_required = 'consultorio.add_laboratorio'
    success_message = "El laboratorio se ha guardado correctamente."


class LaboratorioUpdate(PermissionRequiredMixin, LaboratorioCreateOrUpdateMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'consultorio.change_laboratorio'
    success_message = "El laboratorio se ha actualizado correctamente."
    pk_url_kwarg = 'laboratorio_id'


class LaboratorioDelete(SuccessMessageMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'consultorio.delete_laboratorio'
    template_name = 'consultorio/laboratorio/delete.html'
    success_message = "El laboratorio se ha eliminado correctamente."
    success_url = reverse_lazy('laboratorios')

    def get_object(self, queryset=None):
        return Laboratorio.objects.get(id=self.kwargs['laboratorio_id'])

    def get(self, request, *args, **kwargs):
        laboratorio = self.get_object()
        confirm_delete_form = ConfirmDeleteForm(initial={'laboratorio_id': laboratorio.id})

        context = {
            'object': laboratorio,
            'confirm_delete_form': confirm_delete_form,
        }
        return render(request, self.template_name, context)


# ------------------ Fin Seccion Laboratorio ------------------


# ------------------ Seccion Usuarios Admin Consultorio ----------------------


class UsuarioList(PermissionRequiredMixin, ListView):
    model = Usuario
    template_name = 'consultorio/usuario/list.html'
    context_object_name = 'usuarios'
    permission_required = 'base.list_usuario'

    def get_queryset(self):
        consultorio = self.request.user.consultorio
        return consultorio.usuarios.all().order_by('full_name')


class UserPasswordResetView(PasswordResetView):
    template_name = 'consultorio/usuario/password_reset.html'
    form_class = UserPasswordResetForm


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'consultorio/usuario/password_reset_confirm.html'
    form_class = UserSetPasswordForm
    success_url = reverse_lazy("password-reset-complete")


class UserPasswordChangeView(PasswordChangeView):
    template_name = 'consultorio/usuario/password_change.html'
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("password-change-done")


class UsuarioCreateOrUpdateMixin:
    model = Usuario
    form_class = UsuarioConsultorioForm
    template_name = 'consultorio/usuario/add.html'
    success_url = reverse_lazy('usuarios')


class UsuarioCreate(PermissionRequiredMixin, UsuarioCreateOrUpdateMixin, SuccessMessageMixin, CreateView):
    permission_required = 'base.add_usuario'
    success_message = "El usuario se ha guardado correctamente."

    def form_valid(self, form):
        form.instance.consultorio = self.request.user.consultorio
        user = form.save()

        grupo = form.cleaned_data['grupo']
        form.instance.groups.add(grupo)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_url = reverse_lazy('password-reset-confirm', kwargs={'uidb64': uid, 'token': token})

        # Enviar un correo electrónico con el enlace de restablecimiento de contraseña
        subject = 'Establecimiento de contraseña'
        message = f'Bienvenido a Virtualclinic señor/a {user.full_name}\n.Haga clic en el siguiente enlace para establecer su contraseña: {self.request.build_absolute_uri(reset_url)}'
        from_email = 'noreply@virtualclinic.com.py'
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        return super().form_valid(form)


class UsuarioPacienteCreate(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'base.add_usuario'
    model = Usuario
    fields = ['first_name', 'last_name', 'nro_documento', 'nro_telefono', 'email', 'username']
    success_message = "El usuario se ha guardado correctamente."
    success_url = reverse_lazy('pacientes')

    def form_invalid(self, form):
        if form.errors:
            messages.error(self.request, 'El username ya existe')
            return super().form_invalid(form)
        return super().form_invalid(form)

    def form_valid(self, form):
        form.instance.consultorio = self.request.user.consultorio
        form.instance.tipo = 'paciente'
        user = form.save()
        paciente = Paciente.objects.get(pk=form.data['paciente_id'])
        paciente.usuario = user
        paciente.save()

        grupo = Group.objects.filter(name='Cliente').first()
        form.instance.groups.add(grupo)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_url = reverse_lazy('password-reset-confirm', kwargs={'uidb64': uid, 'token': token})

        # Enviar un correo electrónico con el enlace de restablecimiento de contraseña
        html_content = render_to_string('consultorio/email_usuario.html', {'user': user, 'reset_url': reset_url})

        # Crear el correo electrónico
        subject = 'Bienvenido a Virtualclinic - Establecimiento de contraseña'
        from_email = 'noreply@virtualclinic.com.py'
        to_email = user.email

        # Obtener el texto plano del contenido HTML
        text_content = strip_tags(html_content)

        # Crear el mensaje de correo electrónico
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        msg.attach_alternative(html_content, "text/html")

        # Enviar el correo electrónico
        msg.send(fail_silently=False)

        return super().form_valid(form)


class UserRegisterView(SuccessMessageMixin, CreateView):
    model = Usuario
    form_class = UsuarioConsultorioRegisterForm
    template_name = 'consultorio/usuario/register.html'
    success_url = reverse_lazy('user_login')
    success_message = "Te registraste! Revisa tu mail para los siguientes pasos."

    def form_valid(self, form):
        user = form.save(commit=False)
        consultorio_data = {
            'nombre': form.cleaned_data['nombre_consultorio'],
            'ruc': form.cleaned_data['ruc'],
        }
        consultorio_instance = Consultorio.objects.create(**consultorio_data)
        form.instance.consultorio = consultorio_instance
        form.instance.is_active = False
        form.save()
        form.instance.groups.add(Group.objects.filter(name='Administrador').first())

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_url = reverse_lazy('password-reset-confirm', kwargs={'uidb64': uid, 'token': token})

        # Enviar un correo electrónico con el enlace de restablecimiento de contraseña
        html_content = render_to_string('consultorio/email.html', {'user': user, 'reset_url': reset_url})

        # Crear el correo electrónico
        subject = 'Bienvenido a Virtualclinic - Establecimiento de contraseña'
        from_email = 'noreply@virtualclinic.com.py'
        to_email = user.email

        # Obtener el texto plano del contenido HTML
        text_content = strip_tags(html_content)

        # Crear el mensaje de correo electrónico
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        msg.attach_alternative(html_content, "text/html")

        # Enviar el correo electrónico
        msg.send(fail_silently=False)

        return super().form_valid(form)


class UsuarioUpdate(PermissionRequiredMixin, UsuarioCreateOrUpdateMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'base.change_usuario'
    success_message = "El usuario se ha actualizado correctamente."
    pk_url_kwarg = 'usuario_id'

    def form_valid(self, form):
        grupo = form.cleaned_data['grupo']
        form.instance.groups.clear()
        form.instance.groups.add(grupo)
        return super().form_valid(form)

    def get_object(self, queryset=None):
        consultorio = self.request.user.consultorio
        try:
            return Usuario.objects.get(id=self.kwargs['usuario_id'], consultorio=consultorio)
        except Usuario.DoesNotExist:
            raise Http404("No se encontró un Usuario con los criterios especificados.")


class UsuarioDelete(SuccessMessageMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'base.delete_usuario'
    template_name = 'consultorio/usuario/delete.html'
    success_message = "El usuario se ha eliminado correctamente."
    success_url = reverse_lazy('usuarios')

    def get_object(self, queryset=None):
        consultorio = self.request.user.consultorio
        try:
            return Usuario.objects.get(id=self.kwargs['usuario_id'], consultorio=consultorio)
        except Usuario.DoesNotExist:
            raise Http404("No se encontró un Usuario con los criterios especificados.")

    def get(self, request, *args, **kwargs):
        usuario = self.get_object()
        confirm_delete_form = ConfirmDeleteForm(initial={'usuario_id': usuario.id})

        context = {
            'object': usuario,
            'confirm_delete_form': confirm_delete_form,
        }
        return render(request, self.template_name, context)


# ------------------ Fin Usuarios Admin consultorio ------------------


# ------------------ Seccion Estudio ----------------------


class EstudioList(PermissionRequiredMixin, ListView):
    model = Estudio
    template_name = 'consultorio/estudio/list.html'
    context_object_name = 'estudio'
    permission_required = 'consultorio.list_estudio'

    def get_queryset(self):
        consultorio = self.request.user.consultorio
        return Estudio.objects.filter(paciente__consultorio=consultorio).order_by('-fecha')


class EstudioCreateOrUpdateMixin:
    model = Estudio
    form_class = GeneralEstudioForm
    template_name = 'consultorio/estudio/add.html'
    success_url = reverse_lazy('estudio')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['consultorio'] = self.request.user.consultorio
        return kwargs


class EstudioCreate(PermissionRequiredMixin, EstudioCreateOrUpdateMixin, SuccessMessageMixin, CreateView):
    permission_required = 'consultorio.add_estudio'
    success_message = "El estudio del paciente se ha guardado correctamente."


class EstudioUpdate(PermissionRequiredMixin, EstudioCreateOrUpdateMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'consultorio.change_estudio'
    success_message = "El estudio del paciente se ha actualizado correctamente."

    def get_object(self, queryset=None):
        consultorio = self.request.user.consultorio
        return Estudio.objects.get(id=self.kwargs['estudio_id'], paciente__consultorio=consultorio)


class EstudioDelete(SuccessMessageMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'consultorio.delete_estudio'
    template_name = 'consultorio/estudio/delete.html'
    success_message = "El estudio se ha eliminado correctamente."
    success_url = reverse_lazy('estudio')

    def get_object(self, queryset=None):
        consultorio = self.request.user.consultorio
        return Estudio.objects.get(id=self.kwargs['estudio_id'], paciente__consultorio=consultorio)

    def get(self, request, *args, **kwargs):
        estudio = self.get_object()
        confirm_delete_form = ConfirmDeleteForm(initial={'estudio_id': estudio.id})

        context = {
            'object': estudio,
            'confirm_delete_form': confirm_delete_form,
        }
        return render(request, self.template_name, context)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return redirect(success_url)


# ------------------ Fin Seccion Estudio -----------------


# ------------------ Seccion Pacientes ---------------------


class PacientesList(PermissionRequiredMixin, ListView):
    model = Paciente
    template_name = 'consultorio/paciente/list.html'
    context_object_name = 'pacientes'
    permission_required = 'consultorio.list_paciente'

    def get_queryset(self):
        consultorio = self.request.user.consultorio
        return Paciente.objects.filter(consultorio=consultorio).order_by('nombre')


class PacienteCreateOrUpdateMixin:
    model = Paciente
    form_class = PacienteForm
    template_name = 'consultorio/paciente/add.html'
    success_url = reverse_lazy('pacientes')

    def form_valid(self, form):
        form.instance.consultorio = self.request.user.consultorio
        return super().form_valid(form)


class PacienteCreate(PacienteCreateOrUpdateMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'consultorio.add_paciente'
    success_message = "El paciente se ha guardado correctamente."


class PacienteUpdate(PacienteCreateOrUpdateMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'consultorio.change_paciente'
    success_message = "El paciente se ha actualizado correctamente."

    def get_object(self, queryset=None):
        consultorio = self.request.user.consultorio
        try:
            return Paciente.objects.get(id=self.kwargs['paciente_id'], consultorio=consultorio)
        except Paciente.DoesNotExist:
            raise Http404("No se encontró un paciente con los criterios especificados.")


class PacienteDelete(SuccessMessageMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'consultorio.delete_paciente'
    template_name = 'consultorio/paciente/delete.html'
    success_message = "El paciente se ha eliminado correctamente."
    success_url = reverse_lazy('pacientes')

    def get_object(self, queryset=None):
        paciente_id = self.kwargs.get('paciente_id')
        consultorio = self.request.user.consultorio
        try:
            return Paciente.objects.get(id=paciente_id, consultorio=consultorio)
        except Paciente.DoesNotExist:
            raise Http404("No se encontró un paciente con los criterios especificados.")

    def get(self, request, *args, **kwargs):
        paciente = self.get_object()
        confirm_delete_form = ConfirmDeleteForm(initial={'paciente_id': paciente.id})

        context = {
            'object': paciente,
            'confirm_delete_form': confirm_delete_form,
        }

        return render(request, self.template_name, context)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return redirect(success_url)


def get_paciente(self):
    paciente_id = self.kwargs.get('paciente_id')
    consultorio = self.request.user.consultorio
    try:
        paciente = Paciente.objects.get(id=paciente_id, consultorio=consultorio)
    except Paciente.DoesNotExist:
        raise Http404("No se encontró un paciente con los criterios especificados.")
    return paciente


class PacienteDetail(PermissionRequiredMixin, DetailView):
    permission_required = 'consultorio.view_paciente'
    model = Paciente
    template_name = 'consultorio/paciente/detail.html'
    context_object_name = 'paciente'

    def get_object(self, queryset=None):
        paciente = get_paciente(self)
        return paciente

    def get_context_data(self, **kwargs):
        context = super(PacienteDetail, self).get_context_data()
        context['consultas'] = context['paciente'].consultas.all().order_by('-fecha')
        return context


class PacienteConsultaList(PermissionRequiredMixin, ListView):
    model = Consulta
    template_name = 'consultorio/paciente/consulta/list.html'
    context_object_name = 'consultas'
    permission_required = ('consultorio.view_paciente', 'consultorio.list_consulta')

    def get_context_data(self, **kwargs):
        context = super(PacienteConsultaList, self).get_context_data()
        paciente = get_paciente(self)
        context['paciente'] = paciente
        return context

    def get_queryset(self):
        paciente = get_paciente(self)
        return Consulta.objects.filter(paciente=paciente).order_by('-fecha')


class PacienteConsultaCreateOrUpdateMixin:
    model = Consulta
    form_class = ConsultaForm
    template_name = 'consultorio/paciente/consulta/add.html'

    def form_valid(self, form):
        retorno = super().form_valid(form)
        files = form.cleaned_data['archivos']
        for f in files:
            archivo_consulta = {
                'archivo': f,
                'consulta': form.instance
            }
            ArchivoConsulta.objects.create(**archivo_consulta)
        return retorno

    def get_success_url(self):
        return reverse('paciente-consultas', args=[self.kwargs.get('paciente_id')])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        paciente = get_paciente(self)
        kwargs['initial'] = {'paciente': paciente}
        return kwargs


class PacienteConsultaCreate(PermissionRequiredMixin, PacienteConsultaCreateOrUpdateMixin, SuccessMessageMixin,
                             CreateMixin, CreateView):
    permission_required = ('consultorio.view_paciente', 'consultorio.add_consulta')
    success_message = "La consulta del paciente se ha guardado correctamente."

    def get_context_data(self, **kwargs):
        context = super(PacienteConsultaCreate, self).get_context_data()
        paciente = get_paciente(self)
        context['paciente'] = paciente
        return context


class PacienteConsultaDetail(PermissionRequiredMixin, DetailView):
    permission_required = 'consultorio.view_consulta'
    model = Consulta
    template_name = 'consultorio/paciente/consulta/detail.html'
    context_object_name = 'consulta'
    pk_url_kwarg = 'consulta_id'

    def get_context_data(self, **kwargs):
        context = super(PacienteConsultaDetail, self).get_context_data()
        context['paciente'] = get_paciente(self)
        return context


class PacienteConsultaUpdate(PermissionRequiredMixin, PacienteConsultaCreateOrUpdateMixin, SuccessMessageMixin,
                             UpdateMixin, UpdateView):
    permission_required = ('consultorio.view_paciente', 'consultorio.change_consulta')
    success_message = "La consulta del paciente se ha actualizado correctamente."

    def get_context_data(self, **kwargs):
        context = super(PacienteConsultaUpdate, self).get_context_data()
        paciente = get_paciente(self)
        context['paciente'] = paciente
        return context

    def get_object(self, queryset=None):
        consultorio = self.request.user.consultorio
        return Consulta.objects.get(id=self.kwargs['consulta_id'], paciente__consultorio=consultorio)


class ArchivoConsultaDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('consultorio.view_paciente', 'consultorio.delete_consulta')
    model = ArchivoConsulta
    success_message = "El archivo se ha eliminado correctamente."

    def get_object(self, queryset=None):
        consultorio = self.request.user.consultorio
        return ArchivoConsulta.objects.get(id=self.kwargs['archivo_id'], consulta__paciente__consultorio=consultorio)

    def get_success_url(self):
        return reverse('paciente-consulta-edit', args=[self.kwargs.get('paciente_id'), self.kwargs.get('consulta_id')])


class PacienteConsultaDelete(SuccessMessageMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('consultorio.view_paciente', 'consultorio.delete_consulta')
    template_name = 'consultorio/paciente/consulta/delete.html'
    success_message = "La consulta se ha eliminado correctamente."

    def get_object(self, queryset=None):
        consultorio = self.request.user.consultorio
        return Consulta.objects.get(id=self.kwargs['consulta_id'], paciente__consultorio=consultorio)

    def get_success_url(self):
        return reverse('paciente-consultas', args=[self.kwargs.get('paciente_id')])

    def get(self, request, *args, **kwargs):
        consulta = self.get_object()
        confirm_delete_form = ConfirmDeleteForm(initial={'consulta_id': consulta.id})
        paciente = get_paciente(self)

        context = {
            'object': consulta,
            'paciente': paciente,
            'confirm_delete_form': confirm_delete_form,
        }

        return render(request, self.template_name, context)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return redirect(success_url)


class PacienteEstudioList(PermissionRequiredMixin, ListView):
    model = Estudio
    template_name = 'consultorio/paciente/estudio/list.html'
    context_object_name = 'estudios'
    permission_required = ('consultorio.view_paciente', 'consultorio.list_estudio')

    def get_context_data(self, **kwargs):
        context = super(PacienteEstudioList, self).get_context_data()
        paciente = get_paciente(self)
        context['paciente'] = paciente
        return context

    def get_queryset(self):
        paciente = get_paciente(self)
        return Estudio.objects.filter(paciente=paciente).order_by('-fecha')


class PacienteEstudioCreateOrUpdateMixin:
    model = Estudio
    form_class = EstudioForm
    template_name = 'consultorio/paciente/estudio/add.html'

    def get_success_url(self):
        return reverse('paciente-estudio', args=[self.kwargs.get('paciente_id')])

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        paciente = get_paciente(self)
        kwargs['initial'] = {'paciente': paciente}
        kwargs['consultorio'] = self.request.user.consultorio
        return kwargs


class PacienteEstudioCreate(PermissionRequiredMixin, PacienteEstudioCreateOrUpdateMixin, SuccessMessageMixin,
                            CreateMixin, CreateView):
    permission_required = ('consultorio.view_paciente', 'consultorio.add_estudio')
    success_message = "El estudio del paciente se ha guardado correctamente."

    def get_context_data(self, **kwargs):
        context = super(PacienteEstudioCreate, self).get_context_data()
        paciente = get_paciente(self)
        context['paciente'] = paciente
        return context


class PacienteEstudioUpdate(PermissionRequiredMixin, PacienteEstudioCreateOrUpdateMixin, SuccessMessageMixin,
                            UpdateMixin, UpdateView):
    permission_required = ('consultorio.view_paciente', 'consultorio.change_estudio')
    success_message = "El estudio del paciente se ha actualizado correctamente."

    def get_context_data(self, **kwargs):
        context = super(PacienteEstudioUpdate, self).get_context_data()
        paciente = get_paciente(self)
        context['paciente'] = paciente
        return context

    def get_object(self, queryset=None):
        consultorio = self.request.user.consultorio
        return Estudio.objects.get(id=self.kwargs['estudio_id'], paciente__consultorio=consultorio)


class PacienteEstudioDelete(SuccessMessageMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('consultorio.view_paciente', 'consultorio.delete_estudio')
    template_name = 'consultorio/paciente/estudio/delete.html'
    success_message = "El estudio se ha eliminado correctamente."

    def get_object(self, queryset=None):
        consultorio = self.request.user.consultorio
        return Estudio.objects.get(id=self.kwargs['estudio_id'], paciente__consultorio=consultorio)

    def get_success_url(self):
        return reverse('paciente-estudio', args=[self.kwargs.get('paciente_id')])

    def get(self, request, *args, **kwargs):
        estudio = self.get_object()
        confirm_delete_form = ConfirmDeleteForm(initial={'estudio_id': estudio.id})
        paciente_id = self.kwargs.get('paciente_id')
        paciente = get_object_or_404(Paciente, id=paciente_id)

        context = {
            'object': estudio,
            'paciente': paciente,
            'confirm_delete_form': confirm_delete_form,
        }

        return render(request, self.template_name, context)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return redirect(success_url)


# ------------------ Seccion Pacientes ---------------------


def auth_login(request, param):
    pass


class UserLoginView(LoginView):
    template_name = 'consultorio/login.html'
    form_class = LoginForm

    def form_invalid(self, form):
        if form.errors:
            messages.error(self.request,
                           'Tu cuenta está inactiva o ingresaste mal tu contraseña. Por favor, registrate o revisa tu correo electrónico para más instrucciones.')
            return super().form_invalid(form)
        return super().form_invalid(form)

    def form_valid(self, form):
        self.user = form.get_user()
        if self.user.groups.filter(name__in=['Doctor', 'Administrador']).exists():
            login(self.request, self.user)
            return redirect('dashboard')
        elif self.user.groups.filter(name__in=['Cliente']).exists():
            login(self.request, self.user)
            return redirect('dashboard-cliente')
        else:
            form.add_error(None, "No tienes permiso para acceder a esta vista.")
            return self.form_invalid(form)


def logout_view(request):
    logout(request)
    return redirect('/clinicadmin/login/')
