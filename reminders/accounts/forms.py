from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')
        labels = {
            'username': 'Username (what you use to log in)',
            'email': 'Email address',
            'first_name': 'First name',
            'last_name': 'Last name',
        }
