from django.db import models
from django.contrib.auth.models import User

#user module for storing user account information
class UserAccount(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    account_num = models.CharField(max_length=50, blank=True, null=True)
    balance = models.IntegerField(blank=True, null=True)
    mobile = models.CharField(max_length=50, blank=True, null=True)
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
            
    