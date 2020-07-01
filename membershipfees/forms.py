from django import forms
import hashlib
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

def validate_camt_upload_pass(value):
    value_hash = hashlib.sha1(value.encode('utf-8')).hexdigest()
    if value_hash != settings.CAMT_UPLOAD_PASS:
        raise ValidationError(
            _('The upload password is incorrect.'),
        )

class FileUploadForm(forms.Form):
    file_field = forms.FileField(label="Upload Camt052-Archive")
    salt = forms.CharField(widget=forms.PasswordInput(), validators=[validate_camt_upload_pass])
