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

def index(request):
    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # template = loader.get_template('polls/index.html')
    # context = {
    #     'latest_question_list': latest_question_list,
    # }
    if(request.user.is_authenticated):
        return render(request, '/polls/dashView.html')
    return redirect('/polls/dashLogin')
    # output = ', '.join([q.question_text for q in latest_question_list])
    # return HttpResponse(output)


def fileUpload(request):
    return render(request, 'polls/fileUpload.html')

#dashView test
def dashView(request):
    return render(request, 'polls/dashview.html')

def tableView(request):
    return render(request, 'polls/tableview.html')

def dashLogin(request):
    return render(request, 'polls/dashLogin.html')

def register(request):
    return render(request, 'polls/register.html')

def dashRegister(request):
    return render(request, 'polls/dashRegister.html')

def register_post(request):
    email = request.POST['email']
    password = request.POST['password']

    user = User.objects.create_user(email, email, password)

    context = {
        'user' : user
    }

    return render(request, 'polls/register_success.html', context)

def login(request):
    return render(request, 'polls/login.html');

def login_post(request):
    email = request.POST['email']
    password = request.POST['password']

    user = authenticate(request, username=email, password=password)
    if user is not None:
        auth_login(request, user)
        #redirect to success page
        return render(request, 'polls/dashview.html', {'user' : user})
    else:
        #redirect with error msg.
        return render(request, 'polls/login.html')

def logout(request):
    auth_logout(request)
    return render(request, 'polls/index.html')

def detail(request, question_id):
    # response = "You're looking at question %s." % question_id
    try:
        question = Question.objects.get(pk=question_id)
        context = {
            'question' : question
        }
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', context)
    # return HttpResponse(response)

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {
        'question': question
    })

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        #redisplay voting
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice...",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
        
    # response = "You're voting on question %s." % question_id
    # return HttpResponse(response)
