from django.urls import path
from main_feed.views import (
    create_review,
    HomeView,
    TicketCreateView,
    update_ticket,
    update_review,
    followings,
    PostsView,
    unfollow_user,
    review_detail
    )


urlpatterns = [
    path("home/", HomeView.as_view(), name="homepage"),
    path(
        "tickets/create/",
        TicketCreateView.as_view(),
        name="create_ticket"
    ),
    path("reviews/create/", create_review, name="create_review"),
    path(
        "reviews/create/<int:ticket_id>/",
        create_review,
        name="create_review_from_ticket"
    ),
    path(
        "tickets/update/<int:ticket_id>/",
        update_ticket,
        name="update_ticket"
    ),
    path(
        "reviews/update/<int:review_id>/",
        update_review,
        name="update_review"
    ),
    path("reviews/<int:review_id>/", review_detail, name="review_detail"),
    path("followings/", followings, name="followings"),
    path("posts/", PostsView.as_view(), name="posts"),
    path(
        "followings/unfollow/<int:user_id>/", unfollow_user, name="unfollow"
    )
]
