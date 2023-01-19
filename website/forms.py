from django import forms

class WorkWithMe(forms.Form):
    email = forms.EmailField(label='Your email adress', max_length=2**7)
    name = forms.CharField(label='Your name', max_length=2**6)
    message = forms.CharField(widget=forms.Textarea, label='Your message', max_length=2**9)