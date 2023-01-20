from django.db import models

# Create your models here.


class Message(models.Model):
    email = models.EmailField(max_length=2**7)
    name = models.CharField(max_length=2**6)
    message = models.TextField(max_length=2**9)

    def __str__(self) -> str:
        return self.email