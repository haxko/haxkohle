from django.db import models
from django.contrib.auth.models import User
from xmltodict import parse as parsexml
from functools import reduce
from users.models import Member, Subscription


# BANKING
class BankAccount(models.Model):
    """
    A BankAccount is identified by its iban and bic.
    It has one owner and can be linked to a user, which can have multiple bank accounts.
    """
    owner = models.CharField(max_length=50)
    iban = models.CharField(max_length=32)
    bic = models.CharField(max_length=11)
    member = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

class BankTransaction(models.Model):
    """
    BankTransaction represents a single transaction.
    """
    amount = models.DecimalField(max_digits=11, decimal_places=2)
    start_balance = models.DecimalField(max_digits=11, decimal_places=2)
    end_balance = models.DecimalField(max_digits=11, decimal_places=2)
    currency = models.CharField(max_length=3)
    booking_date = models.DateTimeField()
    details = models.TextField()
    contact_account = models.ForeignKey(BankAccount, blank=True, null=True, on_delete=models.SET_NULL)
    member = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    visible = models.BooleanField(default=True)


class CamtDocument:
    """
    The CamtDocument is just a factory to import camt-files.
    It validates data and creates BankAccount and BankTransaction objects.
    The CamtDocument is not saved to the database.
    """

    def __init__(self, camt_document, *args, **kwargs):
        with open(camt_document, 'r') as camt:
            data = parsexml(camt.read())['Document']['BkToCstmrAcctRpt']['Rpt']
            self.balance = self.__parse_balance(data['Bal'])
            self.transactions_old, self.transactions_new = self.__process_transactions(data['Ntry'])
            self.amount = reduce(lambda t1, t2: t1.amount + t2.amount, self.transactions_new + self.transactions_old, 0)
            assert self.balance['start'] + self.amount == self.balance['end'], 'The closing balance does not match the start balance plus transaction amount'

    def has_importable_data(self):
        return len(self.transactions['new']) != 0

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

            if status in ['‘PRCD’', 'OPBD']:
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

        def get_or_create_transaction_from_entry(ntry, amount_offset):
            bank_account, _ = BankAccount.objects.get_or_create(
                iban = ntry['CdtrAcct']['Id']['IBAN'],
                bic  = ntry['NtryDtls']['TxDtls']['RltdAgts']['CdtrAgt']['FinInstnId']['BIC'],
                defaults = {'owner': ntry['Cdtr']['Nm']}
            )

            sign = '-' if ntry['CdtDbtInd'] == 'DBIT' else ''

            fixed_transaction_details = {
                'amount': float(sign + ntry['Amt']['#text'].strip()),
                'currency':  ntry['Amt']['@Ccy'].strip(),
                'booking_date': ntry['BookDt']['Dt'].strip(),
                'details': re.sub(r"\s+", " ", ntry['NtryDtls']['TxDtls']['RmtInf']['Ustrd'].strip().replace("\n", " ")),
                'contact_account': bank_account,
            }

            modifiable_transaction_details = {}

            try:
                return BankTransaction.get(**fixed_transaction_details), False
            except self.model.DoesNotExist:
                return BankTransaction(**fixed_transaction_details, **modifiable_transaction_details), True

        transactions = { 'new': [], 'old': [] }
        for entry in entries:
            transaction, created = get_transaction_from_ntry(entry)
            transactions['new' if created else 'old'].append(get_transaction_from_ntry(ntry, self))
        return transactions['old'], transactions['new']

