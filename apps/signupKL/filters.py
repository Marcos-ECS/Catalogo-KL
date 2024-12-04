# filters.py
import django_filters
from .models import Proyecto

class ProyectoFilter(django_filters.FilterSet):
    titulo = django_filters.CharFilter(lookup_expr='icontains', label="Buscar por título")
    estatus = django_filters.ChoiceFilter(
        field_name='estatus',
        choices=Proyecto._meta.get_field('estatus').choices,  # Usa las opciones definidas en el modelo
        label="Estatus del proyecto"
    )

    class Meta:
        model = Proyecto
        fields = ['titulo', 'estatus']
