from django.db import models
from django.contrib.auth.models import User

# Create your models here.
<<<<<<< HEAD
#Modelo Emilio

#Db Login
#Crea tabla user con los campos name, email, password, celular (posibles campos: RFC, )
class User(models.Model):
    name=models.CharField (max_lenght=20)
    email=models.EmailField(null=False, unique=True, )
    password=models.CharField(min_lenght=7, max_lenght=15, null=False)
    celular=models.CharField(max_length=10)
    
#Duda
def __str__(self):
    return self.User
    
class Meta:
    db_table = 'user'
    verbose_name = 'usuario'
    verbose_name_plural = 'usuarios'



    
=======

class Contactos(models.Model):
    nombre = models.CharField(max_length=100, null=False, unique=True, verbose_name='Nombre')
    apellido = models.CharField(max_length=100, null=False, unique=True, verbose_name='Apellido')
    email = models.EmailField(null=False, unique=True, verbose_name="Email")
    telefono = models.IntegerField(null=True, unique=False, verbose_name='Telefono')
    comentarios = models.TextField(null=True, verbose_name='Comentarios')
    fecha_alta = models.DateTimeField(auto_now_add=True, verbose_name='Fecha alta')
    estado = models.BooleanField(null=False, verbose_name='Estado')
    
    def __str__(self):
        return self.nombre
    class Meta:
        db_table = 'contact'
        verbose_name = 'Contactos'
        verbose_name_plural = 'Contactos'
        ordering = ['id']

class Posts(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    contacto = models.ForeignKey(Contactos, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200, unique=True, null=False, verbose_name='Título')
    contenido = models.TextField(null=True, verbose_name='Contenido del post')
    fecha_alta = models.DateTimeField(auto_now_add=True, verbose_name='Fecha alta')
    fecha_actualizacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de actualización')

    def __str__(self):
        return self.titulo

    class Meta:
        db_table = 'posts'
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['id']
>>>>>>> master
