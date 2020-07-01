from django.contrib import admin
from django.shortcuts import render, redirect
from .models import Subscription, BankAccount, BankTransaction
from django.contrib.auth import forms as auth_forms, logout as auth_logout, login as auth_login, authenticate
from django.views import generic as generic_views, View
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import user_passes_test
from .forms import FileUploadForm
from io import BytesIO
from zipfile import ZipFile
from .models import CamtDocument
import hashlib

admin.site.site_header = "Haxkohle Admin"
admin.site.site_title = "Haxkohle"
admin.site.index_title = "Haxkohle"

class BankAccountAdmin(admin.ModelAdmin):
    list_display=('owner', 'member')
    exclude=('id_val',)
admin.site.register(BankAccount, BankAccountAdmin)

class BankTransactionAdmin(admin.ModelAdmin):
    list_display=('id', 'amount', 'currency', 'member', 'booking_date')
admin.site.register(BankTransaction, BankTransactionAdmin)

def stream_gzip_decompress(stream):
    dec = zlib.decompressobj(32 + zlib.MAX_WBITS)  # offset 32 to skip the header
    for chunk in stream:
        rv = dec.decompress(chunk)
        if rv:
            yield rv

@method_decorator(user_passes_test(lambda user: user.is_active and user.is_superuser, '/admin/'), name='dispatch')
class ImportCamt(generic_views.FormView):
    template_name = 'admin/import_camt.html'
    form_class = FileUploadForm
    redirect_to = '/'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class})


    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            with ZipFile(request.FILES['file_field'].file, 'r') as zip_file:
                for file_name in zip_file.namelist():
                    camt_file = CamtDocument(zip_file.open(file_name).read().decode(), salt=request.POST.get("salt"))
                    break
            return render(request, self.template_name, {'form': form })
        return render(request, self.template_name, {'form': form })


@method_decorator(user_passes_test(lambda user: user.is_active and user.is_superuser, '/admin/'), name='dispatch')
class MatchTransactions(generic_views.FormView):
    template_name = 'admin/match_transactions.html'
    form_class = auth_forms.AuthenticationForm
    redirect_to = '/'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'form': self.form_class})


    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        return render(request, self.template_name, {'form': form})

