from django.contrib import admin
from django.contrib.admin import AdminSite
from django.urls import path
from django.template.response import TemplateResponse
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from datetime import datetime
import json
from .models import (
    Client, Supplier, Product, Invoice, InvoiceItem, Payment, CreditNote, 
    Service, InvoiceServiceItem, Expense
)

# Customizing the Admin Site
class InvoiceManagerAdminSite(AdminSite):
    site_header = "Invoice Manager Dashboard"
    site_title = "Invoice Manager Admin"
    index_title = "Welcome to the Invoice Manager Dashboard"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.dashboard_view, name='dashboard'),
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        monthly_data = (
            Payment.objects
            .annotate(month=TruncMonth('date'))
            .values('month')
            .annotate(total=Sum('paid_amount'))
            .order_by('month')
        )
        labels = [entry['month'].strftime('%B') for entry in monthly_data]
        totals = [float(entry['total']) for entry in monthly_data]

        top_products = (
            InvoiceItem.objects
            .values('product__name')
            .annotate(total_sold=Sum('quantity'))
            .order_by('-total_sold')[:5]
        )

        unpaid_total = Invoice.objects.filter(balance__gt=0).aggregate(total=Sum('balance'))['total'] or 0
        unpaid_count = Invoice.objects.filter(balance__gt=0).count()

        upcoming_expenses = Expense.objects.filter(recurring=True, date__gte=datetime.today()).order_by('date')[:5]

        context = {
            'total_clients': Client.objects.count(),
            'total_invoices': Invoice.objects.count(),
            'total_payments': Payment.objects.aggregate(total_paid=Sum('paid_amount'))['total_paid'] or 0,
            'total_products': Product.objects.count(),
            'labels': json.dumps(labels),
            'totals': json.dumps(totals),
            'cards': [
                ("Total Clients", Client.objects.count(), 'admin:invoice_manager_client_changelist'),
                ("Total Invoices", Invoice.objects.count(), 'admin:invoice_manager_invoice_changelist'),
                ("Total Payments", Payment.objects.aggregate(total_paid=Sum('paid_amount'))['total_paid'] or 0, 'admin:invoice_manager_payment_changelist'),
                ("Total Products", Product.objects.count(), 'admin:invoice_manager_product_changelist'),
            ],
            'top_products': top_products,
            'unpaid_count': unpaid_count,
            'unpaid_total': unpaid_total,
            'upcoming_expenses': upcoming_expenses
        }
        return TemplateResponse(request, "admin/dashboard.html", context)

# Instantiate the custom admin site
admin_site = InvoiceManagerAdminSite(name='invoice_manager_admin')

# Register models with the custom admin site
@admin.register(Client, site=admin_site)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('organization_name', 'contact_number', 'email', 'balance')
    search_fields = ('organization_name', 'email')
    list_filter = ('balance',)

@admin.register(Supplier, site=admin_site)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('organization_name', 'contact_number', 'email', 'balance')
    search_fields = ('organization_name', 'email')
    list_filter = ('balance',)

@admin.register(Product, site=admin_site)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'sale_rate', 'current_stock', 'minimum_stock')
    search_fields = ('name', 'code')
    list_filter = ('current_stock',)

@admin.register(Invoice, site=admin_site)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'client', 'created_date', 'amount', 'balance')
    search_fields = ('invoice_number', 'client__organization_name')
    list_filter = ('created_date',)

@admin.register(InvoiceItem, site=admin_site)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'product', 'quantity', 'rate', 'amount')
    search_fields = ('invoice__invoice_number', 'product__name')
    list_filter = ('quantity',)

@admin.register(Payment, site=admin_site)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('transaction_no', 'client', 'paid_amount', 'invoice')
    search_fields = ('transaction_no', 'client__organization_name')
    list_filter = ('paid_amount',)

@admin.register(CreditNote, site=admin_site)
class CreditNoteAdmin(admin.ModelAdmin):
    list_display = ('number', 'client', 'created_date', 'amount', 'balance')
    search_fields = ('number', 'client__organization_name')
    list_filter = ('created_date',)

@admin.register(Service, site=admin_site)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'sale_rate', 'is_inhouse')
    search_fields = ('name', 'code')
    list_filter = ('is_inhouse',)

@admin.register(InvoiceServiceItem, site=admin_site)
class InvoiceServiceItemAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'service', 'quantity', 'rate', 'amount')
    search_fields = ('invoice__invoice_number', 'service__name')
    list_filter = ('quantity',)

@admin.register(Expense, site=admin_site)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('title', 'amount', 'category', 'date', 'recurring')
    search_fields = ('title', 'category')
    list_filter = ('category', 'recurring')