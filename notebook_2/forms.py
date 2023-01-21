from django.forms import ModelForm, ValidationError
from django.db.models import Q
from .models import Container


class ContainerForm(ModelForm):
    class Meta:
        model = Container
        fields = ["name", "description", "parentContainer"]

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = Container.objects.filter(owner=user)

    def clean(self):
        cleaned_data = self.cleaned_data
        container_exists = self.queryset.filter(Q(name=cleaned_data['name']) | Q(description=cleaned_data['description'])).exists()

        if container_exists:
            raise ValidationError("A container with the same name has already been created.")
        
        return cleaned_data