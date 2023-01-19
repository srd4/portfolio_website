from django.contrib import admin

# Register your models here.


from .models import Skill, Lesson, Tag, TimePeriod

admin.site.register(Skill)
admin.site.register(Lesson)
admin.site.register(Tag)
admin.site.register(TimePeriod)

