from django import forms
from .models import Message

class WorkWithMe(forms.ModelForm):
    class Meta:
        model = Message
        fields = "__all__"