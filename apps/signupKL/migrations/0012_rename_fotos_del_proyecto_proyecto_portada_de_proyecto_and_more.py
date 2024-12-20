# Generated by Django 5.1.1 on 2024-10-19 09:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signupKL', '0011_proyecto_fotos_del_proyecto'),
    ]

    operations = [
        migrations.RenameField(
            model_name='proyecto',
            old_name='Fotos_del_proyecto',
            new_name='Portada_de_proyecto',
        ),
        migrations.CreateModel(
            name='ImagenesdeProyecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(upload_to='proyectos_imagenes/')),
                ('proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imagenes', to='signupKL.proyecto')),
            ],
        ),
    ]
