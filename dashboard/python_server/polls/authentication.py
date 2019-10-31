# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
# from django.template import loader
from django.urls import reverse
from .models import Question, Choice

def register(request):
    return render(request, 'polls/register.html')

def register_post(request):
    email = request.POST['email']
    password = request.POST['password']

    user = User.objects.create_user(email, email, password)

    #Then log user in.
    authenticate(request, username=email, password=password)

    context = {
        'user': user
    }
    
    return render(request, 'polls/register_success.html', context)

def login(request):
    return render(request, 'polls/login.html')

def login_post(request):
    email = request.POST['email']
    password = request.POST['password']

    user = authenticate(request, username=email, password=password)
    if user is not None:
        auth_login(request, user)
        #redirect to success page
        #return render(request, 'polls/index.html', {'user': user})
        return redirect('/polls')
    else:
        #redirect with error msg.
        return redirect('/polls/login')



def logout(request):
    auth_logout(request)
    return redirect('/polls')
