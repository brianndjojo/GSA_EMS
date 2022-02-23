from typing import List
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect, JsonResponse

from django.shortcuts import redirect, render, reverse
from django.core.mail import send_mail
from django.views.generic import ListView, DetailView, CreateView, DeleteView, FormView

from django.contrib.auth.mixins import LoginRequiredMixin


from .rolemixin import OrganizerRequiredMixin, AdminRequiredMixin

from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView

import json
from .forms import CustomCreationForm, UserModelForm
from .models import User, UserProfile, Event
from .serializers import UserSerializer, UserModelSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response  import Response

import datetime


# Create your views here.

# Filter Users
#def search_user(request):
#    users = User.objects.all()
#    search_filter = request.GET.get('specific-user')
#    print(search_filter)
#    search_user = users.filter(username = search_filter)
#    if(search_user.exists()):
#        return UserProfile.objects.all().filter(user_id = search_user.get().id)
#    return UserProfile.objects.all()

class LandingPageView(LoginRequiredMixin, ListView):
    # Specify Template to be used.
    template_name = "landing.html"
    context_object_name = 'events'
    
    def get_queryset(self):
        events = Event.objects.all()
        current_date = datetime.datetime.now().date()
        return events.filter(event_date__gte=current_date)
    

    def get(self, *args, **kwargs):
        if(not self.request.user.is_authenticated):
            return redirect('login')
        return super().get(self.request, *args, **kwargs)

    

# Create a Singup view, because Django does not have a Sign Up View. However, it has a Login and Logout view.
class SignUpView(CreateView):
    template_name = "registration/signup.html"
    form_class = CustomCreationForm

    def get_success_url(self) -> str:
        return reverse("login")

# List View to display Agents.
class MemberListView(AdminRequiredMixin, ListView):
    template_name = "user_list.html"
    context_object_name = "users"

    def get_queryset(self):
        return UserProfile.objects.all()
    # pass the context data of users as JSON to the frontend
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        users = User.objects.all().values()
        
            
        # UserModelSerailizer filters out the JSON data to only show what is necessary rather than all the attributes within the record.
        serializer = UserModelSerializer(users, many = True)
      
        # Render the serialized data as a JSON object.
        data = JSONRenderer().render(serializer.data)
        print('serialized data',data)
        print(type(serializer))
        print(type(data))
        data2 = data.decode('utf-8')
        print(type(data2))
        print(data2)
        # Assign the Context as the JSON Object.
        context['users_list'] = data2
      
        return context
    

class MemberListAPI(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer

class MemberListAPIDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer

class MemberDetailView(AdminRequiredMixin, DetailView):
    # Specify template to be used
    template_name = "user_detail.html"

    context_object_name = "user"
    # Speicfy Query Set
    def get_queryset(self):
        # Filters out the queryset of agent-list specific to the same Organization..
        return  UserProfile.objects.all()

class MemberUpdateView(AdminRequiredMixin, UpdateView):
    # Specify template to be used
    template_name = "user_update.html"

    # Instead of Query, we specify the formclass to be used.
    form_class = UserModelForm

    # Specify what happens when form is successfully submitted.
    def get_success_url(self) -> str:
        return reverse("users:user-list")

    def get_queryset(self):
        print(self.kwargs.get('pk'))
        user_id = UserProfile.objects.filter(id = self.kwargs.get('pk')).get().user_id
        specific_user = User.objects.filter(id = user_id)
        return specific_user
    

class MemberDeleteView(AdminRequiredMixin, DeleteView):
    template_name = "user_delete.html"
   
    def get_success_url(self) -> str:
        return reverse("users:user-list")

    def get_queryset(self):
        print(self.kwargs.get('pk'))
        user_id = UserProfile.objects.filter(id = self.kwargs.get('pk')).get().user_id
        print(user_id)
        specific_user = User.objects.filter(id = user_id)
        print(specific_user)
        return specific_user
    
        

    


