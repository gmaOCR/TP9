from itertools import chain
from django.db import models
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.forms import formset_factory
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from . import forms, models

@login_required
def home(request):
    tickets = models.Ticket.objects.all()
    reviews = models.Review.objects.all()
    context = {
        'tickets': tickets,
        'reviews': reviews,
    }
    return render(request, 'ticket/home.html',  context=context)

@login_required
def create_ticket(request):
    ticket_form = forms.TicketForm()
    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        if ticket_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('home')
    context = {
        'ticket_form': ticket_form,
    }
    return render(request, 'ticket/create_ticket_post.html', context=context)

@login_required
@permission_required('ticket.view_ticket', raise_exception=True)
def view_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    return render(request, 'ticket/view_ticket.html', {'ticket': ticket})

@login_required
@permission_required('ticket.change_ticket', raise_exception=True)
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    edit_form = forms.TicketForm(instance=ticket)
    delete_form = forms.DeleteTicketForm()
    if request.method == 'POST':
        if 'edit_ticket' in request.POST:
            edit_form = forms.TicketForm(request.POST, instance=ticket, files=request.FILES)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('home')
        if 'delete_ticket' in request.POST:
            delete_form = forms.DeleteTicketForm(request.POST)
            if delete_form.is_valid():
                ticket.delete()
                return redirect('home')
    context = {
        'edit_form': edit_form,
        'delete_form': delete_form,
    }
    return render(request, 'ticket/edit_ticket.html', context=context)

@login_required
# @permission_required
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
            return redirect('home')
    context = {
        'review_form': review_form,
        'ticket_form': ticket_form,
    }
    return render(request, 'ticket/create_ticket_and_review.html', context=context)

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
            return redirect('home')
    context = {
        'review_form': review_form,
    }
    return render(request, 'ticket/create_review.html', context=context)

@login_required
# @permission_required('ticket.change_review', raise_exception=True)
def edit_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    edit_form = forms.ReviewForm(instance=review)
    delete_form = forms.DeleteReviewForm()
    if request.method == 'POST':
        if 'edit_review' in request.POST:
            edit_form = forms.ReviewForm(request.POST, instance=review, files=request.FILES)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('home')
        if 'delete_review' in request.POST:
            delete_form = forms.DeleteReviewForm(request.POST)
            if delete_form.is_valid():
                review.delete()
                return redirect('home')
    context = {
        'edit_form': edit_form,
        'delete_form': delete_form,
    }
    return render(request, 'ticket/edit_review.html', context=context)

@login_required
def followed_users(request):
    form = forms.FollowedUsersForm(instance=request.user)
    if request.method == 'POST':
        form = forms.FollowedUsersForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'ticket/follow_users_form.html', context={'form': form})

@login_required
def view_followed_users(request):
    users_followed = models.UserFollows.objects.all()
    context = {
        'users_f': users_followed,
    }
    return render(request, 'ticket/view_followed_users.html', context=context)



