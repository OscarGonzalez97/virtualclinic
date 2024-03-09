from rest_framework import serializers

from .models import Usuario


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('id', 'first_name', 'last_name', 'nro_documento', 'email', 'password', 'fecha_nacimiento', 'nro_telefono')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}

    def create(self, validated_data):
        user = Usuario.objects.create(
            email=validated_data['email'],
            nro_documento=validated_data['nro_documento'],
            fecha_nacimiento=validated_data['fecha_nacimiento'],
            nro_telefono=validated_data['nro_telefono'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.nro_documento = validated_data.get('nro_documento', instance.nro_documento)
        instance.fecha_nacimiento = validated_data.get('fecha_nacimiento', instance.fecha_nacimiento)
        instance.nro_telefono = validated_data.get('nro_telefono', instance.nro_telefono)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        return instance
