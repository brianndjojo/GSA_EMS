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
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetCompleteView, PasswordResetConfirmView, PasswordResetDoneView
from django.urls import path
from django.urls.conf import include
from users.views import LandingPageView, SignUpView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPageView.as_view(), name='landing-page'),
    path('users/', include('users.urls', namespace='users')),
    path('events/', include('events.urls', namespace='events')),
    path('venues/', include('venues.urls', namespace='venues')),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('signup/', SignUpView.as_view(), name="signup"),
    path('reset/', PasswordResetView.as_view(), name="resetpass"),
    path('reset/complete', PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('reset/done', PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    
    
]
