from django.urls import path
from main_feed.views import home, create_review, create_ticket, HomeView, TicketCreateView


urlpatterns = [
    path("home/", HomeView.as_view(), name="homepage"),
    path("tickets/create/", TicketCreateView.as_view(), name="create_ticket"),
    path("reviews/create/", create_review, name="create_review"),
    path("reviews/create/<int:ticket_id>/", create_review, name="create_review_from_ticket")
]
