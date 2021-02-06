from django import forms


class LoginForm(forms.Form):
    """Formulario para autenticar usuarios"""
    username = forms.CharField(label='Nombre de usuario', max_length=100)
    password = forms.CharField(label='Contraseña', max_length=100, widget=forms.PasswordInput)


class PreguntaForm(forms.Form):
    """Formulario para añadir opiniones"""
    titulo = forms.CharField(max_length=250, required=True, label="Título")
    texto = forms.CharField(max_length=5000, required=True, label='Texto')

class RespuestaForm(forms.Form):
	texto = forms.CharField(max_length=5000, required=True, label='Texto')