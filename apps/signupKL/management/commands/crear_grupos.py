from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Crea los grupos necesarios para los tipos de usuario'

    def handle(self, *args, **kwargs):
        grupos = ['Empleado', 'Admin', 'Cliente']
        for grupo in grupos:
            Group.objects.get_or_create(name=grupo)
        self.stdout.write(self.style.SUCCESS('Grupos creados correctamente.'))
