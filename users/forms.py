from django import forms
from django.db import models
from .models import User, UserProfile, Venue, Event, Signup
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth import get_user_model # Returns the active model within this project.

# Creating Form Template.. Similar to models    

# Inherit from Model to make a form
class UserModelForm(forms.ModelForm):
    # Meta specifies information about the form.
    class Meta:
        model = get_user_model()
        fields = {
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'is_blacklist',
            'is_organizer',
            'organisation_name',
            'is_regular',
            'is_beginner'
        }

# Customize UserCreationForm since Django automatically uses the built-in Django User-Model.
# We customize it to use our own active User
class CustomCreationForm(UserCreationForm):
    # Meta specifies information about the form.
     class Meta:
        model = get_user_model() # Returns the User Model that is active in this project.
        fields = {
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number"
        }
        field_classes = {'username': UsernameField}

# For admin to input RFID
class RfidInputForm(forms.ModelForm):
    # Meta specifies information about the form.
    class Meta:
        model = User
        fields = {
            'rfid'
        }

