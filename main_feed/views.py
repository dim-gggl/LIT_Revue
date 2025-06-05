from itertools import chain
from django.shortcuts import (
    HttpResponseRedirect, redirect, render, get_object_or_404)
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView
from django.db.models import CharField, Value
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from authentication.models import User, UserFollows
from .models import Ticket, Review
from .forms import (
    TicketForm,
    ReviewForm,
    UserFollowForm,
    DeleteReviewForm,
    DeleteTicketForm,
    CommentForm
)


class HomeView(LoginRequiredMixin, ListView):
    """
    HomeView displays a combined feed of reviews and tickets
    for the logged-in user and users they follow.

    Inherits:
        LoginRequiredMixin: Ensures the user is authenticated.
        ListView: Provides list display functionality.

    Attributes:
        template_name (str): The template used to render the home
        feed.
        context_object_name (str): The context variable name for
        the posts in the template.

    Methods:
        get_queryset():
            Retrieves and returns a sorted list of Review and
            Ticket objects created by the current user and users
            they follow.
            Each object is annotated with a 'content_type'
            field indicating whether it is a 'REVIEW' or 'TICKET'.
            The combined list is sorted in descending order
            by creation time.
    """
    template_name = "main_feed/home.html"
    context_object_name = "posts"

    def get_queryset(self):
        """
        Returns a combined and chronologically ordered list
        of Review and Ticket objects
        created by the current user and users they follow.
        Each object in the list is
        annotated with a 'content_type' field indicating
        whether it is a 'REVIEW' or a 'TICKET'.

        Returns:
            list: A list of Review and Ticket objects sorted
            by 'time_created' in descending order.
        """
        followee_ids = self.request.user.following.values_list(
            "id", flat=True
        )
        user_ids = list(followee_ids) + [self.request.user.id]
        reviews = Review.objects.filter(
            user_id__in=user_ids).order_by("-time_created")
        reviews = reviews.annotate(
            content_type=Value("REVIEW", output_field=CharField()))
        tickets = Ticket.objects.filter(
            user_id__in=user_ids).order_by("-time_created")
        tickets = tickets.annotate(
            content_type=Value("TICKET", output_field=CharField()))
        posts = sorted(
            chain(
                reviews, tickets
            ), key=lambda post: post.time_created, reverse=True)
        return posts


class PostsView(LoginRequiredMixin, ListView):
    """
    PostsView displays a list of the current user's posts,
    including both reviews and tickets.

    This view combines Review and Ticket objects created by
    the logged-in user, annotates each with a 'content_type'
    field to distinguish between reviews and tickets, and
    orders them by creation time in descending order.

    Attributes:
        template_name (str): The template used to render the
        posts.
        context_object_name (str): The context variable name
        for the posts in the template.

    Methods:
        get_queryset():
            Retrieves and returns a sorted list of the user's
            reviews and tickets, each annotated with a
            'content_type'
            to indicate its type, ordered by 'time_created'
            in descending order.
    """
    template_name = "main_feed/posts.html"
    context_object_name = "personal_posts"

    def get_queryset(self):
        reviews = Review.objects.filter(
            user=self.request.user).order_by("-time_created")
        reviews = reviews.annotate(
            content_type=Value("REVIEW", output_field=CharField()))
        tickets = Ticket.objects.filter(
            user=self.request.user).order_by("-time_created")
        tickets = tickets.annotate(
            content_type=Value("TICKET", output_field=CharField()))
        personal_posts = sorted(
            chain(reviews, tickets),
            key=lambda personal_post: personal_post.time_created,
            reverse=True
        )
        return personal_posts


class TicketCreateView(LoginRequiredMixin, CreateView):
    """
    TicketCreateView is a Django class-based view that
    allows authenticated users to create new Ticket instances.

    Inherits:
        LoginRequiredMixin: Ensures that only logged-in
        users can access this view.
        CreateView: Provides the logic for displaying a
        form for creating a new object and saving it.

    Attributes:
        model (Ticket): The model associated with this
        view.
        fields (tuple): The fields of the Ticket model
        to be displayed in the form ('title', 'description',
        'image').
        template_name (str): The path to the template used
        to render the form.
        success_url (str): The URL to redirect to upon
        successful creation of a Ticket.

    Methods:
        form_valid(form):
            Assigns the currently logged-in user to the
            Ticket instance before saving.
            Redirects to the success URL upon successful
            form submission.
    """
    model = Ticket
    fields = ('title', 'description', 'image')
    template_name = 'main_feed/create_ticket.html'
    success_url = reverse_lazy('homepage')

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())


@login_required
def create_review(request, ticket_id=None):
    """
    Handle the creation of a review, either for an existing
    ticket or by creating a new ticket and review simultaneously.

    If a `ticket_id` is provided, the view allows the user
    to create a review for the specified ticket, provided that a
    review does not already exist for it. If a review already exists
    for the ticket, the user is redirected to the homepage.

    If no `ticket_id` is provided, the view allows the user
    to create both a new ticket and a review in a single form submission.

    Args:
        request (HttpRequest): The HTTP request object.
        ticket_id (int, optional): The ID of the ticket to review.
        Defaults to None.

    Returns:
        HttpResponse: Renders the review creation template or
        redirects to the homepage upon successful creation.
    """

    if ticket_id:
        ticket = get_object_or_404(Ticket, pk=ticket_id)
        if Review.objects.filter(ticket=ticket).exists():
            return redirect("homepage")

        form = ReviewForm(request.POST or None)

        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect("homepage")

        return render(
            request,
            "main_feed/create_review.html",
            context={
                "form": form,
                "ticket": ticket,
            }
        )

    ticket_form = TicketForm(
        request.POST or None,
        request.FILES or None
    )
    review_form = ReviewForm(
        request.POST or None
    )

    if ticket_form.is_valid() and review_form.is_valid():
        ticket = ticket_form.save(commit=False)
        ticket.user = request.user
        ticket.save()

        review = review_form.save(commit=False)
        review.user = request.user
        review.ticket = ticket
        review.save()
        return redirect("homepage")

    return render(
        request,
        "main_feed/create_review.html",
        context={
            "ticket_form": ticket_form,
            "review_form": review_form,
        }
    )


@login_required
def review_detail(request, review_id):
    """
    Display the details of a specific review and handle
    comment submission.

    Args:
        request (HttpRequest): The HTTP request object.
        review_id (int): The ID of the review to display.

    Returns:
        HttpResponse: The rendered review detail page with
        associated comments and a comment form.
        If a valid comment is submitted via POST, redirects
        to the same review detail page.
    """
    review = get_object_or_404(Review, id=review_id)
    comments = review.comments.all().order_by("time_created")
    form = CommentForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.review = review
        new_comment.author = request.user
        new_comment.save()
        return redirect("review_detail", review_id=review.id)

    return render(
        request,
        "main_feed/review_detail.html",
        {
            "review": review,
            "comments": comments,
            "form": form
        }
    )


@login_required
def update_ticket(request, ticket_id):
    """
    Handle the update and deletion of a Ticket instance.

    This view supports both updating and deleting a ticket,
    depending on the form submitted.
    - If the request method is POST and the 'update_ticket'
    button is pressed, it validates and saves the updated ticket data.
    - If the 'delete_ticket' button is pressed, it validates
    and deletes the ticket.
    - On GET requests, it displays the update and delete
    forms pre-filled with the ticket's current data.

    Args:
        request (HttpRequest): The HTTP request object.
        ticket_id (int): The ID of the ticket to update or delete.

    Returns:
        HttpResponse: Renders the update_ticket template with the
        forms, or redirects to the homepage after a successful update
        or deletion.
    """
    ticket = get_object_or_404(Ticket, id=ticket_id)
    update_form = TicketForm(instance=ticket)
    delete_form = DeleteTicketForm()
    if request.method == "POST":
        if "update_ticket" in request.POST:
            form = TicketForm(request.POST, instance=ticket)
            if form.is_valid():
                form.save()
                return redirect("homepage")

        if "delete_ticket" in request.POST:
            form = DeleteTicketForm(request.POST)
            if form.is_valid():
                ticket.delete()
                return redirect("homepage")

    context = {
        "update_form": update_form,
        "delete_form": delete_form
    }
    return render(
        request,
        "main_feed/update_ticket.html",
        context
    )


@login_required
def update_review(request, review_id):
    """
    Handle the update and deletion of a Review instance.

    This view supports both updating and deleting a review,
    depending on the submitted form.
    - If the request method is POST and the 'update_review'
    button is pressed, it validates and saves the updated review.
    - If the 'delete_review' button is pressed, it validates
    and deletes the review.
    - On GET requests, it displays the forms pre-filled with
    the current review data.

    Args:
        request (HttpRequest): The HTTP request object.
        review_id (int): The primary key of the Review to
        update or delete.

    Returns:
        HttpResponse: The rendered update_review template with
        the forms, or a redirect to the homepage upon
        successful update or deletion.
    """
    review = get_object_or_404(
        Review, id=review_id
        )
    update_form = ReviewForm(
        instance=review
        )
    delete_form = DeleteReviewForm()

    if request.method == "POST":
        if "update_review" in request.POST:
            update_form = ReviewForm(
                request.POST, instance=review
                )

            if update_form.is_valid():
                update_form.save()
                return redirect("homepage")

        if "delete_review" in request.POST:
            delete_form = DeleteReviewForm(
                request.POST
                )
            if delete_form.is_valid():
                review.delete()
                return redirect("homepage")

    context = {
        "update_form": update_form,
        "delete_form": delete_form
    }
    return render(
        request,
        "main_feed/update_review.html",
        context=context
        )


@login_required
def followings(request):
    """
    Handle the followings page, allowing users to
    follow other users by username.

    - On GET: Displays the followings and followers
    of the current user, along with a form to follow new users.
    - On POST: Processes the follow form, validates
    the username, and creates a follow relationship if possible.
        - Shows appropriate messages for errors
        (e.g., user not found, self-follow) and success.
        - Redirects to the followings page after
        a successful follow attempt.

    Args:
            request (HttpRequest): The HTTP request object.

    Returns:
            HttpResponse: Rendered followings page with the form,
            current followings, and followers.
    """
    form = UserFollowForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        username = form.cleaned_data["username"]
        try:
            user_to_follow = User.objects.get(
                username=username
                )
            if user_to_follow == request.user:
                messages.error(
                    request,
                    "Vous ne pouvez pas vous suivre vous-même."
                )
            else:
                obj, created = UserFollows.objects.get_or_create(
                    user=request.user,
                    followed_user=user_to_follow
                )
                if created:
                    messages.success(
                        request,
                        f"Vous suivez maintenant {username}."
                    )
                else:
                    messages.info(
                        request,
                        f"Vous suivez déjà {username}."
                    )
                return redirect("followings")

        except User.DoesNotExist:
            messages.error(
                request,
                "Utilisateur introuvable."
            )
    following = request.user.following.all()
    followers = request.user.followers.all()
    return render(
        request,
        "main_feed/followings.html",
        context={
            "form": form,
            "following": following,
            "followers": followers,
        }
    )


@login_required
def unfollow_user(request, user_id):
    """
    Handles the process of unfollowing a user.

    If the target user is the same as the requesting
    user, an error message is displayed.
    Otherwise, attempts to remove the follow relationship
    between the requesting user and the target user.
    Displays a success message if the unfollow action was
    successful, or an informational message if the user was
    not being followed.

    Redirects the user to the "followings" page.

    Args:
        request (HttpRequest): The HTTP request object.
        user_id (int): The primary key of the user to unfollow.

    Returns:
        HttpResponseRedirect: Redirects to the "followings"
        page.
    """
    target = get_object_or_404(User, pk=user_id)
    if target == request.user:
        messages.error(
            request, "Se désabonner de soi-même ? Joker."
            )
    else:
        deleted, _ = UserFollows.objects.filter(
            user=request.user,
            followed_user=target
        ).delete()
        if deleted:
            messages.success(
                request,
                f"Vous ne suivez plus {target.username}."
            )
        else:
            messages.info(
                request,
                f"Vous ne suiviez déjà plus {target.username}."
            )
    return redirect("followings")
