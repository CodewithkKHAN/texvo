# filepath: /Users/abc/Documents/TEXVO/texvo/invoice_manager/views.py
from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>Welcome to the Invoice Manager App</h1>")

from django.shortcuts import render
import json

def dashboard_view(request):
    labels = ['January', 'February', 'March']
    totals = [100, 200, 300]
    return render(request, 'dashboard.html', {
        'labels': json.dumps(labels),
        'totals': json.dumps(totals),
    })