from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import MinValueValidator, MaxValueValidator


#Modelo Emilio
'''
#Db Login
#Crea tabla user con los campos name, lastname, second_lastname, email, password, celular (posibles campos: RFC, )
class User(AbstractBaseUser):
    name=models.TextField (max_length=50, null=False, verbose_name="Nombre", blank=False)
    lastname=models.TextField (max_length=20, null=False, verbose_name="Primer apeliido", blank=False)
    second_lastname=models.TextField (max_length=20, null=False, verbose_name="Segundo apellido", blank=True)
    email=models.EmailField(null=False, unique=True, verbose_name="Correo electronico", blank=False)
    passrd=models.CharField(max_length=30, null=False, verbose_name="Contraseña", blank=False)
    #Se agrega validadores al campo celular
    cellphone_number=models.IntegerField(unique=True, null=False, verbose_name="Número de celular", blank=False)(
        validators=[MinValueValidator (10), MaxValueValidator (10)]
    )
    user_active = models.BooleanField (default=True, verbose_name="Usuario activo")
    user_admin = models.BooleanField(default=False, verbose_name="Usuario admin")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email, passrd']
# class User(models.Model):
#     name=models.TextField (max_length=50, null=False, verbose_name="Nombre")
#     lastname=models.TextField (max_length=20, null=False, verbose_name="Primer apeliido")
#     second_lastname=models.TextField (max_length=20, null=False, verbose_name="Segundo apellido")
#     email=models.EmailField(null=False, unique=True, verbose_name="Correo electronico")
#     passrd=models.CharField(max_length=30, null=False, verbose_name="Contraseña")
#     #Se agrega validadores al campo celular
#     cellphone_number=models.IntegerField(unique=True, null=False, verbose_name="Número de celular")(
#         validators=[MinValueValidator (10), MaxValueValidator (10)]
#     )

#Convertimos la tabla en una variable
def __str__(self):
    return f'User {self.name},{self.lastname},{self.second_lastname}'

def has_perm(self,perm,obj = None):
    return True

def has_module_perms(self,app_label):
    return True
@property
def is_staff(self):
    return self.usuario_administrador
    
#Clase meta con meta datos de la tabla
class Meta:
    db_table = 'User'
    verbose_name = 'Usuario'
    verbose_name_plural = 'Usuarios'
    ordering = ['id']



    

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
        '''
