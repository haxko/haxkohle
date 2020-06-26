from django.contrib import admin
from .models import Member, Subscription, BankAccount, BankTransaction


admin.site.index_template = 'admin/index.html'

admin.site.site_header = "Haxkohle Admin"
admin.site.site_title = "Haxkohle"
admin.site.index_title = "Haxkohle"

admin.site.register(BankAccount)
admin.site.register(BankTransaction)

