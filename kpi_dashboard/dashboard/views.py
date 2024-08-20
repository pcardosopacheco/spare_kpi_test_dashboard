# dashboard/views.py
from django.shortcuts import render
from django.contrib import messages
from .models import KPI
from .fetch_data import fetch_ridership_data, fetch_duty_data
from .calculate_kpis import calculate_ridership_kpis
import json


def update_kpis(request):
    ridership_data = fetch_ridership_data()
    with open('dashboard/ridership_data.json', 'w') as f:
        json.dump(ridership_data, f)

    kpi_data = calculate_ridership_kpis(ridership_data)
    KPI.objects.all().delete()
    for key, value in kpi_data.items():
        KPI.objects.create(key=key, value=value)
    
    messages.success(request, 'KPI data updated successfully!')
    context = {'kpi_data': json.dumps(kpi_data, indent=4)}
    return render(request, 'dashboard/update_kpis.html', context)

def show_dashboard(request):
    kpis = KPI.objects.all()
    for kpi in kpis:
        print(f"{kpi.key}: {kpi.value}")  # Print KPIs to the console for debugging
    return render(request, 'dashboard/dashboard.html', {'kpis': kpis})


