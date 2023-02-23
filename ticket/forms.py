from django import forms
from . import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import UserFollows

User = get_user_model()


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

class DeleteForm(forms.ModelForm):
    delete = forms.BooleanField(widget=forms.HiddenInput, initial=True)

class ReviewForm(forms.ModelForm):
    edit_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    rating = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label="Note")

    class Meta:
        model = models.Review
        fields = ['headline','rating','body']

class DeleteReviewForm(forms.Form):
    delete_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)

class AddUserToFollow(forms.ModelForm):
    username = forms.CharField(label='Suivre un utilisateur', required = True)

    class Meta:
        model = models.UserFollows
        fields = ('user',)
        widgets = {
            "user": forms.HiddenInput(),
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        user = self.cleaned_data['user']
        try:
            followed_user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise ValidationError("L'utilisateur %(username)s n'existe pas.", params = {'username': username})
        if UserFollows.objects.filter(user=user, followed_user=followed_user).exists():
            raise ValidationError("Vous suivez déjà %(username)s.", params = {'username': username})
        return followed_user

    def save(self, commit=True):
        self.instance.followed_user = self.cleaned_data['username']
        return super().save(commit=commit)




