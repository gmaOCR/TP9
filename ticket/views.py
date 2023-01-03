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
    return render(request, 'ticket/home.html',  context={'tickets': tickets})

@login_required
def create_ticket(request):
    ticket_form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user =request.user
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


