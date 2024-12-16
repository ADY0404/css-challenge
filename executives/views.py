from django.shortcuts import render
from .models import Executive

# Create your views here.

def executives(request):
    academic_year = request.GET.get('year', '2024/24')  # Default year
    executives = Executive.objects.filter(academic_year=academic_year)
    return render(request, 'executives/executives.html', {
        'executives': executives,
        'academic_year': academic_year,
    })
