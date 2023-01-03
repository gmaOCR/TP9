# from django.contrib.auth import get_user_model
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

from . import models

class TicketForm(forms.ModelForm):
    edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = models.Ticket
        fields = ['title','description','image']

class DeleteTicketForm(forms.Form):
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)

# class UploadProfilePhotoForm(forms.ModelForm):
#     class Meta:
#         model = get_user_model()
#         fields = ('profile_photo', )
