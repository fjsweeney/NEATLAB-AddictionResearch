# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
import datetime
from django.utils import timezone

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

class UploadedFile(models.Model):
    uploadFile = models.FileField()
    uploadDate = models.DateTimeField(auto_now_add=True)
    ownerID = models.IntegerField()

class ClusterFileUpload(models.Model):
    locationFile = models.FileField()
    smokingReportFile = models.FileField()
    uploadDate = models.DateTimeField(auto_now_add=True)
    ownerID = models.IntegerField()