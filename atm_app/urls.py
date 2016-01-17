from django.conf.urls import url
from django.conf.urls import patterns, url, include

urlpatterns = [
    url(r'^$', 'atm_app.views.main_page'),

    # Auth urls
    url(r'^check/$', 'atm_app.views.check'),
    url(r'^login/$', 'atm_app.views.card_login'),
    url(r'^auth/$', 'atm_app.views.card_auth'),
    url(r'^logout/$', 'atm_app.views.card_logout'),
    url(r'^operations/$', 'atm_app.views.operations'),
    url(r'^invalid/$', 'atm_app.views.card_invalid'),

    # Operations urls
    url(r'^balance/$', 'atm_app.views.balance'),
    url(r'^cash_withdrawal/$', 'atm_app.views.cash_withdrawal'),
    url(r'^result/$', 'atm_app.views.result'),
    url(r'^blocked/$', 'atm_app.views.blocked')
]