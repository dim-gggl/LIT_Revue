from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from LITRevue.settings import AUTH_USER_MODEL

from PIL import Image


class Ticket(models.Model):
    """
    Represents a ticket created by a user, which may include
    a title, description, optional image, and creation timestamp.

    Fields:
        title (CharField): The title of the ticket (max 128 characters).
        description (TextField): Optional detailed description of the
        ticket (max 2048 characters).
        user (ForeignKey): Reference to the user who created the ticket.
        image (ImageField): Optional image associated with the ticket.
        time_created (DateTimeField): Timestamp when the ticket was created.

    Properties:
        has_review (bool): Returns True if at least one review exists for
        this ticket.

    Methods:
        resize_image(): Resizes the associated image to fit within
        IMAGE_MAX_SIZE.
        save(*args, **kwargs): Saves the ticket instance and resizes
        the image if present.
    """
    title = models.CharField(max_length=128)
    description = models.TextField(
        max_length=2048, blank=True
        )
    user = models.ForeignKey(
        to=AUTH_USER_MODEL,
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
    """
    Represents a review for a ticket in the application.
    Attributes:
        ticket (Ticket): The ticket associated with this review.
        rating (int): The rating given in the review (0 to 5).
        headline (str): The headline/title of the review
        (max 128 characters).
        body (str): The main content of the review (max 8192
        characters, optional).
        user (User): The user who wrote the review.
        time_created (datetime): The timestamp when the review
        was created.

    Properties:
        stars_rating (str): Returns a string of star characters
        ("★") corresponding to the rating.

    Methods:
        __str__(): Returns a string representation of the review,
        including its ID and associated ticket title.
    """
    ticket = models.ForeignKey(
        to=Ticket, on_delete=models.CASCADE
        )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
        )
    headline = models.CharField(max_length=128)
    body = models.CharField(max_length=8192, blank=True)
    user = models.ForeignKey(
        to=AUTH_USER_MODEL,
        on_delete=models.CASCADE
        )
    time_created = models.DateTimeField(auto_now_add=True)

    @property
    def stars_rating(self):
        return "" + "★" * self.rating

    def __str__(self):
        return (f"Review #{id} - "
                f"{self.ticket.title if self.ticket else 'No Ticket'}")


class Comment(models.Model):
    """
    Represents a comment made by a user on a review.

    Attributes:
        review (Review): The review to which this comment
        is attached.
        author (User): The user who wrote the comment.
        content (str): The textual content of the comment
        (optional, up to 2048 characters).
        time_created (datetime): The date and time when
        the comment was created.

    Methods:
        __str__(): Returns a string representation of the
        comment, including its ID, author, and associated
        review.
    """
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name="comments"
    )
    author = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    content = models.TextField(
        max_length=2048, verbose_name="Commentaire",
        blank=True, null=True
    )
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f"Comment #{self.id} par {self.author} "
                f"sur Review #{self.review.id}")
