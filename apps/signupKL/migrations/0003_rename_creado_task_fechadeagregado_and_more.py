# Generated by Django 5.1.1 on 2024-10-06 04:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('signupKL', '0002_rename_usuario_task_responsable_del_proyecto'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='creado',
            new_name='FechaDeAgregado',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='datecompleted',
            new_name='Fecha_De_Realizacion',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='Responsable_Del_Proyecto',
            new_name='Responsable',
        ),
    ]
