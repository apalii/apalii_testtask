from django.conf.urls import url

urlpatterns = [
    url(r'^$', 'atm_app.views.main_page'),

    # Auth urls
    url(r'^check/$', 'atm_app.views.check', name='check'),
    url(r'^login/$', 'atm_app.views.card_login', name='login'),
    url(r'^auth/$', 'atm_app.views.card_auth', name='auth'),
    url(r'^logout/$', 'atm_app.views.card_logout', name='logout'),
    url(r'^operations/$', 'atm_app.views.operations', name='ops'),
    url(r'^invalid/$', 'atm_app.views.card_invalid', name='invalid'),

    # Operations urls
    url(r'^balance/$', 'atm_app.views.balance', name='balance'),
    url(r'^cash_withdrawal/$', 'atm_app.views.cash_withdrawal', name='withdrawal'),
    url(r'^result/$', 'atm_app.views.result', name='result'),
    url(r'^blocked/$', 'atm_app.views.blocked', name='blocked'),

]