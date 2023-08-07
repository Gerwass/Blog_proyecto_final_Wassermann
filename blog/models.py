from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Posteo (models.Model):
    #los atributos de clase(son las columnas de la tabla)
    titulo = models.CharField(max_length=64)
    bajada = models.CharField(max_length=140)
    creador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posteo_creados', null=True)
    imagen = models.ImageField(upload_to='media')
    texto = models.CharField(max_length=5000)
    fecha_publicacion=models.DateField(null=True)

    def __str__(self):
        return f"{self.titulo}, {self.creador}"