from django.db import models
from django.contrib.auth.models import User
import json


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
TRUTH_OR_LIE_CHOICES = (
    ('Truth', 'Truth'),
    ('Lie', 'Lie'),
    ('Middle', 'Middle'),
    ('No Comment', 'No Comment')
)

class Question(models.Model):
    question = models.TextField()
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    is_fundamental = models.BooleanField(default=False)
    truth_or_lie = models.CharField(max_length=10, choices=TRUTH_OR_LIE_CHOICES, default='Middle')
    active = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question


class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=10)
    date = models.DateTimeField(auto_now_add=True)
    add_to_certificate = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username + ' - ' + self.question.question + ' - ' + str(self.answer)
    
    def general_public(self):
        all_answer = UserAnswer.objects.filter(question=self.question)
        total = len(all_answer)
        agree = len(all_answer.filter(answer='agree'))
        disagree = len(all_answer.filter(answer='disagree'))
        no_comment = len(all_answer.filter(answer='no_comment'))

        # return the greater of agree or disagree or no comment
        if agree > disagree and agree > no_comment:
            parcentage = (agree / total) * 100
            return 'Agree', parcentage
        elif disagree > agree and disagree > no_comment:
            parcentage = (disagree / total) * 100
            return 'Disagree', parcentage
        elif no_comment > agree and no_comment > disagree:
            parcentage = (no_comment / total) * 100
            return 'No comment', parcentage
        else:
            parcentage = (no_comment / total) * 100
            return 'No comment', parcentage

    

class Reason(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    reason = models.TextField()
    file = models.FileField(upload_to='media/reasons/', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ' - ' + self.question.question + ' - ' + self.reason
    

class ReasonAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.ForeignKey(Reason, on_delete=models.CASCADE)
    answer = models.CharField(max_length=10, choices=TRUTH_OR_LIE_CHOICES)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ' - ' + self.reason.reason + ' - ' + str(self.answer)