from itertools import chain
from django.db import models
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.forms import formset_factory
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

from . import forms, models

User = get_user_model()

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
def view_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    return render(request, 'ticket/view_ticket.html', {'ticket': ticket})

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
                return redirect('home')
        if 'delete_ticket' in request.POST:
            # delete_form = forms.DeleteTicketForm(request.POST)
            delete_form = forms.DeleteForm(request.POST)
            if delete_form.is_valid():
                ticket.delete()
                return redirect('home')
    context = {
        'edit_form': edit_form,
        'delete_form': delete_form,
    }
    return render(request, 'ticket/edit_ticket.html', context=context)

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
def edit_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    edit_form = forms.ReviewForm(instance=review)
    delete_form = forms.DeleteForm()
    # delete_form = forms.DeleteReviewForm()
    if request.method == 'POST':
        if 'edit_review' in request.POST:
            edit_form = forms.ReviewForm(request.POST, instance=review, files=request.FILES)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('home')
        if 'delete_review' in request.POST:
            # delete_form = forms.DeleteReviewForm(request.POST)
            delete_form = forms.DeleteForm(request.POST)
            if delete_form.is_valid():
                review.delete()
                return redirect('home')
    context = {
        'edit_form': edit_form,
        'delete_form': delete_form,
    }
    return render(request, 'ticket/edit_review.html', context=context)

@login_required
def follow_index(request):
    followed_users = User.objects.filter(followed_by__user=request.user)
    followed_by = User.objects.filter(following__followed_user=request.user)
    if request.method == 'POST':
        form = forms.AddUserToFollow(
            data= request.POST, initial={'user': request.user}
                         )
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = forms.AddUserToFollow(initial={'user': request.user})
    context = {
        'form': form,
        'followed_users': followed_users,
        'followed_by': followed_by,
    }
    return render(request, 'ticket/view_follow_users.html', context=context)

@login_required
def unfollow(request, followed_user_id):
    delete_form = forms.DeleteForm(request.POST)
    # if request.method == 'POST':
    #     if 'unfollow_user' in request.POST:
    if delete_form.is_valid():
        userfollow_to_delete = get_object_or_404(models.UserFollows,user=request.user,followed_user=followed_user_id)
        if userfollow_to_delete.exists():
            userfollow_to_delete.delete()
            return redirect('ticket/view_follow_users.html')
        return redirect('home')









