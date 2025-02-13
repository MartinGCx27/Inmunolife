from django import forms
from .models import Contactos

class FormContact(forms.ModelForm):
    class Meta:
        model = Contactos
        fields = '__all__'
        widgets = {
            'name_contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu Nombre'}),
            'lastname_contact': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Tu Correo Electrónico'}),
            'phone_contact': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Tu Nombre'}),
            'email_contact': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Tu correo personal'}),
            'email_contact': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Tu correo personal'}),
            'comments_contact': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Inserta tus comentarios', 'rows': 6}),
        }