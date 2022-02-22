# Register your models here.
from django.contrib import admin

# Register your models here.
from .models import User, UserProfile, Signup,  Event, Venue



# Must Register Models so that it appears in Admin Dashboard.
admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Event)
admin.site.register(Venue)
admin.site.register(Signup)


