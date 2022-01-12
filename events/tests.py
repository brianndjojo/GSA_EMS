import datetime

from django.test import TestCase
from django.utils import timezone

from users.models import User, UserProfile, Event, Signup, Venue, Invoice

# To be written once development is done..
# Not recommended though, a better way is to start development with given tests in mind...