from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from authentication.models import User
from django.conf import settings

from PIL import Image


class Ticket(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(
        max_length=2048, blank=True
        )
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
        )
    image = models.ImageField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    IMAGE_MAX_SIZE = (210, 297)

    @property
    def has_review(self):
        return Review.objects.filter(ticket=self).exists()

    def resize_image(self):
        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        image.save(self.image.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image()


class Review(models.Model):
    ticket = models.ForeignKey(
        to=Ticket, on_delete=models.CASCADE
        )
    rating = models.PositiveSmallIntegerField(
        # validates that rating must be between 0 and 5
        validators=[MinValueValidator(0), MaxValueValidator(5)]
        )
    headline = models.CharField(max_length=128)
    body = models.CharField(max_length=8192, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
        )
    time_created = models.DateTimeField(auto_now_add=True)

    @property
    def stars_rating(self):
        return "" + "★" * self.rating


class Comment(models.Model):
    review = models.ForeignKey(
        to=Review, on_delete=
        models.CASCADE
    )
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE
    )
    time_created = models.DateTimeField(auto_now_add=True)

