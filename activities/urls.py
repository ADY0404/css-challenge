from django.urls import path
from . import views

app_name = 'activities'

urlpatterns = [
    path('', views.activities, name='activities_list'),
    path('event/<int:id>/', views.event_detail, name='event'),
    path('event/<int:id>/register/', views.event_register, name='event_register'),
    path('sample-events/<slug:slug>/', views.sample_event_detail, name='sample_event'),
]
