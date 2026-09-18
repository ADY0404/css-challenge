from django.urls import path
from . import views

app_name = 'executives'

urlpatterns = [
    path('', views.executives, name='list'),
]
