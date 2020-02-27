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

import argparse


def index(request):

    if not request.user.is_authenticated:
        return redirect('/polls')
    
    return render(request, 'polls/modelExecution/index.html')

def modelExecutionPOST(request):

    parser = argparse.ArgumentParser()

    parser.add_argument("base_dir", type=str,
                        help="Directory containing all participant data.")
    parser.add_argument("bag_interval", type=str,
                        help="Number of minutes for each bag.")
    parser.add_argument("pct_test", type=float,
                        help="Percent of data used for test set")
    parser.add_argument("--train", type=str,
                       help="File containing training data (a pkl)")
    parser.add_argument("model", type=str,
                        choices=["RF", "miSVM", "MISVM", "LRC", "GBC", 
                        "SVM"],
                        help="Model type")
    parser.add_argument("--hyperopt", type=int,
                        help="Number of hyperparameter iterations for "
                             "hyperopt tuning.")
    parser.add_argument("--sklearn", type=int,
                        help="Number of hyperparameter iterations for sklearn "
                             "tuning.")
    parser.add_argument("--take_mean", action='store_true', default=False,
                        help="Use the feature mean for each bag as one "
                             "instance (as opposed to stacking multiple "
                             "instances as the input to the model).")

    # args = parser.parse_args(args=["./python_ml/Data", "5", ".2", "SVM", "--sklearn", "1"])

    pipeline.main(['/home/weesp/Desktop/github_senior_proj/NEATLAB-AddictionResearch/dashboard/python_server/polls/python_ml/Data', '5', '.2', 'SVM', '--sklearn', '1'])

    # if not request.user.is_authenticated:
    #     return redirect('/polls')
    


    # latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # # template = loader.get_template('polls/index.html')
    # context = {
    #     'latest_question_list': latest_question_list,
    # }
    # return render(request, 'polls/index.html', context)
    # output = ', '.join([q.question_text for q in latest_question_list])
    # return HttpResponse(output)
