# Generated by Django 5.1.1 on 2024-11-15 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signupKL', '0018_alter_imagenesdeproyecto_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagenesdeproyecto',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='proyectos_galeria/'),
        ),
    ]