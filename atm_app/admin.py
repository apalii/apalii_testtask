from django.contrib import admin
from atm_app.models import Card, Operations

class TaskInline(admin.StackedInline):
    model = Operations

class TaskAdmin(admin.ModelAdmin):
    inlines = [TaskInline]

admin.site.register((Card, Operations))
