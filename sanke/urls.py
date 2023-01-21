from django.urls import path
from . import views

app_name = 'sanke'
urlpatterns = [
    path("", views.sanke, name="sanke")
]