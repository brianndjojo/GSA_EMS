from ast import Pass
from typing import List
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect, JsonResponse

from django.shortcuts import redirect, render, reverse
from django.core.mail import send_mail
from django.views.generic import ListView, DetailView, CreateView, DeleteView, FormView

from django.contrib.auth.mixins import LoginRequiredMixin

from users.rolemixin import OrganizerRequiredMixin, AdminRequiredMixin

from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView
from django.contrib.auth.views import PasswordChangeView

import json
from users.forms import CustomCreationForm, UserModelForm
from .forms import PasswordChangingForm, UpdateAccountForm
from users.models import User, UserProfile, Event
from users.serializers import UserSerializer, UserModelSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response  import Response

import datetime

class AccountSettingsView(LoginRequiredMixin, TemplateView):
    template_name = "settings.html"

class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    # Specify template to be used
    template_name = "registration/password_update_form.html"

    # Instead of Query, we specify the formclass to be used.
    form_class = PasswordChangingForm

    # Specify what happens when form is successfully submitted.
    def get_success_url(self):
        return reverse("user-settings")

    def get_queryset(self):
        
        your_id = self.request.user.id
        specific_user = User.objects.filter(id = your_id)
        return specific_user

class UpdateAccountView(LoginRequiredMixin, UpdateView):
    # Specify template to be used
    template_name = "account_update.html"

    # Instead of Query, we specify the formclass to be used.
    form_class = UpdateAccountForm

    # Specify what happens when form is successfully submitted.
    def get_success_url(self):
        return reverse("user-settings")

    def get_queryset(self):
        
        your_id = self.request.user.id
        specific_user = User.objects.filter(id = your_id)
        return specific_user


class AccountDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "account_delete.html"
   
    def get_success_url(self):
        return reverse("user-settings")

    def get_queryset(self):

        your_id = self.request.user.id
        specific_user = User.objects.filter(id = your_id)
        return specific_user