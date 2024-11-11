from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Usuario

class RegistroUsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'RUT', 'email', 'direccion', 'telefono', 'fecha_nacimiento', 'password1', 'password2']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }

class LoginForm(forms.Form):
    RUT = forms.CharField(max_length=12)
    password = forms.CharField(widget=forms.PasswordInput)

class UsuarioChangeForm(UserChangeForm):
    class Meta:
        model = Usuario
        fields = ['username', 'RUT', 'email', 'direccion', 'telefono', 'fecha_nacimiento']
        exclude = ['password']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('password', None)