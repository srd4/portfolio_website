from django.contrib import admin
from .models import Container, Item, StatementVersion, ItemTag

# Register your models here.

admin.site.register(Container)
admin.site.register(Item)
admin.site.register(StatementVersion)
admin.site.register(ItemTag)