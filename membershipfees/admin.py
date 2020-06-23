from django.contrib import admin
from .models import Member, Subscription, BankAccount, BankTransaction

admin.site.register(BankAccount)
admin.site.register(BankTransaction)

