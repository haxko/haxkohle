from django.db import models
from django.contrib.auth.models import User
from xmltodict import parse as parsexml
from functools import reduce
from users.models import Subscription
from django.conf import settings
import hashlib
import re

# BANKING
class BankAccount(models.Model):
    """
    A BankAccount is identified by its iban and bic.
    It has one owner and can be linked to a user, which can have multiple bank accounts.
    """
    owner = models.CharField(max_length=255)
    id_val = models.CharField(max_length=32)
    member = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Bank Account: {self.owner}"

class BankTransaction(models.Model):
    """
    BankTransaction represents a single transaction.
    """
    amount = models.DecimalField(max_digits=11, decimal_places=2)
    start_balance = models.DecimalField(max_digits=11, decimal_places=2)
    end_balance = models.DecimalField(max_digits=11, decimal_places=2)
    currency = models.CharField(max_length=3, default=settings.DEFAULT_CURRENCY)
    booking_date = models.DateTimeField()
    details = models.TextField()
    contact_account = models.ForeignKey(BankAccount, blank=True, null=True, on_delete=models.SET_NULL)
    member = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    visible = models.BooleanField(default=True)

    def __str__(self):
        return f"BankTransaction: {self.id}"


class CamtDocument:
    """
    The CamtDocument is just a factory to import camt-files.
    It validates data and creates BankAccount and BankTransaction objects.
    The CamtDocument is not saved to the database.
    """

    def __init__(self, camt_document, salt, *args, **kwargs):
        self.salt = salt
        data = parsexml(camt_document)['Document']['BkToCstmrAcctRpt']['Rpt']
        self.balance = self.__parse_balance(data['Bal'])
        self.transactions = self.__process_transactions(data['Ntry'])
        self.amount = 0
        for transaction in self.transactions:
            self.amount += transaction.amount


    def has_importable_data(self):
        return len(self.transactions) != 0

    def matches_current_balance(self):
        return BankTransaction.objects.order_by('id')[0].balance['end'] == self.balance['start'] \
            or BankTransaction.objects.count() == 0

    def camt_import(self):
        assert self.matches_current_balance(), "The camt document can not be imported, its balance does not match the database"

        for transaction in self.transactions_new:
            transaction.save()

        return len(self.transactions_new)

    def __get__(self, key):
        if key == "transactions":
            return self.transactions_old + self.transactions_new
        raise KeyError(f"The parameter {key} does not exist.")

    def __parse_balance(self, balances):
        """
        Returns the start balance and the end balance of the document.
        """
        for balance in balances:
            status = balance['Tp']['CdOrPrtry']['Cd']
            if status in ['PRCD', 'OPBD']:
                start_balance = balance['Amt']['#text']
                start_currency = balance['Amt']['@Ccy']
            elif status in ['CLBD', 'CLAV']:
                end_balance = balance['Amt']['#text']
                end_currency = balance['Amt']['@Ccy']

        assert start_currency == end_currency, "The balance currencies do not match each other"

        return {'start': start_balance, 'end': end_balance, 'currency': end_currency }

    def __process_transactions(self, entries):
        """
        Returns lists for old and new of transaction objects.
        """

        def get_or_create_transaction_from_entry(ntry, salt):

            id_hash_val = ntry['NtryDtls']['TxDtls']['RltdPties']['CdtrAcct']['Id']['IBAN'] \
                    + ntry['NtryDtls']['TxDtls']['RltdAgts']['CdtrAgt']['FinInstnId']['BIC'] \
                    + salt
            bank_account, _ = BankAccount.objects.get_or_create(
                id_val = hashlib.sha224( id_hash_val.encode('utf-8') ).hexdigest(),
                defaults = {'owner': ntry['NtryDtls']['TxDtls']['RltdPties']['Cdtr']['Nm']}
            )

            sign = '-' if ntry['CdtDbtInd'] == 'DBIT' else ''

            #assert False, ntry['BookgDt']
            fixed_transaction_details = {
                'amount': float(sign + ntry['Amt']['#text'].strip()),
                'currency':  ntry['Amt']['@Ccy'].strip(),
                'booking_date': ntry['BookgDt']['Dt'].strip(),
                'details': re.sub(r"\s+", " ", ntry['NtryDtls']['TxDtls']['RmtInf']['Ustrd'].strip().replace("\n", " ")),
                'contact_account': bank_account,
            }

            modifiable_transaction_details = {}

            return BankTransaction(**fixed_transaction_details, **modifiable_transaction_details)

        transactions = []
        if 'NtryDtls' not in entries:
            for entry in entries:
                transactions.append(get_or_create_transaction_from_entry(entry, self.salt))
            return transactions
        else:
            return [get_or_create_transaction_from_entry(entries, self.salt)]

