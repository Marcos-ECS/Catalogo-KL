# Generated by Django 5.1.1 on 2024-12-04 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signupKL', '0021_estatusdeproyecto_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='tipo_usuario',
            field=models.CharField(choices=[('Empleado', 'Empleado'), ('Admin', 'Admin'), ('Cliente', 'Cliente')], default='Empleado', max_length=20),
        ),
    ]
