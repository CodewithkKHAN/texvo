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
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db import transaction
from datetime import date
from invoice_manager.models import Client, Product, Invoice, InvoiceItem, Payment

# POS view
def pos_view(request):
    clients = Client.objects.all()
    products = Product.objects.all()
    return render(request, 'pos/pos.html', {
        'clients': clients,
        'products': products,
    })

@require_POST
def create_invoice_from_pos(request):
    try:
        with transaction.atomic():
            # Get client ID and validate
            client_id = request.POST.get('client_id')
            if not client_id:
                return JsonResponse({'success': False, 'error': 'Client ID is required.'})
            client = get_object_or_404(Client, id=client_id)

            # Get payment amount and validate
            try:
                payment_amount = float(request.POST.get('payment_amount', 0))
            except ValueError:
                return JsonResponse({'success': False, 'error': 'Invalid payment amount.'})

            # Get items and validate
            items = request.POST.getlist('items[]')
            if not items:
                return JsonResponse({'success': False, 'error': 'No items in the cart.'})

            # Create the invoice
            invoice = Invoice.objects.create(
                client=client,
                created_date=date.today(),
                due_date=date.today(),
                amount=0,
                discount_rate=0,
                discount=0,
                tax_rate=0,
                tax_amount=0,
                shipping_charges=0,
                adjustment=0,
                balance=0,
            )

            # Process items and calculate total amount
            total_amount = 0
            for item_data in items:
                try:
                    product_id, quantity, rate = item_data.split(',')
                    product = get_object_or_404(Product, id=int(product_id))
                    quantity = int(quantity)
                    rate = float(rate)
                    amount = quantity * rate
                except (ValueError, TypeError):
                    return JsonResponse({'success': False, 'error': 'Invalid item data.'})

                # Create InvoiceItem
                InvoiceItem.objects.create(
                    invoice=invoice,
                    product=product,
                    quantity=quantity,
                    rate=rate,
                    amount=amount,
                )
                total_amount += amount

            # Update invoice totals
            invoice.amount = total_amount
            invoice.balance = total_amount - payment_amount
            invoice.save()

            # Record payment if applicable
            if payment_amount > 0:
                Payment.objects.create(
                    client=client,
                    invoice=invoice,
                    paid_amount=payment_amount,
                    payment_date=date.today(),
                    payment_mode='Cash',
                    transaction_no=f'POS-{invoice.id}',
                )

        return JsonResponse({"success": True, "invoice_id": invoice.id})

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})