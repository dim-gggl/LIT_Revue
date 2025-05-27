from .models import Review, Ticket

def get_users_viewable_reviews(user):
    followee_ids = user.following.values_list('id', flat=True)
    user_ids = list(followee_ids) + [user.id]
    return Review.objects.filter(user_id__in=user_ids).order_by("-time_created")

def get_users_viewable_tickets(user):
    followee_ids = user.following.values_list('id', flat=True)
    user_ids = list(followee_ids) + [user.id]
    return Ticket.objects.filter(user_id__in=user_ids).order_by("-time_created")

