from itertools import chain
from django.shortcuts import HttpResponseRedirect, render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import View, ListView, CreateView, UpdateView
from django.db.models import CharField, Value, Exists, OuterRef
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from authentication.models import User, UserFollows
from .models import Ticket, Review
from .forms import TicketForm, ReviewForm, UserFollowForm
from .utils import get_users_viewable_reviews, get_users_viewable_tickets


@login_required
def posts_view(request):
    reviews = request.user.review_set.all()
    reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))
    tickets = request.user.ticket_set.all()
    tickets = tickets.annotate(content_type=Value("TICKET", CharField()))
    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )
    return render(
        request,
        "main_feed/posts.html",
        context={"post": posts}
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
def update_ticket(request, ticket_id):
    ticket = Ticket.get_object_or_404(
        Ticket, id=ticket_id
        )
    update_ticket = forms.TicketForm(
        instance=ticket
        )
    delete_ticket = forms.DeleteTicketForm()

    if request.method == "POST":
        if "update_ticket" in request.POST:
            update_form = forms.TicketForm(
                request.POST, instance=ticket
                )

            if update_form.is_valid():
                update_form.save()
                return redirect("homepage")

            if "delete_ticket" in request.POST:
                delete_form = forms.DeleteTicketForm(
                    request.POST
                    )
                if delete_form.is_valid():
                    ticket.delete()
                    return redirect("homepage")

    context = {
        "update_ticket": update_ticket,
        "delete_ticket": delete_ticket
    }
    return render(
        request,
        "main_feed/update_ticket.html",
        context=context
        )


@login_required
def followings(request):
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
