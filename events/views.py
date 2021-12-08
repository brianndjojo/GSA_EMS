from django.shortcuts import render

# Create your views here.
from typing import List

from django.shortcuts import redirect, render, reverse
from django.core.mail import send_mail
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin


from users.rolemixin import OrganizerRequiredMixin, AdminRequiredMixin

from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView

from .forms import EventCreationForm, EventModelForm, EventSignupForm
from users.models import UserProfile, User, Event, Signup

# Create your views here.

# List View to display Agents.
class EventListView(LoginRequiredMixin, ListView):
    template_name = "event_list.html"
    context_object_name = "events"

    def get_queryset(self):
        # Filters out the queryset of agent-list specific to the same Organization..
        return  Event.objects.all()
       

class EventCreateView(LoginRequiredMixin, CreateView):
    # Specify template to be used
    template_name = "event_create.html"

    # Instead of Query, we specify the formclass to be used.
    form_class = EventCreationForm

    # Specify what happens when form is successfully submitted.
    def get_success_url(self) -> str:
        return reverse("events:event-list")
    
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
        obj = form.save(commit=False)
        obj.user = self.request.user.userprofile
        obj.organisation = obj.user
        obj.save()
    
        # Once email is sent return back to what the form was originally supposed to do.
        return super(EventCreateView, self).form_valid(form)

class EventDetailView(LoginRequiredMixin, DetailView):
    # Specify template to be used
    template_name = "event_detail.html"

    context_object_name = "event"
    # Speicfy Query Set
    def get_queryset(self):
        # Filters out the queryset of agent-list specific to the same Organization..
        
        return  Event.objects.all()
        

class EventUpdateView(OrganizerRequiredMixin, UpdateView):
    # Specify template to be used
    template_name = "event_update.html"

    # Speicfy Query Set
    def get_queryset(self):
        # Filters out the queryset of agent-list specific to the same Organization..
        if self.request.user.is_superuser:
            return  Event.objects.all()
        else:
            return  Event.objects.filter(organisation = self.request.user.userprofile)
    # Instead of Query, we specify the formclass to be used.
    form_class = EventModelForm

    # Specify what happens when form is successfully submitted.
    def get_success_url(self) -> str:
        return reverse("events:event-list")

class EventDeleteView(OrganizerRequiredMixin, DeleteView):
    template_name = "event_delete.html"
    def get_queryset(self):
        # Filters out the queryset of agent-list specific to the same Organization..
        if self.request.user.is_superuser:
            return  Event.objects.all()
        else:
            return  Event.objects.filter(organisation = self.request.user.userprofile)

    def get_success_url(self) -> str:
        return reverse("events:event-list")


##############################
# For personal Organizers #
##############################
class MyEventListView(OrganizerRequiredMixin, ListView):
    template_name = "event_list.html"
    context_object_name = "events"

    def get_queryset(self):
        # Filters out the queryset of agent-list specific to the same Organization..
        if self.request.user.is_superuser:
            return  Event.objects.all()
        else:
            return  Event.objects.filter(organisation = self.request.user.userprofile)

##############################
# For Signup for Events #
##############################

class EventSignupView(LoginRequiredMixin, CreateView):
    # Specify template to be used
    template_name = "event_signup.html"

    # Instead of Query, we specify the formclass to be used.
    form_class = EventSignupForm

    # Specify what happens when form is successfully submitted.
    def get_success_url(self) -> str:
        return reverse("events:event-list")
    
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
        obj = form.save(commit=False)
        obj.user = self.request.user.userprofile
        obj.event = Event.objects.get(pk=self.kwargs.get('pk'))
        obj.is_registered = True
        
        obj.save()
    
        # Once email is sent return back to what the form was originally supposed to do.
        return super(EventSignupView, self).form_valid(form)

class EventRegisteredView(LoginRequiredMixin, ListView):
    template_name = "events_registered.html"
    context_object_name = "regevent"

    def get_queryset(self):
        # Filters out the queryset of agent-list specific to the same Organization..
        
        return Signup.objects.filter(user = self.request.user.userprofile)

##############################
# For Checkin/Checkout System #
##############################
class CheckinCheckoutView(AdminRequiredMixin, ListView):
    template_name = "checkin_checkout.html"
    context_object_name = "events"

    def get_queryset(self):
        # Filters out the queryset of agent-list specific to the same Organization..
        
        return Event.objects.all()

    

