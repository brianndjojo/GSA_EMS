# Create your models here.
from email.policy import default
from enum import unique
from django.db import models

#AbstractUser allows us to create our own user-model..
#AbstractUser models are complete with base user fields and full feature with admin compliant permissions.
from django.contrib.auth.models import AbstractUser
# Create your models here.

# Signals are basically actions that automatically fires when certain events take place.
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
#pre_save used to add new info to DB before data is comitted to DB.
#post_save used to add new info to DB when data is already comitted to DB.

from django.core.validators import RegexValidator
from django.core.validators import MaxValueValidator, MinValueValidator

class User(AbstractUser):
    # Fields below determien what type of user you are..
    email = models.EmailField(unique=True)
    is_organizer = models.BooleanField(default=False) # Determines whether you are an Organizer.
     #https://stackoverflow.com/questions/19130942/whats-the-best-way-to-store-phone-number-in-django-models
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, unique = True) # validators should be a list
    is_blacklist = models.BooleanField(default=False)
    organisation_name = models.CharField(max_length=20, null=True, default="None")
    is_regular = models.BooleanField(default=False)
    is_beginner = models.BooleanField(default=False)
    rfid = models.CharField(max_length=100, blank=True)
    
# User Profile manages all details for users.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.user.username

class Venue(models.Model):
    venue_title = models.CharField(null = True, max_length=20)

    venue_address = models.CharField(max_length=20)
    
  
    venue_desc = models.CharField(null = True, max_length=200)
    venue_rules = models.CharField(null = True, max_length=200)

    # Since we allow Venue to be unassigned we should track the Organisation that the Venue belongs to.
    organisation = models.ForeignKey("UserProfile", null=True, blank=True, on_delete=models.CASCADE)


    def __str__(self):
        # format to return multiple features together..
        return f"{self.venue_title}"

class Event(models.Model):
    venue = models.ForeignKey("Venue", null=True, blank=True, on_delete=models.CASCADE)
    # Event hosted by user assigned as organizer.
    organisation = models.ForeignKey("UserProfile", null=True, blank=True, on_delete=models.CASCADE)
    event_title = models.CharField(max_length=20)
    event_date = models.DateField()
    rule_list = models.CharField(null = True, blank = True, max_length=200)
    capacity = models.IntegerField(default=0)
    current_capacity = models.IntegerField(default=0)
    event_price = models.IntegerField(default=0)
    available = models.BooleanField(default = True)
    event_desc = models.CharField(max_length=200, blank= True, null=True)
    # returns objects in string format
    def __str__(self):
        return f"{self.event_title}"

    

class Signup(models.Model):
    # usercs can have many signups
    user = models.ForeignKey("UserProfile", null=True, blank=True, on_delete=models.SET_NULL)

    
    # Event specified for signup
    event = models.ForeignKey("Event", null=True, blank=True, on_delete=models.CASCADE)
    # Sign up status to indicate whether signed up or not
    is_registered = models.BooleanField(default=False)
    # Checkin status for specific user.
    is_checkedin = models.BooleanField(default=False)
    # Team-assigned to player
    # 0 = Team Blue, 1 = Team Red
    team = models.IntegerField(default=0, validators=[
            MaxValueValidator(1),
            MinValueValidator(0)
        ])

    # to check whether user has paid.
    is_paid = models.BooleanField(null = True, default=False)


    amount = models.IntegerField(default=0)
    description = models.CharField(max_length=20, null=True, blank=True)
    attachments = models.CharField(max_length=20,blank=True)
    # returns objects in string format
    def __str__(self):
        return f"{self.user} {self.event} {self.is_checkedin}"




# Changes to be implemented to User DB when User instance is created/edited.
def post_user_created_signal(sender, instance, created, **kwargs):
    # created is used to check whether an instance is created at the very moment this function is called.
    print(instance, created)

    # Creates UserProfile only when a new User is created. Otherwise, no point.
    if created:
        UserProfile.objects.create(user = instance)


# Changes to be implemented to Event DB when Event instance is created/edited.
@receiver(post_save, sender=Event)
def post_event_created_signal(sender, instance, created, **kwargs):
    if created:

        instance.current_capacity=instance.capacity
        print('current capacity:',instance.current_capacity)
        instance.save()

# Changes to be implemented to Event DB when Event instance is created/edited.
@receiver(post_save, sender=Signup)
def post_signup_created_signal(sender, instance, created, **kwargs):
    if created:
        if(instance.event.current_capacity > 0):
            instance.amount = instance.amount + instance.event.event_price
            print('current capacity:',instance.event.event_price)
            instance.save()
     
     

# Django includes a “signal dispatcher” which helps allow decoupled applications get notified when actions occur elsewhere in the framework.
# https://docs.djangoproject.com/en/4.0/ref/signals/#post-save
# https://stackoverflow.com/questions/35949755/django-when-should-i-use-signals-and-when-should-i-override-save-method
post_save.connect(post_user_created_signal, sender=User)
post_save.connect(post_event_created_signal, sender=Event)
post_save.connect(post_signup_created_signal, sender=Signup)
