from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Tous les autres champs hérités
    following = models.ManyToManyField(
        'self',
        through='UserFollows',
        through_fields=('user', 'followed_user'),
        symmetrical=False,
        related_name='followers'
    )

class UserFollows(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='follows_relations'
    )
    followed_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='followed_by_relations'
    )

    class Meta:
        unique_together = ('user', 'followed_user')
        verbose_name = "Abonnement"
        verbose_name_plural = "Abonnements"
