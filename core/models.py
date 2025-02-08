from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Contactos(models.Model):
    nom_usuario = models.CharField(max_length=500, null=False, unique=True, verbose_name='Nombre')
    
    def __str__(self):
        return self.nom_usuario
    class Meta:
        db_table = 'contact'
        verbose_name = 'Contacto'
        verbose_name_plural = 'Contactos'
        ordering = ['id']

class Posts(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    contacto = models.ForeignKey(Contacto, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200, unique=True, null=False, verbose_name='Título')
    contenido = models.TextField(null=True, verbose_name='Contenido del post')
    imagen = models.ImageField(upload_to='post/%Y/%M/%D' null=True, verbose_name='Imagen del post')
    fecha_alta = models.DateTimeField(auto_now_add=True, verbose_name='Fecha alta')
    fecha_actualizacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de actualización')

    def __str__(self):
        return self.titulo

    class Meta:
        db_table = 'posts'
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['id']