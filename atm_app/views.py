# -*- coding: utf-8 -*-

import requests, json, time
from django.utils import timezone
from apalii_testtask import settings
from atm_app.models import Card, Operations
from django.core.context_processors import csrf
from django.contrib import auth
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import (
    render, render_to_response, get_object_or_404, redirect
)

requests.packages.urllib3.disable_warnings()

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


def card_logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")


def card_auth(request):
    print request
    number = request.POST['number']
    password = request.POST['password']
    print number, password
    user = auth.authenticate(number=number, password=password)
    card = Card.objects.get(number=number)
    if user is not None:
        auth.login(request, user)
        card.attempts = 0
        card.save(update_fields=['attempts'])
        response = json.dumps({"success": True})
        return HttpResponse(response, content_type='application/json')
    elif card.attempts < 3:
        tries = card.attempts + 1
        card.attempts = F('attempts') + 1
        card.save()
        response = json.dumps(
            {'message': "Wrong PIN. Attempts left : {}".format(3 - tries),
            'tries': tries
           }
        )
        print response
        return HttpResponse(response,
                            content_type='application/json', status=401)
    elif card.attempts >= 3:
        card.is_active = False
        card.save()
        response = json.dumps(
            {'message': "Your card is blocked !",
            'tries': 0
           }
        )
        print card.attempts, response
        return HttpResponse(response,
                            content_type='application/json', status=401)


def blocked(request):
    args = {'message': 'Your card is blocked ! '
            'Please contact our support department 8-800-111-222-333',
            'path': "/"
           }
    return render_to_response('error.html', args)


def card_invalid(request):
    path = request.META.get('PATH_INFO')
    args = {'message': 'Invalid password ! Try again !',
            'path': path
           }
    return render_to_response('error.html', args)


@login_required
def operations(request):
    card = Card.objects.get(id=request.user.id)
    print card.last_login, "operations"
    return render(request, 'operations.html')


@login_required
def balance(request):
    card = Card.objects.get(id=request.user.id)
    args = {}
    args['today'] = timezone.now()
    new_op_id = str(card.id) + time.time().__str__().replace('.', "")
    new_op = Operations.objects.create(prev_balance=card.balance,
                                       cur_balance=card.balance,
                                       diff=0,
                                       operation_type = "balance",
                                       operation_code=new_op_id,
                                       operation_card=card
                                      )
    return render(request, 'balance.html', args)


@login_required
def cash_withdrawal(request):
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
            args = {'message': 'Not enough money !',
                    'path': '/operations/'
                    }
            return render_to_response('error.html', args)
        prev_balance = card[0].balance
        cur_balance = card[0].balance - amount
        card.update(balance=cur_balance)
        new_op_id = str(card[0].id) + time.time().__str__().replace('.', "")
        new_op = Operations.objects.create(prev_balance=prev_balance,
                                           cur_balance=cur_balance,
                                           diff=amount,
                                           operation_type = "withdrawal",
                                           operation_code=new_op_id,
                                           operation_card=card[0]
                                          )
        request.session['op'] = new_op.id
        print request.session['op']
        return redirect('/result/')


@login_required
def result(request):
    new_op = request.session.get('op')
    qwe = Operations.objects.get(id=new_op)
    return render(request, 'result.html', {'op': qwe})

