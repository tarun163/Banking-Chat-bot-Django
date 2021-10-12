from django.shortcuts import render, redirect
import json
from django.views.generic.base import TemplateView
from django.views.generic import View
from django.http import JsonResponse
from chatterbot import ChatBot
from chatterbot.ext.django_chatterbot import settings
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from .models import User, UserAccount, Convers
from django.contrib.auth import authenticate, login as loginUser

class ChatterBotAppView(TemplateView):
    template_name = 'app.html'


class ChatterBotApiView(View):
    
    chatterbot = ChatBot(
    'Example Bot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry, but I do not understand.How can I help you?(enter number of curresponding options) --> 1)register informations your-self  2)Check balance  3)found transefer  4)Loan',
            'maximum_similarity_threshold': 0.90
        }
      ]
    )    
    trainer = ListTrainer(chatterbot)
    #train by python list trainer
    trainer.train([
        'hello',
        'hii.. How can I help you?(enter number of curresponding options) --> 1)register informations your-self  2)Check balance  3)fund transefer  4)Loan',
        'hey',
        'hii.. How can I help you?(enter number of curresponding options) --> 1)register informations your-self  2)Check balance  3)fund transefer  4)Loan',
        'hii',
        'hii.. How can I help you?(enter number of curresponding options) --> 1)register informations your-self  2)Check balance  3)fund transefer  4)Loan',
        '1',
        'Type of Information want to update/register --> 5)edit username  6)register account number  7) register phone number  18)add/update email',
        '5',
        'enter new username',       
        '6',
        'enter account number',
        '7',
        'enter mobile number',
        '18',
        'enter email address',
        '19',
        'username updated successfully!',
        '20',
        'Email/updated added successfully!',
        '21',
        'account number added succussfully!',
        '22',
        'phone number added/updated successfully!',
        '2',
        'your current account balance is ',
        '3',
        'want to transfer fund --> 8)yes  9)no',
        '8',
        'enter account number want to transfer money',
        '9',
        'Thankyou,..',
        '10',
        'enter fund to transfer',
        '11',
        'transaction successfully completed your current balance is ',
        '12',
        'Opps sorry some bank related problems',
        '4',
        'type of loan you need --> 14)Education  15)Farming  16)Startup  17)Home',
        '14',
        'for more information please visit https://homeloans.sbi/',
        '15',
        'for more information please visit https://homeloans.sbi/',
        '16',
        'for more information please visit https://homeloans.sbi/',
        '17',
        'for more information please visit https://homeloans.sbi/',     
    ])

    
    def post(self, request, *args, **kwargs):
        input_data = json.loads(request.body.decode('utf-8'))
        if 'text' not in input_data:
            return JsonResponse({
                'text': [
                    'The attribute "text" is required.'
                ]
            }, status=400)    
        response = self.chatterbot.get_response(input_data)

        # edit/add username
        if(request.session['num'] == '5'):
            user = request.user
            ins = User.objects.get(username=user)
            ins.username = input_data['text']
            ins.save()
            chack = UserAccount.objects.get(name=user)
            if(check is not None):
                check.name = input_data['text']
                check.save()
            input_data['text'] = '19'
            request.session['num'] = '0'
            response = self.chatterbot.get_response(input_data)

        # add/update email
        if(request.session['num'] == '18'):
            user = request.user 
            ins = User.objects.get(username=user)
            ins.email = input_data['text']
            ins.save()
            input_data['text'] = '20'
            request.session['num'] = '0'
            response = self.chatterbot.get_response(input_data) 

        # register account number    
        if(request.session['num'] == '6'):
            user = request.user
            ins = UserAccount(name=user, account_num=input_data['text'], balance=0, mobile='0')
            ins.save()
            input_data['text'] = '21'
            request.session['num'] = '0'
            response = self.chatterbot.get_response(input_data)

        # register/update phone number
        if(request.session['num'] == '7'):
            user = request.user 
            ins = UserAccount.objects.get(name=user)
            ins.mobile = input_data['text']
            ins.save()
            input_data['text'] = '22'
            request.session['num'] = '0'
            response = self.chatterbot.get_response(input_data) 

        #  check account balance
        if(input_data['text'] == '2'):
            user = request.user 
            ins = UserAccount.objects.get(name=user)
            response = self.chatterbot.get_response(input_data)  
            response_data = response.serialize()
            x = response_data['text']
            y = str(ins.balance)
            x = x + ' $'+y
            response_data['text'] = x
            request.session['num'] = '0'
            return JsonResponse(response_data, status=200)

        #fund transfer acc 
        if(request.session['num'] == '8'):
            user = request.user 
            request.session['acc'] = input_data['text']
            input_data['text'] = '10'
            response = self.chatterbot.get_response(input_data)

        #add fund to transfer    
        if(request.session['num'] == '10'):
            user = request.user 
            acc_to = request.session['acc']
            user_by = UserAccount.objects.get(name=user)
            user_to = UserAccount.objects.get(account_num=acc_to)
            if user_to is not None:
                if(user_by.balance >= int(input_data['text'])):
                    user_to.balance = int(user_to.balance) + int(input_data['text'])
                    user_to.save()
                    user_by.balance = int(user_by.balance) - int(input_data['text']) 
                    user_by.save()
                    input_data['text'] = '11'
                    response = self.chatterbot.get_response(input_data)
                    response_data = response.serialize()
                    x = response_data['text']
                    y = str(user_by.balance)
                    x = x + ' $'+y
                    response_data['text'] = x
                    request.session['num'] = '0'
                    return JsonResponse(response_data, status=200)
                else:    
                    input_data['text'] = '12'
            else:
                input_data['text'] = '12'        
            response = self.chatterbot.get_response(input_data)

        
        response_data = response.serialize()
        Convers(name=request.user, chat=input_data['text'], response=response).save()
        request.session['num'] = input_data['text']
        return JsonResponse(response_data, status=200)

    def get(self, request, *args, **kwargs):
        """
        Return data corresponding to the current conversation.
        """
        return JsonResponse({
            'name': self.chatterbot.name
        })

#for login user
def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            request.session['num'] = '0'
            loginUser(request, user)
            return redirect('main')
    return render(request, 'login.html')        
#for register new user
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password1 = request.POST.get('p1')
        password2 = request.POST.get('p2')
        email = request.POST.get('email')
        user = User.objects.create_user(username, email, password1)
        user.save()
        ins = UserAccount(name=username, account_num='', balance=0, mobile='')
        ins.save()
        return redirect('login')
    return render(request, 'register.html')
    
