from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.

    Attributes:
        following (ManyToManyField): A many-to-many relationship to self,
        representing the users that this user is following.
            - Uses the 'UserFollows' intermediary model to store
            the relationship.
            - 'through_fields' specifies the order of fields in
            the intermediary model: ('user', 'followed_user').
            - 'symmetrical=False' allows for one-way following
            (user A can follow user B without B following A).
            - 'related_name="followers"' allows reverse access
            to users who follow this user.

    Methods:
        __str__(): Returns the username of the user as the string
        representation.
    """
    following = models.ManyToManyField(
        "self",
        through="UserFollows",
        through_fields=("user", "followed_user"),
        symmetrical=False,
        related_name="followers"
    )

    def __str__(self):
        return self.username


class UserFollows(models.Model):
    """
    Model representing a "follow" relationship between users.

    Attributes:
        user (ForeignKey): The user who is following another user.
        followed_user (ForeignKey): The user being followed.

    Meta:
        unique_together: Ensures that a user cannot follow the
        same user more than once.
        verbose_name: Human-readable singular name for the model
        ("Abonnement").
        verbose_name_plural: Human-readable plural name for the model
        ("Abonnements").
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="follows_relations"
    )
    followed_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="followed_by_relations"
    )

    class Meta:
        unique_together = ("user", "followed_user")
        verbose_name = "Abonnement"
        verbose_name_plural = "Abonnements"
