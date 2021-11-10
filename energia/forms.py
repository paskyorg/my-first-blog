from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()

class EdistribucionForm(forms.Form):
    user = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    CHOICES = [('1', 'Último día'),('2', 'Última semana'),('3', 'Último mes')]
    consulta = forms.ChoiceField(choices=CHOICES)