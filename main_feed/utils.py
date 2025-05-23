from .models import Review, Ticket

def get_users_viewable_reviews(user):
    return Review.objects.filter(user=user).order_by("-time_created")

def get_users_viewable_tickets(user):
    return Ticket.objects.filter(user=user).order_by("-time_created")
