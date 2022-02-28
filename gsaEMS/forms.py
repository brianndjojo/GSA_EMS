from pyexpat import model
from django import forms
from django.db import models
from users.models import User, UserProfile, Venue, Event, Signup
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth import get_user_model # Returns the active model within this project.
from django.contrib.auth.forms import PasswordChangeForm

class UpdateAccountForm(forms.ModelForm):
    # Meta specifies information about the form.
    class Meta:
        model = get_user_model()
        fields = {
            'first_name',
            'last_name',
            'email',
            'phone_number'
        }

class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form control', 'type': 'password'}))
    new_password1 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password1 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))

    class Meta:
        model = User
        fields = ('old_password', 'new_password', 'new_password2')