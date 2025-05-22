from itertools import chain
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.db.models import CharField, Value
from authentication.models import User
from . import forms


@login_required
def home(request):
    return render(request, "main_feed/home.html")

@login_required
def create_ticket(request):
    form = forms.TicketForm

    if request.method == "POST":
        form = forms.TicketForm(
            request.POST,
            request.FILES
            )

        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect("home")

    return render(
        request,
        "main_feed/create_ticket.html",
        context={"form": form}
        )


@login_required
def create_review(request, ticket_id=None):

    if ticket_id:
        ticket = get_object_or_404(
            Ticket, pk=ticket_id
            )
        form = ReviewForm(request.POST or None)

        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect("home")

        return render(request,
        "main_feed/create_review.html", context={
            "form": form,
            "ticket": ticket,
        })

    ticket_form = forms.TicketForm(
        request.POST or None,
        request.FILES or None
        )
    review_form = forms.ReviewForm(
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
        return redirect("home")

    return render(
        request,
        "main_feed/create_review.html",
        context={
        "ticket_form": ticket_form,
        "review_form": review_form,
        }
    )

@login_required
def feed(request):
    reviews = get_users_viewable_reviews(request.user)
    # returns queryset of reviews
    reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))
    tickets = get_users_viewable_tickets(request.user)
    # returns queryset of tickets
    tickets = tickets.annotate(content_type=Value("TICKET", CharField()))
    # combine and sort the two types of posts
    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )
    return render(request,"main_feed/home.html", context={"posts": posts})
