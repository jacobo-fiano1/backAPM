"""backAPM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin;
from django.urls import path, include;
from .views import *;
from django.urls import path, include
from rest_framework.authtoken import views

urlpatterns = [
    path('user/register', Users.as_view(), name='Protecora log in'),
    path('authenticate', views.obtain_auth_token, name='Protecora log in'),
    path('protectora/info', UsersInfo.as_view(), name='Create Protectora'),
    path('animal/search', AnimalSearch.as_view(), name='Get Animal'),
    path('animal/fav', AnimalFavs.as_view(), name='Favs Animal'),
    path('animal/state', AnimalState.as_view(), name='Favs Animal'),
    path('animal/tweet', TwitterAPI.as_view(), name='Publish tweet'),
    path('animal/<str:id>', Animal.as_view(), name='Get Animal'),
    path('animal', Animal.as_view(), name='Register Animal'),
    path('protectora/register', ProtectoraUsers.as_view(), name='Create Protectora'),
    path('protectora/search', ProtectoraSearch.as_view(), name='Search protectoras'),
    path('protectora/<str:id>', Protecora.as_view(), name='Get protectora'),
]
