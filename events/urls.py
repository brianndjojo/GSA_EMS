"""gsaEMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from .views import EventListView, EventCreateView, EventDetailView, EventDeleteView, EventUpdateView, EventSignupView, MyEventListView, EventRegisteredView, UserInputView
from django.shortcuts import redirect, render, reverse
from django.http import HttpResponse

app_name = "events"

urlpatterns = [
    path('', EventListView.as_view(), name='event-list'),
    path('<int:pk>/', EventDetailView.as_view(), name = 'event-detail'),
    path('<int:pk>/update/', EventUpdateView.as_view(), name = 'event-update'),
    path('<int:pk>/delete/', EventDeleteView.as_view(), name='event-delete'),
    path('<int:pk>/regsiter/', EventSignupView.as_view(), name='event-signup'),
    path('<int:pk>/regsitered/', EventRegisteredView.as_view(), name='event-registered'),
    path('create/', EventCreateView.as_view(), name='event-create'),

    path('checkincheckout/', EventListView.as_view(), name='checkin-checkout'),
     path('checkincheckout/<int:pk>/', UserInputView.as_view(), name='checkin-checkout-input'),

    path('myevents/', MyEventListView.as_view(), name = 'myevent-list'),
    path('myevents/<int:pk>/', EventDetailView.as_view(), name = 'myevent-detail'),
    path('myevents/<int:pk>/update/', EventUpdateView.as_view(), name = 'myevent-update'),
    path('myevents/<int:pk>/delete/', EventDeleteView.as_view(), name='myevent-delete'),
    
]
