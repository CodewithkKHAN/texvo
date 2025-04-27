from decimal import Decimal
from django.db import models

# --- Clients and Suppliers ---
class Client(models.Model):
    organization_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.TextField()
    contact_person = models.CharField(max_length=255)
    tax_id = models.CharField(max_length=100, blank=True, null=True)
    business_detail = models.TextField(blank=True, null=True)
    shipping_address = models.TextField(blank=True, null=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    total_invoices = models.PositiveIntegerField(default=0)
    unpaid_invoices = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.organization_name

class Supplier(models.Model):
    organization_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.TextField()
    contact_person = models.CharField(max_length=255)
    tax_id = models.CharField(max_length=100, blank=True, null=True)
    business_detail = models.TextField(blank=True, null=True)
    shipping_address = models.TextField(blank=True, null=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    total_purchase = models.PositiveIntegerField(default=0)
    unpaid_purchase = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.organization_name

class Product(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    buy_rate = models.DecimalField(max_digits=10, decimal_places=2)
    sale_rate = models.DecimalField(max_digits=10, decimal_places=2)
    measurement_units = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    current_stock = models.IntegerField(default=0)
    minimum_stock = models.PositiveIntegerField(default=0)
    opening_stock = models.PositiveIntegerField(default=0)
    opening_stock_rate = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    opening_date = models.DateField(blank=True, null=True)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    tax_list = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Invoice(models.Model):
    invoice_number = models.CharField(max_length=100, unique=True, blank=True)
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    created_date = models.DateField()
    due_date = models.DateField(blank=True, null=True)
    reference = models.CharField(max_length=100, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    shipping_charges = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    adjustment = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    ship_to = models.TextField(blank=True)
    gross_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    PAYMENT_STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('partial', 'Partially Paid'),
        ('unpaid', 'Unpaid'),
    ]
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='unpaid')

    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.client}"

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            last_id = Invoice.objects.count() + 1
            self.invoice_number = f"INV-AUTO-{last_id}"
        super().save(*args, **kwargs)

class Service(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    sale_rate = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    description = models.TextField(blank=True, null=True)
    is_inhouse = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class ServicePartUsage(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="parts_used")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity_used = models.PositiveIntegerField()
    source = models.CharField(
        max_length=20,
        choices=[('inventory', 'Inventory'), ('supplier', 'Supplier')],
        default='inventory'
    )

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    measurement_unit = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    rate = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    tax = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.invoice} (Qty: {self.product})"

class InvoiceServiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    rate = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), blank=True, null=True)
    tax = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    description = models.TextField(blank=True, null=True)

class Payment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    contact_person = models.CharField(max_length=255, blank=True, null=True)
    transaction_no = models.CharField(max_length=100)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    payment_date = models.DateField(blank=True, null=True)
    payment_mode = models.CharField(max_length=50, default='Cash')

    def __str__(self):
        return f"Payment {self.transaction_no} - {self.client}"

class CreditNote(models.Model):
    number = models.CharField(max_length=100)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    reference = models.CharField(max_length=100, blank=True)
    created_date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    balance = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Credit Note {self.number} - {self.client}"

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('rent', 'Rent'),
        ('electricity', 'Electricity'),
        ('maintenance', 'Maintenance'),
        ('software', 'Software'),
    ]
    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    date = models.DateField()
    recurring = models.BooleanField(default=False)
    frequency = models.CharField(
        max_length=20,
        choices=[('weekly', 'Weekly'), ('monthly', 'Monthly')],
        blank=True, null=True
    )
    next_due_date = models.DateField(blank=True, null=True)
