from django.urls import path
from . import views

app_name = 'activities'

urlpatterns = [
    path('', views.activities, name='activities_list'),
    path('event/<int:id>/', views.event_detail, name='event'),
]
