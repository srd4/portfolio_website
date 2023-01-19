from django.urls import path
from .views import home, portfolio, about, contact, skill_set_div, practice_lesson_set_div, work_with_me_form

app_name = 'website'
urlpatterns = [
    path('', home, name='home'),
    path('portfolio/', portfolio, name='portfolio'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),

    path('skill_set/', skill_set_div, name='skill_set'),
    path('practice_lesson_set/', practice_lesson_set_div, name='practice_lesson_set'),

    path('work_with_me_form/', work_with_me_form, name='work_with_me_form'),
    
    
]
