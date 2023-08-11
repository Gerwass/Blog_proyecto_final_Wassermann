from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count
from ckeditor.fields import RichTextField
import uuid
# Create your models here.

class Avatar(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
   
    imagen = models.ImageField(upload_to='avatares', null=True, blank=True)

    def __str__(self):
        return f"Avatar de: {self.user}"
    




class ModelBase(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, db_index=True,editable=False)
    tiempo = models.DateTimeField(auto_now_add=True)
    actualizar = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
    
class CanalMensaje(ModelBase):
    canal = models.ForeignKey("Canal", on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, related_name='chats_usuario1', on_delete=models.CASCADE)
    texto = RichTextField(config_name='default')

class CanalUsuario(ModelBase):
    canal = models.ForeignKey("Canal", null = True, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)



class CanalQuerySet(models.QuerySet):
    def solo_uno(self):
        return self.annotate(num_usuarios = Count("usuarios").fitler(num_usuarios=1))

    def solo_dos(self):
        return self.annotate(num_usuarios = Count("usuarios").fitler(num_usuarios=2))
    


class CanalManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return CanalQuerySet(self.model, using=self._db)




class Canal(ModelBase):
    usuarios = models.ManyToManyField(User, blank=True, through=CanalUsuario)
    objects = CanalManager()
    




