from django import forms
from . import models

CHOICES = (
    ("1",1),
    ("2",2),
    ("3",3),
    ("4",4),
    ("5",5)
)

class TicketForm(forms.ModelForm):
    edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = models.Ticket
        fields = ['title','description','image']

class DeleteTicketForm(forms.Form):
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)

class ReviewForm(forms.ModelForm):
    edit_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    rating = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="Note")

    class Meta:
        model = models.Review
        fields = ['headline','rating','body']

class DeleteReviewForm(forms.Form):
    delete_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)
