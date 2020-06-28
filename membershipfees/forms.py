from django import forms

class FileUploadForm(forms.Form):
    file_field = forms.FileField(label="Upload Camt052-Archive")
