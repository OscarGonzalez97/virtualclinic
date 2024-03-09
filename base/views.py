from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from base.models import Usuario
from base.serializers import UserSerializer

ERROR_TEMPLATE = "consultorio/error.html"

class UserCreateAPIView(generics.CreateAPIView):
    """Enpoint para crear un nuevo usuario (registro)"""
    queryset = Usuario.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        data = {
            'token': token.key,
            'id': user.id,
            'email': user.email,
            'full_name': user.full_name,
            'genero': user.genero,
            'fecha_nacimiento': user.fecha_nacimiento,
            'nro_telefono': user.nro_telefono,
        }
        return Response(data, status=status.HTTP_201_CREATED)


class LoginAuthToken(ObtainAuthToken):
    """Enpoint para el login"""

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'id': user.id,
            'email': user.email,
            'full_name': user.full_name,
            'nro_documento': user.nro_documento,
            'fecha_nacimiento': user.fecha_nacimiento,
            'nro_telefono': user.nro_telefono,
        })


def handler400(request, exception, template_name=ERROR_TEMPLATE):
    data = {
        'codigo': 400,
        'titulo': 'Solicitud incorrecta',
        'mensaje': 'Verifique que los datos enviados sean los correctos.'
    }
    response = render(request, template_name, data)
    response.status_code = 400
    return response


def handler403(request, exception, template_name=ERROR_TEMPLATE):
    data = {
        'codigo': 403,
        'titulo': 'Acceso denegado',
        'mensaje': 'No posee permiso para acceder a esta página.'
    }
    response = render(request, template_name, data)
    response.status_code = 403
    return response


def handler404(request, exception, template_name=ERROR_TEMPLATE):
    data = {
        'codigo': 404,
        'titulo': 'Página no encontrada',
        'mensaje': 'La página solicitada no existe.'
    }
    response = render(request, template_name, data)
    return response


def handler500(request):
    data = {
        'codigo': 500,
        'titulo': 'Error del servidor',
        'mensaje': 'Ha ocurrido un error inesperado, nuestros técnicos están trabajando en una solución.'
    }
    response = render(request, ERROR_TEMPLATE, data)
    response.status_code = 500
    return response
