# -*- coding: utf-8 -*-
import ujson as json
import time
import requests
from django.db.models import F
from django.contrib import auth
from django.utils import timezone
from django.core.context_processors import csrf
from .models import Card, Operations
from .forms import LoginForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required

from django.views.decorators.http import (
    require_http_methods, require_safe, require_POST
)
from django.shortcuts import (
    render, render_to_response, redirect
)

requests.packages.urllib3.disable_warnings()


def kurs_privat():
    """Безналичный курс Приватбанка
    (конвертация по картам, Приват24, пополнение вкладов)
    """
    url = "https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=11"
    kurs = requests.get(url).json()[0]
    return 'buy {} | sale {}'.format(kurs['buy'], kurs['sale'])


def main_page(request):
    return render_to_response('main.html',
                              {'kurs': kurs_privat()}
                              )


@require_safe
def check(request):
    number = request.GET['number'].replace("-", "")
    to_response = {'number_requested': number}
    try:
        card = Card.objects.get(number=number)
        to_response['is_active'] = True if card.is_active else False
    except Card.DoesNotExist:
        card = None
    to_response['valid'] = True if card else False
    return JsonResponse(to_response)


def card_login(request):
    args = {}
    args.update(csrf(request))
    return render_to_response('login.html', args)


def card_logout(request):
    card_id = request.session.get('card_id')
    card = Card.objects.get(id=card_id)
    card.was_last_time = card.last_login
    card.save(update_fields=['was_last_time'])
    auth.logout(request)
    return HttpResponseRedirect("/")


@require_POST
def card_auth(request):
    number = request.POST['number']
    password = request.POST['password']
    user = auth.authenticate(number=number, password=password)
    card = Card.objects.get(number=number)
    if user is not None:
        auth.login(request, user)
        request.session['card_id'] = card.id
        card.attempts = 0
        card.save(update_fields=['attempts'])
        return JsonResponse({"success": True})
    elif card.attempts < 3:
        tries = card.attempts + 1
        card.attempts = F('attempts') + 1
        card.save()
        response = {
            'message': "Wrong PIN. Attempts left : {}".format(3 - tries),
            'tries': tries
             }
        return JsonResponse(response, status=401)
    elif card.attempts >= 3:
        card.is_active = False
        card.save()
        response = {
            'message': "Your card is blocked !",
            'tries': 0
        }
        return JsonResponse(response, status=401)


def blocked(request):
    args = {'message': 'Your card is blocked ! '
                       'Please contact support department 8-800-111-22-33',
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
    return render(request, 'operations.html')


@login_required
def balance(request):
    card = Card.objects.get(id=request.user.id)
    args = {'today': timezone.now(), 'last_login': card.was_last_time}
    new_op_id = str(card.id) + time.time().__str__().replace('.', "")
    new_op = Operations.objects.create(prev_balance=card.balance,
                                       cur_balance=card.balance,
                                       diff=0,
                                       operation_type="balance",
                                       operation_code=new_op_id,
                                       operation_card=card
                                       )
    return render(request, 'balance.html', args)


@require_http_methods(["GET", "POST"])
@login_required
def cash_withdrawal(request):
    if request.method == 'GET':
        args = {}
        args.update(csrf(request))
        args['today'] = timezone.now()
        return render(request, 'take_cash.html', args)
    if request.method == 'POST':
        amount = int(request.POST['amount'])
        card = Card.objects.get(id=request.user.id)
        if amount > card.balance:
            args = {'message': 'Not enough money !',
                    'path': '/operations/'
                    }
            return render_to_response('error.html', args)
        prev_balance = card.balance
        cur_balance = card.balance - amount
        card.balance = cur_balance
        card.save(update_fields=['balance'])
        new_op_id = str(card.id) + time.time().__str__().replace('.', "")
        new_op = Operations.objects.create(prev_balance=prev_balance,
                                           cur_balance=cur_balance,
                                           diff=amount,
                                           operation_type="withdrawal",
                                           operation_code=new_op_id,
                                           operation_card=card
                                           )
        request.session['op'] = new_op.id
        return redirect('/result/')


@login_required
def result(request):
    new_op = request.session.get('op')
    qwe = Operations.objects.get(id=new_op)
    return render(request, 'result.html', {'op': qwe})
