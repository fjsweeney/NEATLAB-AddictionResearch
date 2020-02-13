# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
# from django.template import loader
from django.urls import reverse
from .models import Question, Choice, UploadedFile, models, ClusterFileUpload, RF_Upload

def fileUpload(request):
    return render(request, 'polls/fileUpload.html')

def fileUploadPOST(request):
    clusterFile = ClusterFileUpload.objects.create(locationFile=request.FILES['locationFile'], smokingReportFile=request.FILES['smokingReportFile'], ownerID=request.user.id)
    clusterFile.save()
    return redirect('/polls/user/fileUploadList')

def fileUploadList(request):
    
    context = {
        'clusterFiles' : ClusterFileUpload.objects.filter(ownerID=request.user.id),
        'rf_files' : RF_Upload.objects.filter(ownerID=request.user.id)
    }
    
    return render(request, 'polls/fileUploadList.html', context)

def random_forest(request):
        participantDirectory = RF_Upload.objects.create(participantFolder=request.FILES['participantFolder'], ownerID=request.user.id)
        participantDirectory.save()
        
        return redirect('/polls/user/fileUploadList')
        



# modelUploads.random_forest