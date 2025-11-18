from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .validators import normalize_rut

User = get_user_model()


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='Usuario o RUT',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'usuario'}),
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '********'}),
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        if username:
            normalized = normalize_rut(username)
            match = User.objects.filter(rut__iexact=normalized).first()
            if match:
                self.cleaned_data['username'] = match.get_username()
        return super().clean()


class CustomUserCreationForm(UserCreationForm):
    terms = forms.BooleanField(label='Acepto los términos y condiciones')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = [
            'username',
            'email',
            'rut',
            'first_name',
            'last_name',
            'maternal_last_name',
            'age',
            'occupation',
            'sex',
            'phone',
            'city',
        ]
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'correo@dominio.com'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Nombres'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Apellido paterno'}),
            'maternal_last_name': forms.TextInput(attrs={'placeholder': 'Apellido materno'}),
            'occupation': forms.TextInput(attrs={'placeholder': 'Arquitecto, Constructor, etc.'}),
            'phone': forms.TextInput(attrs={'placeholder': '+56 9 0000 0000'}),
            'city': forms.TextInput(attrs={'placeholder': 'Comuna / Ciudad'}),
        }

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        if rut:
            return normalize_rut(rut)
        return rut


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'email',
            'rut',
            'first_name',
            'last_name',
            'maternal_last_name',
            'age',
            'occupation',
            'sex',
            'phone',
            'city',
        ]
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        if rut:
            return normalize_rut(rut)
        return rut
