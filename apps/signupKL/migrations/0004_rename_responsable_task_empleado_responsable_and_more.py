# Generated by Django 5.1.1 on 2024-10-06 04:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('signupKL', '0003_rename_creado_task_fechadeagregado_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='Responsable',
            new_name='Empleado_Responsable',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='titulo',
            new_name='Titulo',
        ),
    ]