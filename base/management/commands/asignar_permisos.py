import logging

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand

logger = logging.getLogger('django')


class Command(BaseCommand):
    @staticmethod
    def crear_permisos_list_view():
        for ctype in ContentType.objects.all():
            if not Permission.objects.filter(content_type=ctype, codename='list_{}'.format(ctype.model)).exists():
                Permission.objects.create(
                    name='List {}'.format(ctype.model),
                    content_type=ctype,
                    codename='list_{}'.format(ctype.model)
                )
                logger.info('Creado permiso list_{}'.format(ctype.model))
            if not Permission.objects.filter(content_type=ctype, codename='view_{}'.format(ctype.model)).exists():
                Permission.objects.get_or_create(
                    name='View {}'.format(ctype.model),
                    content_type=ctype,
                    codename='view_{}'.format(ctype.model)
                )
                logger.info('Creado permiso view_{}'.format(ctype.model))

    @staticmethod
    def crear_permisos(permisos, grupo):
        for p in permisos:
            ctype = ContentType.objects.get(app_label=p[0], model=p[1])
            perm = Permission.objects.get(content_type=ctype, codename=p[2])
            if not grupo.permissions.filter(pk=perm.pk).exists():
                grupo.permissions.add(perm)
                logger.info(f'Agregado permiso {p[0]}_{p[1]}.{p[2]} a {grupo.name}')

    def handle(self, *args, **options):
        # administrador de la plataforma tiene todos los permisos
        gadministrador, _ = Group.objects.get_or_create(name='Administrador')

        if _:
            logger.info('Creado grupo Administrador')

        # doctor
        gdoctor, _ = Group.objects.get_or_create(name='Doctor')

        if _:
            logger.info('Creado grupo Doctor')

        # cliente que se registra para transaccionar en la aplicacion
        gcliente, _ = Group.objects.get_or_create(name='Cliente')

        if _:
            logger.info('Creado grupo Cliente')

        self.crear_permisos_list_view()

        pcliente = [
            ('consultorio', 'paciente', 'list_paciente'),
            ('consultorio', 'paciente', 'view_paciente'),
            ('consultorio', 'paciente', 'change_paciente'),
            ('consultorio', 'consulta', 'list_consulta'),
            ('consultorio', 'estudio', 'list_estudio'),
        ]

        pdoctor = [
            ('consultorio', 'paciente', 'add_paciente'),
            ('consultorio', 'consulta', 'view_consulta'),
            ('consultorio', 'consulta', 'add_consulta'),
            ('consultorio', 'consulta', 'change_consulta'),
            ('consultorio', 'consulta', 'delete_consulta'),
            ('consultorio', 'estudio', 'view_estudio'),
            ('consultorio', 'estudio', 'add_estudio'),
            ('consultorio', 'estudio', 'change_estudio'),
            ('consultorio', 'estudio', 'delete_estudio'),
            ('consultorio', 'tipoestudio', 'list_tipoestudio'),
            ('consultorio', 'tipoestudio', 'view_tipoestudio'),
            ('consultorio', 'tipoestudio', 'add_tipoestudio'),
            ('consultorio', 'tipoestudio', 'change_tipoestudio'),
            ('consultorio', 'tipoestudio', 'delete_tipoestudio'),
            ('consultorio', 'laboratorio', 'list_laboratorio'),
            ('consultorio', 'laboratorio', 'view_laboratorio'),
            ('consultorio', 'laboratorio', 'add_laboratorio'),
            ('consultorio', 'laboratorio', 'change_laboratorio'),
            ('consultorio', 'laboratorio', 'delete_laboratorio'),
            ('appointment', 'service', 'list_service'),
            ('appointment', 'service', 'view_service'),
            ('appointment', 'service', 'add_service'),
            ('appointment', 'service', 'change_service'),
            ('appointment', 'service', 'delete_service'),
            ('consultorio', 'consultorio', 'view_consultorio'),
        ] + pcliente

        padministrador = [
            ('base', 'usuario', 'list_usuario'),
            ('base', 'usuario', 'add_usuario'),
            ('base', 'usuario', 'change_usuario'),
            ('base', 'usuario', 'delete_usuario'),
            ('consultorio', 'paciente', 'delete_paciente'),
            ('consultorio', 'consultorio', 'change_consultorio'),
        ] + pdoctor

        self.crear_permisos(pcliente, gcliente)

        self.crear_permisos(pdoctor, gdoctor)

        self.crear_permisos(padministrador, gadministrador)
