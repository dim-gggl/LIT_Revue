from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _


class LoginForm(forms.Form):
    """
    LoginForm is a Django form for user authentication.

    Fields:
        username (CharField): The user's username.
        Maximum length is 64 characters.
        password (CharField): The user's password.
        Maximum length is 128 characters. Rendered as a password input.

    Labels:
        username: "Nom d'utilisateur"
        password: "Mot de passe"
    """
    username = forms.CharField(
        max_length=64, label="Nom d'utilisateur"
        )
    password = forms.CharField(
        max_length=128,
        widget=forms.PasswordInput,
        label="Mot de passe"
        )


class SignUpForm(UserCreationForm):
    """
    Custom user sign-up form extending Django's UserCreationForm.

    This form is used to register new users, utilizing the custom user model
    defined in the project.
    It includes only the 'username' field, which is labeled as
    "Nom d'utilisateur" for localization.

    Attributes:
        Meta (class): Inherits from UserCreationForm.Meta.
            model: The user model returned by get_user_model().
            fields: List containing 'username' as the only field.
            labels: Dictionary mapping 'username' to its localized label.
    """
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ["username"]
        labels = {
            "username": _("Nom d'utilisateur")
            }
