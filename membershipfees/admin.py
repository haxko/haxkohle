from django.contrib import admin
from django.shortcuts import render, redirect
from .models import Subscription, BankAccount, BankTransaction

from django.contrib.admin.views.decorators import user_passes_test

admin.site.site_header = "Haxkohle Admin"
admin.site.site_title = "Haxkohle"
admin.site.index_title = "Haxkohle"


class BankAccountAdmin(admin.ModelAdmin):
    list_display=('iban', 'bic', 'member', 'owner')
admin.site.register(BankAccount, BankAccountAdmin)


class BankTransactionAdmin(admin.ModelAdmin):
    list_display=('id', 'amount', 'currency', 'member', 'booking_date')
admin.site.register(BankTransaction, BankTransactionAdmin)

@user_passes_test(lambda user: user.is_active and user.is_superuser, '/admin/')
def import_camt(request):
    return render(request, 'admin/import_camt.html', {})

@user_passes_test(lambda user: user.is_active and user.is_superuser, '/admin/')
def match_transactions(request):
    return render(request, 'admin/match_transactions.html', {})
