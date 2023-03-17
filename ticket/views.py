from itertools import chain
from django.contrib.auth.decorators import login_required
from django.db.models import Q, OuterRef, Exists
from django.db.models import CharField, Value
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.contrib.auth import get_user_model
from . import forms, models

User = get_user_model()


@login_required
def create_ticket(request):
    ticket_form = forms.TicketForm()
    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('feed')
    context = {
        'ticket_form': ticket_form,
    }
    return render(request, 'ticket/ticket_form.html', context=context)


@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    edit_form = forms.TicketForm(instance=ticket)
    delete_form = forms.DeleteForm()
    if request.method == 'POST':
        if 'edit_ticket' in request.POST:
            edit_form = forms.TicketForm(request.POST, instance=ticket, files=request.FILES)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('feed')
        if 'delete' in request.POST:
            delete_form = forms.DeleteForm(request.POST)
            if delete_form.is_valid():
                ticket.delete()
                return redirect('feed')
    context = {
        'edit_form': edit_form,
        'delete_form': delete_form,
    }
    return render(request, 'ticket/edit_ticket.html', context=context)


@login_required
def create_review(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    review_form = forms.ReviewForm()
    if request.method == 'POST':
        review_form = forms.ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect('feed')
    context = {
        'review_form': review_form,
    }
    return render(request, 'ticket/review_form.html', context=context)


@login_required
def edit_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    edit_form = forms.ReviewForm(instance=review)
    delete_form = forms.DeleteForm()
    if request.method == 'POST':
        if 'edit_review' in request.POST:
            edit_form = forms.ReviewForm(request.POST, instance=review, files=request.FILES)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('feed')
        if 'delete' in request.POST:
            delete_form = forms.DeleteForm(request.POST)
            if delete_form.is_valid():
                review.delete()
                return redirect('feed')
    context = {
        'edit_form': edit_form,
        'delete_form': delete_form,
    }
    return render(request, 'ticket/edit_review.html', context=context)


@login_required
def create_review_and_ticket(request):
    review_form = forms.ReviewForm()
    ticket_form = forms.TicketForm()
    if request.method == 'POST':
        review_form = forms.ReviewForm(request.POST)
        ticket_form = forms.TicketForm(request.POST, files=request.FILES)
        if review_form.is_valid() or ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.ticket = ticket
            review.user = request.user
            review.save()
            return redirect('feed')
    context = {
        'review_form': review_form,
        'ticket_form': ticket_form,
    }
    return render(request, 'ticket/create_ticket_and_review.html', context=context)


@login_required
def my_posts(request):
    reviews = get_my_reviews(request)
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))
    tickets = get_my_tickets(request)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )
    return render(request, 'ticket/my_posts.html', context={'posts': posts})


@login_required
def follow_index(request):
    followed_users = User.objects.filter(followed_by__user=request.user)
    followed_by = User.objects.filter(following__followed_user=request.user)
    if request.method == 'POST':
        form = forms.AddUserToFollow(
            data=request.POST, initial={'user': request.user}
        )
        if form.is_valid():
            form.save()
            return redirect('followed_users')
    else:
        form = forms.AddUserToFollow(initial={'user': request.user})
    context = {
        'form': form,
        'followed_users': followed_users,
        'followed_by': followed_by,
    }
    return render(request, 'ticket/view_follow_users.html', context=context)


@login_required
@require_POST
def unfollow(request, user_id):
    if request.method == 'POST':
        userfollow_to_delete = get_object_or_404(models.UserFollows, user=request.user,
                                                 followed_user=user_id)
        userfollow_to_delete.delete()
        return redirect('followed_users')
    else:
        return redirect('followed_users')


@login_required
def feed(request):
    reviews = get_users_viewable_reviews(request)
    reviews = reviews.annotate(content_type=Value('REVIEW', CharField()))

    tickets = get_users_viewable_tickets(request)
    tickets = tickets.annotate(content_type=Value('TICKET', CharField()))
    user_review = models.Review.objects.filter(ticket=OuterRef('pk'), user=request.user)
    tickets = tickets.annotate(user_has_reviewed=Exists(user_review))

    # combine and sort the two types of posts
    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True
    )
    return render(request, 'feed.html', context={'posts': posts})


def get_users_viewable_reviews(request):
    return models.Review.objects.filter(Q(user=request.user) |
                                        Q(user__followed_by__user=request.user) |
                                        Q(ticket__user=request.user))


def get_users_viewable_tickets(request):
    return models.Ticket.objects.filter(Q(user=request.user) |
                                        Q(user__followed_by__user=request.user)
                                        )


def get_my_reviews(request):
    return models.Review.objects.filter(Q(user=request.user))


def get_my_tickets(request):
    return models.Ticket.objects.filter(Q(user=request.user))
