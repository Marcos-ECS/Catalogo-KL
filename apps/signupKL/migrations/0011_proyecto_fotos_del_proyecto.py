# Generated by Django 5.1.1 on 2024-10-19 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signupKL', '0010_alter_proyecto_estatus_de_proyecto'),
    ]

    operations = [
        migrations.AddField(
            model_name='proyecto',
            name='Fotos_del_proyecto',
            field=models.ImageField(blank=True, null=True, upload_to='proyectos_imagenes/'),
        ),
    ]
