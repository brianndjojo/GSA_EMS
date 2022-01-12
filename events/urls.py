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
from .views import EventListView, EventCreateView, EventDetailView, EventDeleteView, EventUpdateView, EventSignupView, MyEventListView, EventRegisteredView,  EventAdminLandingPageView, CheckinCheckoutInputView, EventAdminUserView, CheckinCheckoutUpdateView, event_unregister, switch_teams, set_payment
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
    path('<int:pk>/registeredDetail', EventDetailView.as_view(), name = 'event-registered-detail'),
    path('<int:pk>/unregister/', event_unregister, name='event-unregister'),

    path('create/', EventCreateView.as_view(), name='event-create'),

    path('eventadmin/', EventListView.as_view(), name='event-admin-list'),
    path('eventadmin/<int:pk>/', EventAdminLandingPageView.as_view(), name='event-admin-landing'),
    path('eventadmin/<int:pk>/checkincheckout/', CheckinCheckoutInputView.as_view(), name='checkin-checkout-input'),
    path('eventmanage/<int:pk>/', EventAdminUserView.as_view(), name='event-manage-user'),
    path('eventmanage/<int:pk>/update', CheckinCheckoutUpdateView.as_view(), name='checkin-checkout-update'),
    path('eventmanage/<int:pk>/switch', switch_teams, name='switch-teams'),
    path('eventmanage/<int:pk>/pay', set_payment, name='set-payment'),

    path('myevents/', MyEventListView.as_view(), name = 'myevent-list'),
    path('myevents/<int:pk>/', EventDetailView.as_view(), name = 'myevent-detail'),
    path('myevents/<int:pk>/update/', EventUpdateView.as_view(), name = 'myevent-update'),
    path('myevents/<int:pk>/delete/', EventDeleteView.as_view(), name='myevent-delete'),
    
]
