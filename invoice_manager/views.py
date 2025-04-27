from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.db import transaction
from datetime import date
import json
from invoice_manager.models import Client, Product, Invoice, InvoiceItem, Payment

# POS Home
def home(request):
    return HttpResponse("<h1>Welcome to the Invoice Manager App</h1>")

# Dashboard View
def dashboard_view(request):
    labels = ['January', 'February', 'March']
    totals = [100, 200, 300]
    return render(request, 'dashboard.html', {
        'labels': json.dumps(labels),
        'totals': json.dumps(totals),
    })

# POS View
def pos_view(request):
    clients = Client.objects.all()
    products = Product.objects.all()
    return render(request, 'pos/pos.html', {
        'clients': clients,
        'products': products,
    })

# POS Create Invoice
@require_POST
def create_invoice_from_pos(request):
    try:
        with transaction.atomic():
            client_id = request.POST.get('client_id')
            if not client_id:
                return JsonResponse({'success': False, 'error': 'Client ID is required.'})

            client = get_object_or_404(Client, id=client_id)

            try:
                payment_amount = Decimal(request.POST.get('payment_amount', '0'))
            except Exception:
                payment_amount = Decimal('0.00')

            items = request.POST.getlist('items[]')
            if not items:
                return JsonResponse({'success': False, 'error': 'Cart is empty!'})

            invoice = Invoice.objects.create(
                client=client,
                created_date=date.today(),
                due_date=date.today(),
                amount=Decimal('0.00'),
                discount_rate=Decimal('0.00'),
                discount=Decimal('0.00'),
                tax_rate=Decimal('0.00'),
                tax_amount=Decimal('0.00'),
                shipping_charges=Decimal('0.00'),
                adjustment=Decimal('0.00'),
                balance=Decimal('0.00'),
            )

            total_amount = Decimal('0.00')
            for item_data in items:
                try:
                    product_id, quantity, rate = item_data.split(',')
                    product = get_object_or_404(Product, id=int(product_id))
                    quantity = int(quantity)
                    rate = Decimal(rate)
                    amount = quantity * rate
                except Exception:
                    return JsonResponse({'success': False, 'error': 'Invalid cart item data.'})

                InvoiceItem.objects.create(
                    invoice=invoice,
                    product=product,
                    quantity=quantity,
                    rate=rate,
                    amount=amount,
                    measurement_unit=product.measurement_units or '',
                    discount_rate=Decimal('0.00'),
                    discount=Decimal('0.00'),
                    tax=Decimal('0.00'),
                    tax_amount=Decimal('0.00'),
                    description=product.description or ''
                )

                total_amount += amount

            invoice.amount = total_amount
            invoice.balance = total_amount - payment_amount
            invoice.save()

            if payment_amount > 0:
                Payment.objects.create(
                    client=client,
                    invoice=invoice,
                    paid_amount=payment_amount,
                    payment_date=date.today(),
                    payment_mode='Cash',
                    transaction_no=f"POS-{invoice.id}"
                )

        return JsonResponse({'success': True, 'invoice_id': invoice.id})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
