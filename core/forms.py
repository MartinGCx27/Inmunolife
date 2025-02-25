from django import forms
from .models import Contactos, Register
import requests
from django.core.exceptions import ValidationError

TOPIC_CHOICES = [
    (0, 'Mas sobre las membresias'),
    (1, 'Cotizar'),
    (2, 'Dudas sobre pagos'),
    (3, 'Dudas en general y sugerencias'),
]

# formulario para contactanos -LGS
class FormContact(forms.ModelForm):
    topic_contact = forms.ChoiceField(
        choices=TOPIC_CHOICES,
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
            'email_contact': forms.EmailInput(attrs={'class': 'form-control ','required placeholder': 'Tu correo personal'}),
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

class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Correo Electrónico",
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu correo'
        })
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu contraseña'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            try:
                user = Register.objects.get(email=email)
                if user.passrd != password:
                    self.add_error('password', 'Contraseña incorrecta.')
            except Register.DoesNotExist:
                self.add_error('email', 'No existe una cuenta con este correo.')
        return cleaned_data