from django import forms
from .models import Contactos, Register
import requests
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password 


#se cambia de int a string las opciones -LGS
TOPIC_CHOICES = [
    ('Mas sobre las membresias', 'Mas sobre las membresias'),
    ('Cotizar', 'Cotizar'),
    ('Dudas sobre pagos', 'Dudas sobre pagos'),
    ('Dudas generales y sugerencias', 'Dudas en general y sugerencias'),
]

# formulario para contactanos -LGS
class FormContact(forms.ModelForm):
    topic_contact = forms.ChoiceField(
        choices=TOPIC_CHOICES,  # Usa las opciones actualizadas -LGS
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Elige el tema de tu interés:"
    )

    class Meta:
        model = Contactos
        fields = ['name_contact', 'lastname_contact', 'phone_contact', 'email_contact', 'topic_contact', 'comments_contact']
        widgets = {
            'name_contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu Nombre'}),
            'lastname_contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu Apellido'}),
            'phone_contact': forms.TextInput(attrs={
                'class': 'form-control',
                'pattern': '[0-9]{10}',  # Permite solo números con exactamente 10 dígitos -LGS
                'placeholder': 'Tu Teléfono (10 dígitos)',
                'title': 'El número debe tener exactamente 10 dígitos.',
                'oninput': 'filterNumbers(this)',  # Función JS para permitir solo números -LGS
            }),
            'email_contact': forms.EmailInput(attrs={'class': 'form-control','required placeholder': 'Tu correo personal'}),
            'topic_contact': forms.Select(attrs={'class': 'dropdown-item'}),
            'comments_contact': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Inserta tus comentarios', 'rows': 6}),
        }
    #def clean_email_contact(self):
    #         email = self.cleaned_data.get('email_contact')
    #         if Contactos.objects.filter(email_contact=email).exists():
    #             raise forms.ValidationError("Este correo electrónico ya está registrado.")
    #         return email
    # def clean_phone_contact(self):
    #     phone = self.cleaned_data.get('phone_contact')
    # #     if Contactos.objects.filter(phone_contact=phone).exists():
    # #         raise forms.ValidationError("Este número de teléfono ya está registrado.")
    #     if phone and (len(str(phone)) != 10):
    #          raise forms.ValidationError("El número de teléfono debe tener exactamente 10 dígitos.")
    #     return phone           
        

# Clase para registrar usuarios
class RegisterForm(forms.ModelForm):
    confirm_passrd = forms.CharField(
        max_length=128,
        widget=forms.PasswordInput,
        label="Confirmar Contraseña"
    )

    class Meta:
        model = Register
        fields = [
            'name',
            'last_name',
            'second_lastname',
            'email',
            'passrd',
            'cellphone'
        ]
        widgets = {
                'passrd': forms.PasswordInput()
            }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("passrd")
        confirm_password = cleaned_data.get("confirm_passrd")

        if password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data

    def clean_email(self): 
        email = self.cleaned_data.get('email')
        if Register.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado.")
        return email
    
    def clean_cellphone(self): 
        cellphone = self.cleaned_data.get('cellphone')
        if Register.objects.filter(cellphone=cellphone).exists():
            raise forms.ValidationError("Este número ya está registrado.")
        if len(cellphone) != 10:
            raise forms.ValidationError("El celular debe tener 10 dígitos.")
        return cellphone


class LoginForm(forms.Form):
    loginEmail = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Correo electrónico',
            'id': 'loginEmail'
        }),
        label="Correo electrónico"
    )
    loginPassword = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña',
            'id': 'loginPassword'
        }),
        label="Contraseña"
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('loginEmail')
        password = cleaned_data.get('loginPassword')

        # Validación de campos vacíos
        if not email or not password:
            raise forms.ValidationError("Todos los campos son obligatorios.")

        try:
            user = Register.objects.get(email=email)
            if not check_password(password, user.passrd):
                raise forms.ValidationError("Contraseña incorrecta.")
        except Register.DoesNotExist:
            raise forms.ValidationError("El correo no está registrado.")

        return cleaned_data
    
#Formulario para solicitar el restablecimiento de contraseña -LGS
class PasswordResetRequestForm(forms.Form):

    email = forms.EmailField(label="Correo Electrónico", widget=forms.EmailInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        if not Register.objects.filter(email=email).exists():
            raise ValidationError("Este correo no está registrado.")
        return email

#Formulario para nueva contraseña -LGS
class PasswordResetForm(forms.Form):
    new_password = forms.CharField(
        label="Nueva Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )
    confirm_password = forms.CharField(
        label="Confirmar Nueva Contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and confirm_password and new_password != confirm_password:
            raise ValidationError("Las contraseñas no coinciden.")

        return cleaned_data