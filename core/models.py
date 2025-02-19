from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator


# Create your models here.

#Modelo Emilx
  #Tabla Usuario -Emix
class Register(models.Model):  
    name = models.CharField (max_length=20, verbose_name="Nombre", null=False, blank=False)
    last_name = models.CharField (max_length=25, verbose_name="Primer apellido", null=False, blank=False)
    second_lastname = models.CharField(max_length=20, verbose_name="Segundo apellido", blank=True)
    email = models.EmailField(unique=True, verbose_name="Correo electrónico")
    passrd = models.CharField(max_length= 30, verbose_name='Contraseña', null=False, blank=False)
    cellphone = models.CharField(
        max_length=10,
        unique=True,
        validators=[MinLengthValidator(10)],
        verbose_name="Número de celular"
    )

    user_active = models.BooleanField(default=True, verbose_name="Usuario activo")
    user_admin = models.BooleanField(default=False, verbose_name="Usuario admin")
    
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['name', 'lastname', 'cellphone_number']

    def __str__(self):
        return self.name_contact
#Clase meta con meta datos de la tabla
class Meta:
    db_table = 'Register'
    verbose_name = 'Registro'
    verbose_name_plural = 'Registros'
    ordering = ['id']


#Arreglo para topic_contact (opciones a elegir) -LGS
options = [
    [0, 'Mas sobre las membresias'],
    [1, 'Cotizar'],
    [2, 'Dudas sobre pagos'],
    [3, 'Dudas en general y sugerencias']
]
    
#Se agrega blank=FALSE para validar no tener campos vacios -LGS

class Contactos(models.Model):
    name_contact = models.CharField(max_length=100, null=False, blank=False, unique=False, verbose_name='Nombre')
    lastname_contact = models.CharField(max_length=100, null=False, blank=False, unique=False, verbose_name='Apellido')
    phone_contact = models.CharField(
        max_length=10, null=False, blank=False, unique=False, verbose_name='Telefono'
    )
    email_contact = models.EmailField(null=False, blank=False, unique=True, verbose_name="Email")
    topic_contact = models.IntegerField(choices=options, null=True, unique=False, blank=False ,verbose_name='Tema de elección')
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

# class Posts(models.Model):
#     autor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
#     contacto = models.ForeignKey(Contactos, on_delete=models.CASCADE)
#     titulo = models.CharField(max_length=200, unique=True, null=False, verbose_name='Título')
#     contenido = models.TextField(null=True, verbose_name='Contenido del post')
#     imagen = models.ImageField(upload_to='post/%Y/%M/%D', null=True, verbose_name='Imagen del post')
#     fecha_alta = models.DateTimeField(auto_now_add=True, verbose_name='Fecha alta')
#     fecha_actualizacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de actualización')

#     def __str__(self):
#         return self.titulo

#     class Meta:
#         db_table = 'posts'
#         verbose_name = 'Post'
#         verbose_name_plural = 'Posts'
#         ordering = ['id']

