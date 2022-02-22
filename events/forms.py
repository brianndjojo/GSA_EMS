from django import forms
from django.db import models
from django.db.models import fields
from users.models import User, UserProfile, Venue, Event,  Signup
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth import get_user_model # Returns the active model within this project.
# Creating Form Template.. Similar to models    


# Customize UserCreationForm since Django automatically uses the built-in Django User-Model.
# We customize it to use our own active User
class EventInputForm(forms.ModelForm):
    # Meta specifies information about the form.
     class Meta:
        model = Event # Returns the User Model that is active in this project.
        fields = {
            "venue",
            "event_title",
            "event_date",
            "rule_list",
            "capacity",
            "event_price",
            "available",
            "event_desc"
        }


#For signing up an event..
class EventSignupForm(forms.ModelForm):
    class Meta:
        model = Signup 
        fields = {
            "user",
            "event",
            "is_registered"
        }

#For checking in & checking out of event
class UserInputForm(forms.Form):
    username = forms.CharField(max_length=20)


   
    




