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
from .views import MemberListView, MemberDetailView, MemberUpdateView, MemberDeleteView, MemberListAPI, MemberListAPIDetail
from django.shortcuts import redirect, render, reverse
from django.http import HttpResponse
from django.conf.urls.static import static

app_name = "users"

urlpatterns = [
    path('', MemberListView.as_view(), name='user-list'),
    
    path('<int:pk>/', MemberDetailView.as_view(), name = 'user-detail'),
    path('<int:pk>/update/', MemberUpdateView.as_view(), name = 'user-update'),
    path('<int:pk>/delete/', MemberDeleteView.as_view(), name='user-delete'),
    
    # Django-REST Framework
    path('api/', MemberListAPI.as_view()),
    path('api/<int:pk>/', MemberListAPIDetail.as_view())

]
