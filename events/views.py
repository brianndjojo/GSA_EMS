from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
from typing import List

from django.shortcuts import redirect, render, reverse
from django.core.mail import send_mail
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin


from users.rolemixin import OrganizerRequiredMixin, AdminRequiredMixin

from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, FormView

from .forms import EventCreationForm, EventModelForm, EventSignupForm, UserInputForm
from django.contrib.auth.models import User
from users.models import UserProfile, Event, Signup, User

# Create your views here.

# List View to display Agents.
class EventListView(ListView):
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


##############################
# For Checkin #
##############################

class UserInputView(LoginRequiredMixin, FormView):
    # Specify template to be used
    template_name = "checkin_checkout_input.html"
    # Specify form to be used
    form_class = UserInputForm

    context_object_name = "checkinStatus"
    # Speicfy Query Set


    def get_success_url(self) -> str:
        return reverse("events:event-list")
    

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.accepts('text/html'):
            return response
        else:
            return JsonResponse(form.errors, status=400)

    def form_valid(self, form):
        # Save Usr-Identification input from form.
        checkin_username = form.cleaned_data.get('username')
        print(checkin_username)

        specific_user = User.objects.all().filter(username = checkin_username)
        print('User_PK:', specific_user.get().id)

        current_event = self.kwargs.get('pk')
        print('Event_Pk:', current_event)
        #retrieved_profile = User.objects.all().filter(username = checkin_username)
        #print('retrieved profile:',retrieved_profile)
        # Search DB whether that user is already signed up into that event..
        signedup_status = Signup.objects.filter(user = specific_user.get().id).filter(event=current_event)
        print(signedup_status)
        print(signedup_status.values('is_checkedin').get()['is_checkedin'])
        print(signedup_status.exists())

        #Checks if user is registered..
        if(signedup_status.exists()):
            if(signedup_status.values('is_checkedin').get()['is_checkedin'] is False):
                signedup_status.update(is_checkedin = True)
       

            elif(signedup_status.values('is_checkedin').get()['is_checkedin'] is True):
                    signedup_status.update(is_checkedin = False)
       
            print(signedup_status.values('is_checkedin').get()['is_checkedin'])
   
        return super().form_valid(form)


   
    
        

