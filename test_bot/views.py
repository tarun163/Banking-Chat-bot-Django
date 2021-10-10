
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
import requests

class ChatterBotAppView(TemplateView):
    template_name = 'app.html'


class ChatterBotApiView(View):
    
    chatterbot = ChatBot(
    'Example Bot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry, but I do not understand.How can I help you? --> 1)register informations your-self  2)Check balance  3)found transefer  4)Loan',
            'maximum_similarity_threshold': 0.70
        }
      ]
    )    
    trainer = ListTrainer(chatterbot)
    trainer.train([
        'hello',
        'How can I help you? --> 1)register informations your-self  2)Check balance  3)fund transefer  4)Loan',
        '1',
        'Type of Information want to update/register --> 5)edit username  6)register account number  7) register phone number  18)add/update email',
        '5',
        'enter new username',
        '19',
        'username updated successfully!',
        '6',
        'enter account number',
        '7',
        'enter mobile number',
        '18',
        'enter email address',
        '20',
        'Email added successfully!',
        '2',
        'your current account balance is ',
        '3',
        'want to transfer fund --> 8)yes  9)no',
        '8',
        'enter account number',
        '10',
        'enter fund to transfer',
        '11',
        'transetion successfully completed',
        '12',
        'Opps sorry some bank related problems',
        '4',
        'type of loan you need --> 14)Education  15)Forming  16)Startup  17)Home',
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
        print("input", input_data['text'], "responce", response, request.session['num'])
        if(request.session['num'] == '5'):
            print(input_data['text'])
            user = request.user
            ins = User.objects.get(username=user)
            ins.username = input_data['text']
            ins.save()
            input_data['text'] = '19'
            response = self.chatterbot.get_response(input_data)
        if(request.session['num'] == '18'):
            print(input_data['text'])
            user = request.user 
            ins = User.objects.get(username=user)
            ins.email = input_data['text']
            ins.save()
            input_data['text'] = '20'
            response = self.chatterbot.get_response(input_data)    
        print("input", input_data['text'], "responce", response, request.session['num'])
        response_data = response.serialize()
        #print(response_data)
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

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username=username, password=password)
        if user is not None:
            request.session['num'] = '0'
            return redirect('main')
    return render(request, 'login.html')        

