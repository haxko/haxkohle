from django.db import models
from django.contrib.auth import User
from xmltodict import parse as parsexml
import abc


# ToDo: Replace ValueStore with a Transaction_History
class ValueStore(models.Model):
    key = models.CharField(max_length=128)
    value = models.TextField()

    def getValue(key):
        return self.objects.get(key=key).first()

    def setValue(key, value):
        self.objects.create(key=key, value=value)

class BankAccount(models.Model):
    owner = models.CharField(max_length=50)
    iban = models.CharField(max_length=32)
    bic = models.CharField(max_length=11)
    member = models.ForeignKey(User, blank=True, null=True)

class BankTransaction(models.Model):
    amount = models.DecimalField(max_digits=11, decimal_places=2)
    currency = models.CharField(max_length=3)
    status = models.CharField(max_length=4)
    value_date = models.DateTimeField()
    booking_date = models.DateTimeField()
    details = models.TextField()
    contact_account = models.ForeignKey(BankAccount)
    member = models.ForeignKey(User, blank=True, null=True)
    visible = models.BooleanField(default=True)

class BankDataDocument(models.Model):
    __metaclass__ = abc.ABCMeta

    upload_date = models.DateTimeField()
    reference_date = models.DateTimeField()
    document = models.FileField(lambda _, filename: f"bdd/{filename}")

    @abc.abstractmethod
    def get_transactions(self):
        """Returns a list of transactions"""
        return

    @abc.abstractmethod
    def is_valid(self):
        """
        Checks if the document is valid and checks wether the bank account
        has a valid state before and after the transactions are imported.
        """
        return

    def save(self, *args, **kwargs):
        """ Prevents the Document from beeing saved. But saves the children instead. """
        for transaction in self.get_transactions():
            if self.is_valid() and transaction.is_valid():

                ValueStore.set('last_account_balance', )
                transaction.save(*args, **kwargs)
            else:
                transaction.delete()

    class Meta:
        abstract = True

class CamtDocument(BankDataDocument):

    def parse_document(self):
        if self.data is None:
            with self.document.open('r') as camt:
                self.data = parsexml(camt.read())['Document']['BkToCstmrAcctRpt']['Rpt']
        return self.data

    def is_valid(self):
        transactions = self.get_transactions()
        transaction_amount = transactions().reduce(lambda t1, t2: t1.amount + t2.amount)
        for balance in self.parse_data()['Bal']:
            status = balance['Tp']['CdOrPrtry']['Cd']

            if status in ['‘PRCD’', 'OPBD']:
                start_balance = balance['Amt']['#text']
                start_currency = balance['Amt']['@Ccy']
            else if status in ['CLBD', 'CLAV']:
                end_balance = balance['Amt']['#text']
                end_currency = balance['Amt']['@Ccy']

        if ValueStore.objects.get('last_account_balance').first() == start_balance: return False
        if start_balance + transaction_amount == end_balance: return False

        return True

    def get_transactions(self):
        # Seperated in subfunction - may be useful for later cacheing.
        def get_or_create_transaction_from_ntry(ntry):
            bank_account, _ = BankAccount.objects.get_or_create(
                iban = ntry['CdtrAcct']['Id']['IBAN'],
                bic  = ntry['NtryDtls']['TxDtls']['RltdAgts']['CdtrAgt']['FinInstnId']['BIC'],
                defaults = {'owner': ntry['Cdtr']['Nm']}
            )

            sign = '-' if ntry['CdtDbtInd'] == 'DBIT' else ''
            transaction, _ = BankTransaction.objects.get_or_create(
                amount = float(sign + ntry['Amt']['#text'].strip()),
                currency =  ntry['Amt']['@Ccy'].strip(),
                booking_date = ntry['BookDt']['Dt'].strip(),
                details = re.sub(r"\s+", " ", ntry['NtryDtls']['TxDtls']['RmtInf']['Ustrd'].strip().replace("\n", " ")),
                contact_account = account,
                defaults = {
                    'status': ntry['Sts'].lower(),
                    'value_date': ntry['ValDt']['Dt'],
                    'contact_account': account,
                }
            )
            return transaction

        transactions = []
        for ntry in self.parse_document()['Ntry']:
            transactions.append(get_transaction_from_ntry(ntry, self))
        return transactions
