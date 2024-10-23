# Generated by Django 5.1.1 on 2024-10-19 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signupKL', '0012_rename_fotos_del_proyecto_proyecto_portada_de_proyecto_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='imagenesdeproyecto',
            options={'verbose_name_plural': 'Galería de proyectos'},
        ),
        migrations.AlterField(
            model_name='imagenesdeproyecto',
            name='imagen',
            field=models.ImageField(upload_to='proyectos_galeria/'),
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='Portada_de_proyecto',
            field=models.ImageField(blank=True, null=True, upload_to='proyectos_portada/'),
        ),
    ]