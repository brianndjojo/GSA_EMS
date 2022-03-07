from django import forms
from django.db import models
from django.db.models import fields
from users.models import User, UserProfile, Venue, Event,  Signup
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth import get_user_model # Returns the active model within this project.
from django.core.validators import RegexValidator
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
            "team"
        }

#For checking in & checking out of event w/ Phone Number
class PhoneNumberInputForm(forms.Form):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = forms.CharField(validators=[phone_regex], max_length=17)

#For checking in & checking out of event w/ RFID
class RfidInputForm2(forms.Form):
    rfid = forms.CharField(max_length=17)


   
    




