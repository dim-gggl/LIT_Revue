from django import forms
from .models import Ticket, Review


class TicketForm(forms.ModelForm):
    update_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }

class ReviewForm(forms.ModelForm):
    update_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = Review
        fields = ["headline", "body", "rating"]
        widgets = {
            "body": forms.Textarea(attrs={"rows": 4}),
            "rating": forms.RadioSelect(
                choices=[
                    (i, f"{i} ★") for i in range(6)
                    ])
        }

class DeleteTicketForm(forms.Form):
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)

class DeleteReviewForm(forms.Form):
    delete_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)

class UserFollowForm(forms.Form):
    username = forms.CharField(
        label="Rechercher un utilisateur",
        max_length=150,
        widget=forms.TextInput(attrs={"placeholder": "Entrez un nom d’utilisateur"})
    )

