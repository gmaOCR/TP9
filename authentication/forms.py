from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class SignupForm(UserCreationForm):
    use_required_attribute = False
    # def __init__(self, *args, **kwargs):
    #     super(SignupForm, self).__init__(*args, **kwargs)
    #     self.field['username'].required = false

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        # fields = ('username','role')

        fields = ('username',)
