from django.db import models

# Create your models here.
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



    