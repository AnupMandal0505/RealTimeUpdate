from django.shortcuts import render
from django.http import JsonResponse
from .models import Appointment

# Create your views here.

def index(request):
    appointments = Appointment.objects.all()
    return render(request, 'myapp/index.html', {'appointments': appointments})

def get_appointments(request):
    appointments = list(Appointment.objects.values('id', 'name', 'status'))
    return JsonResponse({'data': appointments})
