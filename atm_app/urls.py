from django.conf.urls import url
from django.conf.urls import patterns, url, include

urlpatterns = [
    url(r'^$', 'atm_app.views.main_page'),
    url(r'^operations/$', 'atm_app.views.operations'),
    
    # Auth urls
    url(r'^check/$', 'atm_app.views.check'),
    url(r'^login/$', 'atm_app.views.card_login'),
    url(r'^auth/$', 'atm_app.views.card_auth'),
    url(r'^logout/$', 'atm_app.views.card_logout'),
    url(r'^loggedin/$', 'atm_app.views.card_loggedin'),
    url(r'^invalid/$', 'atm_app.views.card_invalid'),
    
    # Operations urls
    url(r'^balance/$', 'atm_app.views.balance'),
    url(r'^take_cash/$', 'atm_app.views.take_cash'),    
]