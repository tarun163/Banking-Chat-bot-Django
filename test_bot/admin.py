from django.contrib import admin
from .models import UserAccount, Convers

@admin.register(UserAccount)
class Useraccount(admin.ModelAdmin):
    list_display  = ('name', 'account_num', 'balance', 'mobile')

@admin.register(Convers)
class Conversation(admin.ModelAdmin):
    list_display  = ('name', 'chat', 'response', 'chat_on')
