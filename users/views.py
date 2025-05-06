from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.hashers import make_password


# def login_view(request):
#     """
#     Handles user login functionality.
#     """
#     if request.method == "POST":
#         username = request.POST.get("username")  # Retrieve 'username' from form
#         password = request.POST.get("password")  # Retrieve 'password' from form

#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             messages.success(request, f"Welcome back, {username}!")
#             return redirect("home")  # Redirect to home page or dashboard
#         else:
#             messages.error(request, "Invalid username or password.")

#     return render(request, "login.html")  # Render login template

# from django.shortcuts import redirect

def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")  # Redirect already logged-in users

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {username}!")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "users/login.html")

def update_profile(request):
    if request.method == 'POST':
        # Fetch the user and profile objects
        user = request.user
        profile = user.profile  # Assuming a OneToOne relationship with User

        # Handle profile picture update
        profile_picture = request.FILES.get('profile_picture')
        if profile_picture:
            profile.profile_picture = profile_picture

        # Update user's first and last name
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)

        # Update profile year
        year = request.POST.get('year')
        if year:
            profile.year = year

        # Update password if provided
        password = request.POST.get('password')
        if password:
            user.password = make_password(password)

        # Save changes
        user.save()
        profile.save()

        # Show success message
        messages.success(request, 'Your profile has been updated successfully!')
        return redirect('update_profile')  # Redirect to the same page after saving

    return render(request, 'users/profile.html')
