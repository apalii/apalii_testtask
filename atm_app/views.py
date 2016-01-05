# -*- coding: utf-8 -*-

import requests, json, time
from django.utils import timezone
from apalii_testtask import settings
from atm_app.models import Card, Operations
from django.core.context_processors import csrf
from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required


def kurs_privat():
    '''Безналичный курс Приватбанка
    (конвертация по картам, Приват24, пополнение вкладов)
    '''
    url = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=11'
    kurs = requests.get(url).json()[0]
    return 'buy {} | sale {}'.format(kurs['buy'], kurs['sale'])

def main_page(request):
    now = timezone.now()
    return render_to_response('main.html',
                              {'kurs': kurs_privat(),})


def check(request):
    if request.method == 'GET':
        number = request.GET['number'].replace("-", "")
        to_response = {}
        to_response['number_requested'] = number
        try:
            card = Card.objects.filter(number=number)[0]
            to_response['is_active'] = True if card.is_active else False
        except IndexError:
            card = None
        to_response['valid'] = True if card else False
        response = json.dumps(to_response)
        return HttpResponse(response, content_type='application/json')
    else:
        raise Http404("GET only")


def card_login(request):
    args = {}
    args.update(csrf(request))
    return render_to_response('login.html', args)

def card_auth(request):
    number = request.POST['number']
    password = request.POST['password']
    print number, password
    user = auth.authenticate(number=number, password=password)
    print (number, password, user.is_authenticated())
    if user is not None:
        auth.login(request, user)
        # return HttpResponseRedirect('/loggedin/')
        response = json.dumps({"success": True})
        return HttpResponse(response, content_type='application/json')
    else:
        #return HttpResponseRedirect('/invalid/')
        response = json.dumps({"success": False})
        print response
        return HttpResponse(response, content_type='application/json')

    
@login_required
def card_loggedin(request):
    card = Card.objects.filter(id=request.user.id)[0]
    args = {}
    print request.user.is_authenticated(), request.user.id, card.balance
    return render(request, 'operations.html', args)

@login_required
def balance(request):
    args = {}
    args['today'] = timezone.now()
    print request.user.is_authenticated(), request.user.id    
    return render(request, 'balance.html', args)

@login_required
def take_cash(request):
    if request.method == 'GET':
        args = {}
        args.update(csrf(request))
        args['today'] = timezone.now()
        return render(request, 'take_cash.html', args)
    if request.method == 'POST':
        amount = int(request.POST['amount'])
        card = Card.objects.filter(id=request.user.id)
        #op = Operations.objects.filter(id=request.user.id)[0]
        if amount > card[0].balance:
            path = request.META.get('PATH_INFO')
            args = {'message': 'Not enough money !',
                    'path': path
                    }
            return render_to_response('error.html', args)
        prev_balance = card[0].balance
        cur_balance = card[0].balance - amount
        card.update(balance=cur_balance)
        new_op_id = str(card[0].id) + time.time().__str__().replace('.', "")
        new_op = Operations.objects.create(prev_balance=prev_balance,
                                           cur_balance=cur_balance,
                                           diff=amount,
                                           operation_code=new_op_id,
                                           operation_card=card[0]
                                          )
        return render(request, 'result.html', {'op': new_op})

        
def card_invalid(request):
    return render_to_response('invalid.html')


def card_logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")

"""
@login_required
def operations(request):
    #card = Card.objects.filter(id=request.user.id)[0]
    args = {}
    #args.update(csrf(request))
    #args['balance'] = card.balance
    #args['balance'] = card.number
    print request.user.number, request.user.id, card.balance
    return render_to_response('operations.html', args)
    """


