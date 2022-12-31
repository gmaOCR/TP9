from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username',)

# class UploadProfilePhotoForm(forms.ModelForm):
#     class Meta:
#         model = get_user_model()
#         fields = ('profile_photo', )
