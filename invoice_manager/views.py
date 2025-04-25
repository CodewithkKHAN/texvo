# filepath: /Users/abc/Documents/TEXVO/texvo/invoice_manager/views.py
from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>Welcome to the Invoice Manager App</h1>")