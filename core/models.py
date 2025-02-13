from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
#Modelo Emilio

#Db Login
#Crea tabla user con los campos name, lastname, second_lastname, email, password, celular (posibles campos: RFC, )
class User(models.Model):
    name=models.TextField (max_length=50, null=False, verbose_name="Nombre")
    lastname=models.TextField (max_length=20, null=False, verbose_name="Primer apeliido")
    second_lastname=models.TextField (max_length=20, null=False, verbose_name="Segundo apellido")
    email=models.EmailField(null=False, unique=True, verbose_name="Correo electronico")
    passrd=models.CharField(max_length=30, null=False, verbose_name="Contraseña")
    cellphone_number=models.IntegerField(max_length=10, unique=True, null=False, verbose_name="Número de celular")

#Convertimos la tabla en una variable
def __str__(self):
    return self.User
    
#Clase meta con meta datos de la tabla
class Meta:
    db_table = 'User'
    verbose_name = 'Usuario'
    verbose_name_plural = 'Usuarios'
    ordering = ['id']



    
#Se agrega blank=FALSE para validar no tener campos vacios -LGS

class Contactos(models.Model):
    name_contact = models.CharField(max_length=100, null=False, blank=False, unique=False, verbose_name='Nombre')
    lastname_contact = models.CharField(max_length=100, null=False, blank=False, unique=False, verbose_name='Apellido')
    email_contact = models.EmailField(null=False, blank=False, unique=True, verbose_name="Email")
    phone_contact = models.IntegerField(
        validators=[MinValueValidator(10), MaxValueValidator(10)]
        , null=True, blank=False ,unique=True, verbose_name='Telefono')
    topic_contact = models.TextField(null=True, unique=False, blank=False ,verbose_name='Tema de elección')
    comments_contact = models.TextField(null=True, blank=False, verbose_name='Comentarios')
    date_contact = models.DateTimeField(auto_now_add=True, verbose_name='Fecha alta')
    status_contact = models.BooleanField(default=False ,null=False, blank=False, verbose_name='Estado')
    
    def __str__(self):
        return self.name_contact
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
