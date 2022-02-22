from django import forms
from django.db import models
from users.models import User, UserProfile, Venue, Event,  Signup
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth import get_user_model # Returns the active model within this project.
# Creating Form Template.. Similar to models    

# Inherit from Model to make a form
class VenueModelForm(forms.ModelForm):
    # Meta specifies information about the form.
    class Meta:
        model = Venue
        fields = {
            'venue_address',
            "venue_title",
            "venue_address",
            "venue_desc",
            "venue_rules",
        }

# Customize UserCreationForm since Django automatically uses the built-in Django User-Model.
# We customize it to use our own active User
class VenueCreationForm(forms.ModelForm):
    # Meta specifies information about the form.
     class Meta:
        model = Venue # Returns the User Model that is active in this project.
        fields = {
            "venue_title",
            "venue_address",
            "venue_desc",
            "venue_rules",
        }
    




