from django.contrib import admin
from atm_app.models import Card, Operations


class OpAdmin(admin.ModelAdmin):
    list_display = ('operation_type',
                   'timestamp',
                   'cur_balance')
    date_hierarchy = 'timestamp'

class CardAdmin(admin.ModelAdmin):
    list_display = ('number',
                    'is_active',
                   'balance')
    #date_hierarchy = 'timestamp'


admin.site.register(Card, CardAdmin)
admin.site.register(Operations, OpAdmin)