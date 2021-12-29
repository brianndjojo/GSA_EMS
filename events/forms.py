from django import forms
from django.db import models
from django.db.models import fields
from users.models import User, UserProfile, Venue, Event,  Signup, Invoice
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth import get_user_model # Returns the active model within this project.
# Creating Form Template.. Similar to models    

# Inherit from Model to make a form
class EventModelForm(forms.ModelForm):
    # Meta specifies information about the form.
    class Meta:
        model = Event
        fields = {
            'venue',
            'event_title',
            'event_date',
            'capacity',
        }

# Customize UserCreationForm since Django automatically uses the built-in Django User-Model.
# We customize it to use our own active User
class EventCreationForm(forms.ModelForm):
    # Meta specifies information about the form.
     class Meta:
        model = Event # Returns the User Model that is active in this project.
        fields = {
            "venue",
            "event_title",
            "event_date",
            "capacity"
        }



class EventSignupForm(forms.ModelForm):
    class Meta:
        model = Signup 
        fields = {
            "user",
            "invoice",
            "event",
            "is_registered"
        }

class UserInputForm(forms.Form):
    username = forms.CharField(max_length=20)


   
    




