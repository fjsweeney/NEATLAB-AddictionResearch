# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
# from django.template import loader
from django.urls import reverse
from .models import Question, Choice

from .python_ml import pipeline

def index(request):

    if not request.user.is_authenticated:
        return redirect('/polls')
    
    return render(request, 'polls/modelExecution/index.html')

def modelExecutionPOST(request):

    if not request.user.is_authenticated:
        return redirect('/polls')
    


    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # # template = loader.get_template('polls/index.html')
    # context = {
    #     'latest_question_list': latest_question_list,
    # }
    # return render(request, 'polls/index.html', context)
    # output = ', '.join([q.question_text for q in latest_question_list])
    # return HttpResponse(output)
