# filters.py
import django_filters
from .models import Proyecto, EstatusDeProyecto

class ProyectoFilter(django_filters.FilterSet):
    titulo = django_filters.CharFilter(lookup_expr='icontains', label="Buscar por título")
    estatus = django_filters.ModelChoiceFilter(
        queryset=EstatusDeProyecto.objects.all(),  # Queryset de los estatus
        label="Estatus del proyecto",
        empty_label="Todos"  # Opción para mostrar todos los estatus
    )

    class Meta:
        model = Proyecto
        fields = ['titulo', 'estatus']
