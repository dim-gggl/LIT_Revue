from django import forms
from .models import Ticket, Review, Comment
from django.utils.translation import gettext_lazy as _


class TicketForm(forms.ModelForm):
    """
    A Django ModelForm for creating or updating Ticket instances.

    Fields:
        - title: The title of the ticket.
        - description: A brief description of the ticket,
        displayed as a textarea with 3 rows.
        - image: An optional image associated with the ticket.
        - update_ticket: A hidden boolean field used to indicate
        if the form is for updating an existing ticket.

    Meta:
        - model: Ticket
        - fields: ["title", "description", "image"]
        - widgets: Customizes the 'description' field to use
        a textarea widget

        - labels: Provides human-readable labels for each
        field, supporting translation.
    """
    update_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = Ticket
        fields = ["title", "description", "image"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }
        labels = {
            "title": _("Titre"),
            "description": _("Description"),
            "image": _("Image")
        }


class ReviewForm(forms.ModelForm):
    """
    A Django ModelForm for creating or updating a Review instance.

    Fields:
        - headline: The title or summary of the review.
        - body: The main content of the review, rendered as
        a textarea with 4 rows.
        - rating: An integer rating from 0 to 5, displayed
        as radio buttons with star symbols.
        - update_review: A hidden boolean field to indicate
        if the form is used for updating a review (default: True).

    Meta:
        - model: Review
        - fields: ["headline", "body", "rating"]
        - widgets: Custom widgets for 'body' (Textarea) and
        'rating' (RadioSelect with star choices).
        - labels: French labels for each field.
    """
    update_review = forms.BooleanField(
        widget=forms.HiddenInput, initial=True
        )

    class Meta:
        model = Review
        fields = ["headline", "body", "rating"]
        widgets = {
            "body": forms.Textarea(attrs={"rows": 4}),
            "rating": forms.RadioSelect(
                choices=[
                    (i, i * "★") for i in range(6)
                ]
            )
        }
        labels = {
            "headline": _("En-tête"),
            "body": _("Contenu"),
            "rating": _("Note")
        }


class DeleteTicketForm(forms.Form):
    """
    A form used to confirm the deletion of a ticket.

    Fields:
        delete_ticket (BooleanField): A hidden field set
        to True to indicate the user's intent to delete the ticket.
    """
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class DeleteReviewForm(forms.Form):
    """
    A form used to confirm the deletion of a review.

    Fields:
        delete_review (BooleanField): A hidden field set to True
        by default, used to indicate the user's intention to delete a review.
    """
    delete_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class UserFollowForm(forms.Form):
    """
    A Django form for searching and following users by username.

    Fields:
        username (CharField): A text input field for entering
        the username of the user to search for and follow.
            - Label: "Rechercher un utilisateur"
            - Max length: 150 characters
            - Placeholder: "Entrez un nom d'utilisateur"
    """
    username = forms.CharField(
        label="Rechercher un utilisateur",
        max_length=150,
        widget=forms.TextInput(attrs={
            "placeholder": "Entrez un nom d'utilisateur"
        })
    )


class CommentForm(forms.ModelForm):
    """
    A Django ModelForm for creating and editing Comment instances.

    Fields:
        content (str): The text content of the comment, displayed
        with a label "Votre commentaire" and rendered as a textarea
        with 3 rows.

    Meta:
        model: Comment
        fields: ["content"]
        labels: {"content": _("Votre commentaire")}
        widgets: {"content": forms.Textarea(attrs={"rows": 3})}
    """
    class Meta:
        model = Comment
        fields = ["content"]
        labels = {"content": _("Votre commentaire")}
        widgets = {"content": forms.Textarea(attrs={"rows": 3})}
