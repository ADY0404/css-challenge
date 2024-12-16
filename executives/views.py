from django.shortcuts import render
from .models import Executive
from datetime import datetime

# Create your views here.

def executives(request):
    # Generate academic years from 2000 to the current year
    current_year = datetime.now().year
    academic_years = [f"{year}/{str(year+1)[-2:]}" for year in range(2017, current_year+1)]
    
    # Get the selected year from the request, default to None
    academic_year = request.GET.get('year', '')
    
    # Filter executives only if a valid year is selected
    executives = Executive.objects.filter(academic_year=academic_year) if academic_year else Executive.objects.none()

    return render(request, 'executives/executives.html', {
        'executives': executives,
        'academic_year': academic_year,
        'academic_years': academic_years,
    })
