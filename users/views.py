from typing import List

from django.shortcuts import redirect, render, reverse
from django.core.mail import send_mail
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin


from .rolemixin import OrganizerRequiredMixin, AdminRequiredMixin

from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView

from .forms import CustomCreationForm, UserModelForm
from .models import UserProfile, User

# Create your views here.

class LandingPageView(TemplateView):
    # Specify Template to be used.
    template_name = "landing.html"

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
        # Filters out the queryset of agent-list specific to the same Organization..
        return  UserProfile.objects.all()
      
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

    # Speicfy Query Set
    queryset = User.objects.all()
    # Instead of Query, we specify the formclass to be used.
    form_class = UserModelForm

    # Specify what happens when form is successfully submitted.
    def get_success_url(self) -> str:
        return reverse("users:user-list")

class MemberDeleteView(AdminRequiredMixin, DeleteView):
    template_name = "user_delete.html"
    queryset = User.objects.all()

    def get_success_url(self) -> str:
        return reverse("users:user-list")

        
    
    


