from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile

# Create your views here.

# @login_required
# def profile(request):
#     if request.method == 'POST':
#         user = request.user
#         user.first_name = request.POST.get('first_name')
#         user.last_name = request.POST.get('last_name')
#         user.email = request.POST.get('email')

#         profile = user.profile
#         profile.year = request.POST.get('year')
#         if 'profile_picture' in request.FILES:
#             profile.profile_picture = request.FILES['profile_picture']

#         password = request.POST.get('password')
#         if password:
#             user.set_password(password)

#         user.save()
#         profile.save()
#         messages.success(request, 'Your profile was updated successfully!')
#         return redirect('profile')

#     return render(request, 'users/profile.html')

# from .forms import SignUpForm

# def signup_view(request):
#     form = SignUpForm()
#     if request.method == 'POST':
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             # Process form data here
#             pass
#     return render(request, 'signup.html', {'form': form})
