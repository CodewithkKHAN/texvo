from django.contrib import admin
from django.contrib.admin import AdminSite
from django.urls import path
from django.template.response import TemplateResponse
from django.db.models import Sum
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
        # Example metrics
        context = {
            'total_clients': Client.objects.count(),
            'total_invoices': Invoice.objects.count(),
            'total_payments': Payment.objects.aggregate(total_paid=Sum('paid_amount'))['total_paid'] or 0,
            'total_products': Product.objects.count(),
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