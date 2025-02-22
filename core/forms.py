from django import forms
from .models import Contactos, Register
import requests

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
            'phone_contact': forms.NumberInput(attrs={'class': 'form-control ', 'placeholder': 'Tu Telefono (Max. 10 digitos)',
                'oninput': 'countDigits(this)'}),
            'email_contact': forms.EmailInput(attrs={'class': 'form-control ','placeholder': 'Tu correo personal'}),
            'topic_contact': forms.Select(attrs={'class': 'dropdown-item'}),
            'comments_contact': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Inserta tus comentarios', 'rows': 6}),
        }
    def clean_email_contact(self):
            email = self.cleaned_data.get('email_contact')
            if Contactos.objects.filter(email_contact=email).exists():
                raise forms.ValidationError("Este correo electrónico ya está registrado.")
            return email
    def clean_phone_contact(self):
        phone = self.cleaned_data.get('phone_contact')
        if Contactos.objects.filter(phone_contact=phone).exists():
            raise forms.ValidationError("Este número de teléfono ya está registrado.")
        if phone and (len(str(phone)) != 10):
            raise forms.ValidationError("El número de teléfono debe tener exactamente 10 dígitos.")
        return phone           
        

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