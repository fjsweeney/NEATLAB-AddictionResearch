# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponse, HttpResponseRedirect

# from django.template import loader
from django.urls import reverse
from .models import Question, Choice
from .python_ml import pipeline

#convert to ENV variable
DATASOURCE = "/home/weesp/DATA/"

def index(request):

    if not request.user.is_authenticated:
        return redirect('/polls')
    
    context = {
        'modelChoices': ["RF", "miSVM", "MISVM", "LRC", "GBC", "SVM"],
        'bagIntervalChoices': [5, 10, 15, 20, 30, 60],
        'percentageTestChoices': [.1, .15, .2, .25],
        'datasetChoices': ['participant_1', 'participant_2', 'participant_3', 'participant_4']
    }

    return render(request, 'polls/modelExecution/index.html', context)


def extractPathFromDatasetSelection(selection):
    return DATASOURCE + selection + '_container'

def modelExecutionPOST(request):

    if not request.user.is_authenticated:
        return redirect('/polls')

    dataPath = extractPathFromDatasetSelection(request.POST['dataset'])

    #TODO - sanitize request.POST data before throwing it into pipeline.
    pipeline.main([dataPath, request.POST['bagInterval'], request.POST['percentageTest'], request.POST['modelName'], '--sklearn', '1'])