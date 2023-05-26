from django.db import models
from django.contrib.auth.models import User
import json


# Create your models here.


class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    data = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
    def get_data(self):
        return json.loads(self.data)
    
    