from django.core.exceptions import ValidationError


class ContainsLetterValidator:
    def validate(self, password, user=None):
        if not any(char.isalpha() for char in password):
            raise ValidationError("Le mot de passe doit contenir au moins une lettre", code="password_no_letters")

    def get_help_text(self):
        return ""

class ContainsNumberValidator:
    def validate(self, password, user=None):
        if not any(char.isdigit() for char in password):
            raise ValidationError("Le mot de passe doit contenir un chiffre", code="password_no_digits")

    def get_help_text(self):
        return ""

class LengthValidator:
    def validate(self, password, user=None):
        if not 8 <= len(password) <= 128:
            raise ValidationError("Le mot de passe doit contenir entre 8 et 128 caractères", code="password_wrong_length")

    def get_help_text(self):
        return ""


