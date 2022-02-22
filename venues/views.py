from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from typing import List

from django.shortcuts import redirect, render, reverse
from django.core.mail import send_mail
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin


from users.rolemixin import OrganizerRequiredMixin

from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView

from .forms import VenueCreationForm, VenueModelForm
from users.models import UserProfile, User, Venue

# Create your views here.

# Filter Venues
def search_venue(request):
    venues = Venue.objects.all()
    search_filter = request.GET.get('specific-venue')
    print(search_filter)
    search_venue = venues.filter(venue_title = search_filter)
    if(search_venue.exists()):
        return venues.filter(venue_title = search_filter)
    return Venue.objects.all()

class VenueListView(LoginRequiredMixin, ListView):
    template_name = "venue_list.html"
    context_object_name = "venues"

    def get_queryset(self):
        # Filters out the queryset of agent-list specific to the same Organization..
        return  search_venue(self.request)

class VenueDetailView(LoginRequiredMixin, DetailView):
    # Specify template to be used
    template_name = "venue_detail.html"

    context_object_name = "venue"
    # Speicfy Query Set
    def get_queryset(self):
        return  Venue.objects.all()
        

class VenueCreateView(OrganizerRequiredMixin, CreateView):
    # Specify template to be used
    template_name = "venue_create.html"

    # Instead of Query, we specify the formclass to be used.
    form_class = VenueCreationForm

    # Specify what happens when form is successfully submitted.
    def get_success_url(self) -> str:
        return reverse("venues:venue-list")
    
    # form_valid function called in POST function of ProcessFormView.
    # Send email when form is submitted to create new Lead.
    # Overriding form_valid function/adding new funcitonality, specifically sending email.
    def form_valid(self, form):
        # Sends email with Django mail function
        send_mail(subject = "A new Event has been added",
            message = "A new Event has been added.", 
            from_email = "test@test.com",
            recipient_list=["test2@test.com"],
        )
        # Automatically saves organisation as user who created it.
        obj = form.save(commit=False)
        #obj.user = self.request.user.userprofile
        obj.organisation = self.request.user.userprofile
        obj.save()
    
        # Once email is sent return back to what the form was originally supposed to do.
        return super(VenueCreateView, self).form_valid(form)

class VenueUpdateView(OrganizerRequiredMixin, UpdateView):
    # Specify template to be used
    template_name = "venue_update.html"

    # Speicfy Query Set
    def get_queryset(self):
        # Filters out the queryset of agent-list specific to the same Organization..
        if self.request.user.is_superuser:
            return  Venue.objects.all()
        else:
            return  Venue.objects.filter(organisation = self.request.user.userprofile)
    # Instead of Query, we specify the formclass to be used.
    form_class = VenueModelForm

    # Specify what happens when form is successfully submitted.
    def get_success_url(self) -> str:
        return reverse("venues:venue-list")

class VenueDeleteView(OrganizerRequiredMixin, DeleteView):
    template_name = "venue_delete.html"
    def get_queryset(self):
        # Filters out the queryset of agent-list specific to the same Organization..
        if self.request.user.is_superuser:
            return  Venue.objects.all()
        else:
            return  Venue.objects.filter(organisation = self.request.user.userprofile)

    def get_success_url(self) -> str:
        return reverse("venues:venue-list")

##############################
# For personal Organizers #
##############################

class MyVenueListView(OrganizerRequiredMixin, ListView):
    template_name = "venue_list.html"
    context_object_name = "venues"

    def get_queryset(self):
        # Filters out the queryset of agent-list specific to the same Organization..
        if self.request.user.is_superuser:
            return  Venue.objects.all()
        else:
            return  Venue.objects.filter(organisation = self.request.user.userprofile)







       

      

      

        
    
    


