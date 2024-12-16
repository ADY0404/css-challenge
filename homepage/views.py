from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'homepage/home.html')

def signup (request):
    return render(request, 'users/signup.html')

def community (request):
    return render(request, 'homepage/community.html')

def community2 (request):
    return render(request, 'homepage/community2.html')


# @login_required
# def profile_view(request):
#     return render(request, 'template_name.html', {
#         'user': request.user
#     })
