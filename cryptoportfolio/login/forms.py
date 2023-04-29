from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class UserAuthForm(AuthenticationForm):
    class Meta:
        model = User
        fields = {'username', 'password'}


class UserRegForm(UserCreationForm):
    class Meta:
        model = User
        fields = {'username', 'password1', 'password2'}
