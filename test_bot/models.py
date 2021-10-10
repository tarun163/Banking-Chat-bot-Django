from django.db import models
from django.contrib.auth.models import User

class UserAccount(models.Model):
    name = models.CharField(max_length=50)
    account_num = models.CharField(max_length=50)
    balance = models.CharField(max_length=50)
    mobile = models.CharField(max_length=50)
    created_on = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Convers(models.Model):
    name = models.CharField( max_length=50)
    chat = models.TextField()
    response = models.TextField()
    chat_on = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.name
            
    