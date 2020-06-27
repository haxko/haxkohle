from django.contrib import admin
from django.contrib.auth.models import User
from .models import *



class SubscriptionAdmin(admin.ModelAdmin):
    list_display=('membership_number', 'user', 'begin_date', 'end_date', )
admin.site.register(Subscription, SubscriptionAdmin)
