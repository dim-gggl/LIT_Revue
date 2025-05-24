from itertools import chain
from django.shortcuts import HttpResponseRedirect, render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import View, ListView, CreateView
from django.db.models import CharField, Value, Exists, OuterRef
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from authentication.models import User
from .models import Ticket, Review
from .forms import TicketForm, ReviewForm
from .utils import get_users_viewable_reviews, get_users_viewable_tickets


@login_required
def home(request):
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
    return render(
        request,
        "main_feed/home.html",
        context={"posts": posts}
        )

class HomeView(LoginRequiredMixin, ListView):
    template_name = "main_feed/home.html"
    context_object_name = "posts"

    def get_queryset(self):
        reviews = get_users_viewable_reviews(self.request.user)
        # returns queryset of reviews
        reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))
        tickets = get_users_viewable_tickets(self.request.user)
        # returns queryset of tickets
        tickets = tickets.annotate(content_type=Value("TICKET", CharField()))
        # combine and sort the two types of posts
        posts = sorted(
            chain(reviews, tickets),
            key=lambda post: post.time_created,
            reverse=True
        )
        return posts


@login_required
def create_ticket(request):
    form = TicketForm(
            request.POST or None,
            request.FILES or None
            )

    if form.is_valid():
        ticket = form.save(commit=False)
        ticket.user = request.user
        ticket.save()
        return redirect("homepage")

    return render(
        request,
        "main_feed/create_ticket.html",
        context={"form": form}
        )

class TicketCreateView(LoginRequiredMixin, CreateView):
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

        return render(request,
        "main_feed/create_review.html", context={
            "form": form,
            "ticket": ticket,
        })

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
def feed(request):
    reviews = get_users_viewable_reviews(request.user)
    # returns queryset of reviews
    reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))
    tickets = get_users_viewable_tickets(request.user)
    # returns queryset of tickets
    tickets = tickets.annotate(content_type=Value("TICKET", CharField()))
    tickets = tickets.annotate(
        has_review=Exists(
            Review.objects.filter(
                ticket=OuterRef("pk")
                )
            )
        )
    # combine and sort the two types of posts
    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )
    return render(request,"main_feed/home.html", context={"posts": posts})
