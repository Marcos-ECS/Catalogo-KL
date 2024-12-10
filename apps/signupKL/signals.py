from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'profile'):  # Verificar si ya existe un perfil
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):  # Solo guardar si existe un perfil
        instance.profile.save()


#Para asignar tipo de usuario por defecto, por ahora se mantendra comentado, en caso de que se necesite en el futuro, 
# actualmente se puede elegir el tipo de usuario desde el front, por lo que si este codigo se habilita
#causa que los nuevos usuarios tenga doble grupo, el defaultl Cliente+El grupo elegido, cuando solo deben tener un solo grupo
#si se elimina la seleccion desde el front, descomentar esto, para tener un grupo por defecto
#se requirira el uso de Django Admin para reasignar grupos.

#@receiver(post_save, sender=User)
#def asignar_grupo_defecto(sender, instance, created, **kwargs):
#    if created and not instance.groups.exists():
#        default_group, _ = Group.objects.get_or_create(name='Cliente')  # Grupo por defecto
#        instance.groups.add(default_group)
        
