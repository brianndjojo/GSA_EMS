# Create your models here.
from django.db import models

#AbstractUser allows us to create our own user-model..
#AbstractUser models are complete with base user fields and full feature with admin compliant permissions.
from django.contrib.auth.models import AbstractUser
# Create your models here.

# Signals are basically actions that automatically fires when certain events take place.
from django.db.models.signals import post_save, pre_save
#pre_save used to add new info to DB before data is comitted to DB.
#post_save used to add new info to DB when data is already comitted to DB.



class User(AbstractUser):
    # Fields below determien what type of user you are..
    is_organizer = models.BooleanField(default=False) # Determines whether you are an Organizer.
    oragnisation_name = models.CharField(max_length=20, null=True, blank=True)
    

# User Profile manages all details for users.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username

class Venue(models.Model):
    venue_address = models.CharField(max_length=20)
    
    venue_price = models.IntegerField(default=0)
    #on_delete handles when foreign key is no longer available..
    #CASCADE: when agent is deleted, this lead is dseleted.

    # Since we allow Venue to be unassigned we should track the Organisation that the Venue belongs to.
    organisation = models.ForeignKey("UserProfile", null=True, blank=True, on_delete=models.CASCADE)


    def __str__(self):
        # format to return multiple features together..
        return f"{self.venue_address} {self.venue_price}"

class Event(models.Model):
    venue = models.ForeignKey("Venue", null=True, blank=True, on_delete=models.CASCADE)
    # Event hosted by user assigned as organizer.
    organisation = models.ForeignKey("UserProfile", null=True, blank=True, on_delete=models.CASCADE)
    event_title = models.CharField(max_length=20)
    event_date = models.DateField()

    capacity = models.IntegerField(default=0)
    # returns objects in string format
    def __str__(self):
        return f"{self.venue} {self.capacity} {self.event_date}"

    
                                            

class Invoice(models.Model):
    # Member ID for the invoice given to
    user = models.ForeignKey("UserProfile", null=True, blank=True, on_delete=models.CASCADE)
    
    amount = models.IntegerField(default=0)
    description = models.CharField(max_length=20, null=True, blank=True)
    attachments = models.CharField(max_length=20)
    # returns objects in string format
    def __str__(self):
        return self.user.username

class Signup(models.Model):
    # usercs can have many signups
    user = models.ForeignKey("UserProfile", null=True, blank=True, on_delete=models.SET_NULL)
    # invoice for signup
    invoice = models.ForeignKey("Invoice", null=True, blank=True, on_delete=models.SET_NULL)
    # Event specified for signup
    event = models.ForeignKey("Event", null=True, blank=True, on_delete=models.SET_NULL)
    # Sign up status to indicate whether signed up or not
    is_registered = models.BooleanField(default=False)

    # returns objects in string format
    def __str__(self):
        return f"{self.user} {self.event}"

class Checkin(models.Model):
    # Signup to check sign up details
    signup = models.OneToOneField("Signup", on_delete=models.CASCADE)
    # Member
    user = models.ForeignKey("UserProfile", null=True, blank=True, on_delete=models.SET_NULL)
    # returns objects in string format
    def __str__(self):
        return self.user.username

# Changes to be implemented to User DB when User instance is created/edited.
def post_user_created_signal(sender, instance, created, **kwargs):
    # created is used to check whether an instance is created at the very moment this function is called.
    print(instance, created)

    # Creates UserProfile only when a new User is created. Otherwise, no point.
    if created:
        UserProfile.objects.create(user = instance)

post_save.connect(post_user_created_signal, sender=User)

