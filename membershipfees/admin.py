from django.contrib import admin
from .models import Subscription, BankAccount, BankTransaction

admin.site.site_header = "Haxkohle Admin"
admin.site.site_title = "Haxkohle"
admin.site.index_title = "Haxkohle"


class BankAccountAdmin(admin.ModelAdmin):
    list_display=('iban', 'bic', 'member', 'owner')
admin.site.register(BankAccount, BankAccountAdmin)


class BankTransactionAdmin(admin.ModelAdmin):
    list_display=('id', 'amount', 'currency', 'member', 'booking_date')
admin.site.register(BankTransaction, BankTransactionAdmin)

