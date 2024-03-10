# Generated by Django 4.2.11 on 2024-03-10 02:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('consultorio', '0003_alter_paciente_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paciente',
            name='usuario',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='paciente', to=settings.AUTH_USER_MODEL),
        ),
    ]