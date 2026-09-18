from django.shortcuts import render
from .models import Executive
from datetime import datetime


def executives(request):
    """Display executives filtered by academic session."""
    current_year = datetime.now().year
    # Generate academic years in descending order so the newest session is default
    academic_years = [f"{year}/{str(year+1)[-2:]}" for year in range(current_year, 2018, -1)]

    academic_year = request.GET.get('year', '').strip()
    if not academic_year and academic_years:
        academic_year = academic_years[0]  # Default to current session e.g. 2024/25

    executives_list = Executive.objects.filter(academic_year=academic_year)
    if not executives_list.exists() and not request.GET.get('year'):
        # Fallback to any published executives if current year is not yet populated
        first_available = Executive.objects.first()
        if first_available:
            academic_year = first_available.academic_year
            executives_list = Executive.objects.filter(academic_year=academic_year)

    return render(request, 'executives/executives.html', {
        'executives': executives_list,
        'academic_year': academic_year,
        'academic_years': academic_years,
    })
