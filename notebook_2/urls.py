from django.urls import path
from . import views

app_name = 'notebook_2'
urlpatterns = [
    path('', views.containersView.as_view(), name='containers'),
    path('container/<int:pk>/', views.containerDetailView.as_view(), name='container_detail'),
    path('new/container', views.containerCreateView.as_view(), name='container_create'),
    path('edit/container/<int:pk>/', views.containerUpdateView.as_view(), name='container_update'),
    path('delete/container/<int:pk>/', views.containerDeleteView.as_view(), name='container_delete'),

    path('collapse/<int:pk>/', views.containerCollapse, name='container_collapse'),
    path('changeTab/<int:pk>/', views.containerChangeTab, name='container_changeTab'),

    path('new/item', views.itemCreateView.as_view(), name='item_create'),
    path('edit/item/<int:pk>/', views.itemUpdateView.as_view(), name='item_update'),
    path('delete/item/<int:pk>/', views.itemDeleteView.as_view(), name='item_delete'),

    path('done/<int:pk>/', views.itemDone, name='item_done'),

    path('search/', views.searchView.as_view(), name='search'),

    path('login/', views.loginView.as_view(), name="login"),
    path('logout/', views.logoutView.as_view(), name="logout"),
    path('register/', views.registerView.as_view(), name="register"),
    ]