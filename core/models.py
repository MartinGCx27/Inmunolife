from django.db import models
from django.contrib.auth.models import User


#Modelo Emilio

#Db Login
#Crea tabla user con los campos name, lastname, second_lastname, email, password, celular (posibles campos: RFC, )
class User(models.Model):
    name=models.TextField (max_lenght=50, null=False, verbose_name="Nombre")
    laststname=models.TextField (max_lenght=20, null=False, verbose_name="Primer apeliido")
    second_lastname=models.TextField (max_leght=20, null=False, verbose_name="Segundo apellido")
    email=models.EmailField(null=False, unique=True, verbose_name="Correo electronico")
    password=models.CharField(min_lenght=8, max_lenght=30, null=False, verbose_name="Contraseña")
    cellphone_number=models.DecimalField(max_digits=12, decimal_places=0, unique=True, null=False, verbose_name="Número de celular")

#Convertimos la tabla en una varibale
def __str__(self):
    return self.User
    
#Clase meta con meta datos de la tabla
class Meta:
    db_table = 'User'
    verbose_name = 'Usuario'
    verbose_name_plural = 'Usuarios'
    ordering = ['id']



    

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
    contacto = models.ForeignKey(Contactos, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200, unique=True, null=False, verbose_name='Título')
    contenido = models.TextField(null=True, verbose_name='Contenido del post')
    imagen = models.ImageField(upload_to='post/%Y/%M/%D', null=True, verbose_name='Imagen del post')
    fecha_alta = models.DateTimeField(auto_now_add=True, verbose_name='Fecha alta')
    fecha_actualizacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de actualización')

    def __str__(self):
        return self.titulo

    class Meta:
        db_table = 'posts'
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['id']
