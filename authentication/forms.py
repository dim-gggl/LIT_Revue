from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=64, label="Nom d'utilisateur"
        )
    password = forms.CharField(
        max_length=128,
        widget=forms.PasswordInput,
        label="Mot de passe"
        )

class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ["username"]
        labels = {
            "username": _("Nom d'utilisateur")
            }
