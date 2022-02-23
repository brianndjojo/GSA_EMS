from pipes import Template
from django.shortcuts import (get_object_or_404,
                              render,
                              HttpResponseRedirect)

from itertools import chain
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

from .forms import EventInputForm, EventSignupForm, UserInputForm
#from django.contrib.auth.models import User
from users.models import User, UserProfile, Event, Signup, User

# To serialize for JSON objects
from django.core.serializers import serialize
from django.http import HttpResponse

#import datetime
import datetime

# Create your views here.

# Both GET and POST method is used to transfer data from client to server in HTTP protocol but Main difference between POST and GET method is that GET carries request parameter appended in URL string while POST carries request parameter in message body which makes it more secure way of transferring data from client to ...
# So essentially GET is used to retrieve remote data, and POST is used to insert/update remote data.

#Upcoming Events for landing.html
  


# Filter Events
def search_event(request):
    events = Event.objects.all()
    search_filter = request.GET.get('specific-event')
    print(search_filter)
    search_event = events.filter(event_title = search_filter)
    if(search_event.exists()):
        return events.filter(event_title = search_filter)
    return Event.objects.all()
    

# List View to display Events
class EventListView(LoginRequiredMixin, ListView):
    template_name = "event_list.html"
    context_object_name = "events"

    def get_queryset(self):
        # Filters out the queryset of agent-list specific to the same Organization..
        event = search_event(self.request)
        return  event


class EventCreateView(OrganizerRequiredMixin, CreateView):
    # Specify template to be used
    template_name = "event_create.html"

    # Instead of Query, we specify the formclass to be used.
    form_class = EventInputForm

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

class EventDetailView(DetailView):
    # Specify template to be used
    template_name = "event_detail.html"

    context_object_name = "event"
    # Speicfy Query Set
    def get_queryset(self):
        # Filters out the queryset of agent-list specific to the same Organization..
        
        return Event.objects.all()
        

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
    form_class = EventInputForm

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
        return reverse("events:event-registered", self.request.user.pk)
    
    # form_valid function called in POST function of ProcessFormView.
    # Send email when form is submitted to create new Lead.
    # Overriding form_valid function/adding new funcitonality, specifically sending email.
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.accepts('text/html'):
            return response
        else:
            return JsonResponse(form.errors, status=400)
    
    def form_valid(self, form):
        # Sends email with Django mail function
        send_mail(subject = "A new Event has been added",
            message = "A new Event has been added.", 
            from_email = "test@test.com",
            recipient_list=["test2@test.com"],
        )
        selectedEvent = Event.objects.get(id = self.kwargs.get('pk'))
        currentUser = UserProfile.objects.get(user = User.objects.get(id = self.request.user.pk))
        existStatus = Signup.objects.filter(event = selectedEvent).filter(user = currentUser)
        
        print('Event-exists:',existStatus.exists())
        if(not existStatus.exists() and selectedEvent.capacity > 0):
            # Signup
            obj = form.save(commit=False)
            obj.user = self.request.user.userprofile
            obj.event = Event.objects.get(pk=self.kwargs.get('pk'))
            obj.is_registered = True
            obj.save()

            # Checks if event-capacity is still available
            if(selectedEvent.current_capacity > 0): 
                selectedEvent.current_capacity = selectedEvent.current_capacity - 1
                print("Remaining Capacity:", selectedEvent.current_capacity)
                
                selectedEvent.save()

            #
        return redirect("events:event-registered", self.request.user.pk)
    
class EventRegisteredView(LoginRequiredMixin, ListView):
    template_name = "events_registered.html"
    context_object_name = "regevent"

    def get_queryset(self):
        # Filters out the queryset of agent-list specific to the same Organization..
        
        return Signup.objects.filter(user = self.request.user.userprofile)

# Unregister Events
def event_unregister(request, pk):
    # dictionary for initial data with
    # field names as keys
    context = {}

    context['error'] = 'You are already registered!'
 
    # fetch the specific event
    event = get_object_or_404(Event, id = pk)
    specific_user = get_object_or_404(UserProfile, user_id = request.user.pk)

    signup = Signup.objects.filter(event = event).filter(user = specific_user)
    checkin = signup.get().is_checkedin
    print(signup)
    print(checkin)
    if request.method =="POST":
        # delete object
        if(signup.exists):
            # Cannot unregister if user is already checked in..
            if(checkin == False):
                # Delete Signup, when user registers
                signup.delete()
                # Update Capacity when user unregisters...
                if(event.current_capacity < event.capacity):
                    event.current_capacity = event.current_capacity + 1
                    print("current capacity:",event.current_capacity)
                    event.save()
                return HttpResponseRedirect("/")
        # after deleting redirect to
        # home page
        print("Cannot Unregister since you are already checked in...")
        return redirect("events:event-unregister-2", event.pk)
    
    return render(request, "event_unregister.html", context)   

##############################
# For Managing Events #
##############################

## EVENT MANAGEMENT LANDING PAGE ##
#class EventAdminLandingPageView(AdminRequiredMixin ,DetailView):
    # Specify Template to be used.
#    template_name = "event-admin-landing.html"
#    context_object_name = 'event'
    
#    def get_queryset(self):
#        selectedEvent = Event.objects.filter(pk=self.kwargs.get('pk'))
#       return selectedEvent

## PLAYER-LIST FOR EVENT MANAGEMENT ##
class EventAdminPlayerListView(AdminRequiredMixin ,ListView):
    # Specify Template to be used.
    template_name = "player_list.html"
    context_object_name = 'players'
    
    def get_queryset(self):
        signup_pk = self.kwargs.get('pk')
        signedup_event = Signup.objects.filter(event_id = signup_pk)
        print('retrieved signups',signedup_event)
        return Signup.objects.filter(event_id = signup_pk)

class EventAdminLandingPageView(AdminRequiredMixin , DetailView):
    # Specify Template to be used.
    template_name = "event-admin-landing.html"
    context_object_name = 'event'

    def get_queryset(self):
        # Get Specific event
        specific_event = Event.objects.filter(pk=self.kwargs.get('pk'))
        print('specific event', specific_event)

        return specific_event

    def get_context_data(self, **kwargs):
        # Retrieve Context to Override.
        context = super().get_context_data(**kwargs)

        # Get signups of specific event
        signup_pk = self.kwargs.get('pk')
        signedup_event = Signup.objects.filter(event_id = signup_pk)
        print('retrieved signups',signedup_event)
        context['players'] = signedup_event

        return context

## CHECKIN-CHECKOUT SYSTEM ##
class CheckinCheckoutInputView(AdminRequiredMixin, FormView):
    # Specify template to be used
    template_name = "checkin_checkout_input.html"
    # Specify form to be used
    form_class = UserInputForm

    context_object_name = "checkin"
    # Specify Query Set


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

        current_event = self.kwargs.get('pk')
        print('Event_Pk:', current_event)

        specific_user = User.objects.all().filter(username = checkin_username)
        if(specific_user.exists()):
            print('User_PK:', specific_user.get().id)

        
            
            # Search DB whether that user is already signed up into that event..
            signedup_status = Signup.objects.filter(user = specific_user.get().id).filter(event=current_event)
            
            #Checks if user is registered..
            if(signedup_status.exists()):

                specific_signup_pk =  signedup_status.get().id # PK of selected user.
                return redirect('events:event-manage-user', specific_signup_pk)
            #If user is not registered...
            else:
                print('user is not registered..')
                return redirect('events:checkin-checkout-input', current_event)
        else:
            print('user does not exist..')
            return redirect('events:checkin-checkout-input', current_event)
                    
## MANAGEMENT-INTERFACE FOR SPECIFIC PLAYER ##    
class EventAdminUserView(AdminRequiredMixin, DetailView):
    # Specify template to be used
    template_name = "event-admin-user.html"
    context_object_name = "specificUser"
    


    def get_queryset(self):
        signup_pk = self.kwargs.get('pk')
        specific_signup = Signup.objects.filter(id = signup_pk)
        specific_user = User.objects.filter(id = specific_signup.get().user_id)
        print(specific_user.values())
        print(specific_signup.values())

        return specific_signup

## CHECKIN-CHECKOUT FOR SPECIFIC USER ##
class CheckinCheckoutUpdateView(AdminRequiredMixin, DetailView):
    template_name = "event-admin-user.html"
    context_object_name = "specificUser"


    # Specify Query Set
    def get_queryset(self):
        # Save Usr-Identification input from form.
        signup_pk = self.kwargs.get('pk')
        signedup_event = Signup.objects.filter(id = signup_pk)
        paid = signedup_event.get().is_paid

        
        if(signedup_event.exists()):
            print('Paid_Status', paid)
            print('Event_Pk:', signup_pk)
            #Checkin
           
            if(signedup_event.values('is_checkedin').get()['is_checkedin'] is False):
                signedup_event.update(is_checkedin = True)
                print('Checked in')
                                    
            #Checkout
            elif(signedup_event.values('is_checkedin').get()['is_checkedin'] is True):
                if(paid == True):
                    signedup_event.update(is_checkedin = False)
                    print('Checked out')
                            
                    print(signedup_event.values('is_checkedin').get()['is_checkedin'])
                
            return signedup_event    
        else:
            print('user is not registered..')
            return signedup_event
            
## SWITCH TEAMS FOR SPECIFIC USER ##
def switch_teams(request, pk):
    # dictionary for initial data with
    # field names as keys
    context = {}
 
    # fetch the specific event
    signup = get_object_or_404(Signup, id = pk)
    print("team:",signup.team)
    if request.method =="GET":
        print('test')
        if(signup.team == 1):
            signup.team = 0
            signup.save()
        elif(signup.team == 0):
            signup.team = 1
            signup.save()
     
    print("team after:", signup.team)
    return redirect("events:event-manage-user", pk)   

## TOGGLE PAYMENT FOR USER ##
def set_payment(request, pk):
    # dictionary for initial data with
    # field names as keys
    context = {}
 
    # fetch the specific event
    signup = get_object_or_404(Signup, id = pk)
    print("Payment-Status:",signup.is_paid)
    if request.method =="GET":
        print('test')
        if(signup.is_paid == False):
            signup.is_paid = True
            signup.save()
        elif(signup.is_paid == True):
            signup.is_paid = False
            signup.save()
     
    print("Payment-Status:", signup.is_paid)
    return redirect("events:event-manage-user", pk)   
    
        



    
