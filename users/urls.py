from django.urls import path
from .views import login_view, update_profile

urlpatterns = [
    path("login/", login_view, name="login"),
    path("profile/", update_profile, name="profile"),
    
]