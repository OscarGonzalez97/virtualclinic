from django.urls import path, include
from django.contrib.auth import views as auth_views

from consultorio import views

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('logout/', views.logout_view, name='logout_user'),
    path('', views.dashboard_view, name='dashboard'),
    path('cliente/', include([
        path('', views.ClienteList.as_view(), name='dashboard-cliente'),
        path('estudios', views.ClienteEstudioList.as_view(), name='estudios-cliente'),
    ])),
    path('consultorio/', include([
        path('', views.ConsultorioDetail.as_view(), name='consultorio'),
        path('update/', views.ConsultorioUpdate.as_view(), name='consultorio-edit'),
    ])),
    path('estudio/', include([
        path('', views.EstudioList.as_view(), name='estudio'),
        path('create/', views.EstudioCreate.as_view(), name='estudio-create'),
        path('<int:estudio_id>/', include([
            path('edit/', views.EstudioUpdate.as_view(), name='estudio-edit'),
            path('delete/', views.EstudioDelete.as_view(), name='estudio-delete'),
        ])),
    ])),
    path('usuarios/', include([
        path('confirmar-reset-password/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(),
             name='password-reset-confirm'),
        path('completado-reset-password/', auth_views.PasswordResetCompleteView.as_view(
                template_name='consultorio/usuario/password_reset_complete.html'
            ), name='password-reset-complete'),
        path('change-password/', views.UserPasswordChangeView.as_view(), name='cambiar-pass'),
        path('password-change-done/', auth_views.PasswordChangeDoneView.as_view(
            template_name='consultorio/usuario/password_change_done.html'
        ), name="password-change-done"),
        path('', views.UsuarioList.as_view(), name='usuarios'),
        path('create/', views.UsuarioCreate.as_view(), name='usuarioconsultorio-create'),
        path('<int:usuario_id>/', include([
            path('edit/', views.UsuarioUpdate.as_view(), name='usuarioconsultorio-edit'),
            path('delete/', views.UsuarioDelete.as_view(), name='usuarioconsultorio-delete'),
        ])),
    ])),
    path('tipoestudio/', include([
        path('', views.TipoEstudioList.as_view(), name='tipoestudio'),
        path('create/', views.TipoEstudioCreate.as_view(), name='tipoestudio-create'),
        path('<int:tipoestudio_id>/', include([
            path('edit/', views.TipoEstudioUpdate.as_view(), name='tipoestudio-edit'),
            path('delete/', views.TipoEstudioDelete.as_view(), name='tipoestudio-delete'),
        ])),
    ])),
    path('laboratorios/', include([
        path('', views.LaboratorioList.as_view(), name='laboratorios'),
        path('create/', views.LaboratorioCreate.as_view(), name='laboratorio-create'),
        path('<int:laboratorio_id>/', include([
            path('edit/', views.LaboratorioUpdate.as_view(), name='laboratorio-edit'),
            path('delete/', views.LaboratorioDelete.as_view(), name='laboratorio-delete'),
        ])),
    ])),
    path('pacientes/', include([
        path('', views.PacientesList.as_view(), name='pacientes'),
        path('create/', views.PacienteCreate.as_view(), name='paciente-create'),
        path('<int:paciente_id>/', include([
            path('', views.PacienteDetail.as_view(), name='paciente'),
            path('edit/', views.PacienteUpdate.as_view(), name='paciente-edit'),
            path('delete/', views.PacienteDelete.as_view(), name='paciente-delete'),
            path('consulta/', include([
                path('', views.PacienteConsultaList.as_view(), name='paciente-consultas'),
                path('create/', views.PacienteConsultaCreate.as_view(), name='paciente-consulta-create'),
                path('<int:consulta_id>/', include([
                    path('edit/', views.PacienteConsultaUpdate.as_view(), name='paciente-consulta-edit'),
                    path('delete/', views.PacienteConsultaDelete.as_view(), name='paciente-consulta-delete'),
                ])),
            ])),
            path('estudios/', include([
                path('', views.PacienteEstudioList.as_view(), name='paciente-estudio'),
                path('create/', views.PacienteEstudioCreate.as_view(), name='paciente-estudio-create'),
                path('<int:estudio_id>/', include([
                    path('edit/', views.PacienteEstudioUpdate.as_view(), name='paciente-estudio-edit'),
                    path('delete/', views.PacienteEstudioDelete.as_view(), name='paciente-estudio-delete'),
                ])),
            ])),
        ])),

    ])),
    path('api/', include([
        path('auth/', include('base.urls')),
        # path('paciente/', include([
        #     path('', PacienteList.as_view(), name='paciente-list'),
        #     path('create/', PacienteCreate.as_view(), name='paciente-create'),
        #     path('update/', PacienteUpdate.as_view(), name='paciente-update'),
        # ])),
        # path('local/', include([
        # ])),
    ])),
]
