from django.db.models.signals import post_save, post_delete
from django.db import transaction
from django.dispatch import receiver
from .models import InvoiceItem, Product, Invoice, Payment, Client

@receiver(post_save, sender=InvoiceItem)
def reduce_product_stock_on_create(sender, instance, created, **kwargs):
    if created:
        product = instance.product
        quantity = instance.quantity

        with transaction.atomic():
            if product.current_stock < quantity:
                raise ValueError(f"Not enough stock for product {product.name}! Current stock: {product.current_stock}, tried to sell: {quantity}")
            product.current_stock -= quantity
            product.save()

@receiver(post_delete, sender=InvoiceItem)
def restore_product_stock_on_delete(sender, instance, **kwargs):
    product = instance.product
    quantity = instance.quantity

    with transaction.atomic():
        product.current_stock += quantity
        product.save()

@receiver(post_save, sender=Invoice)
def update_client_balance_on_invoice(sender, instance, created, **kwargs):
    if created:
        client = instance.client
        amount = instance.amount or 0

        with transaction.atomic():
            client.balance += amount
            client.save()

        update_invoice_payment_status(instance)

@receiver(post_save, sender=Payment)
def update_client_balance_on_payment(sender, instance, created, **kwargs):
    if created:
        client = instance.client
        paid_amount = instance.paid_amount or 0

        with transaction.atomic():
            client.balance -= paid_amount
            client.save()

        if instance.invoice:
            update_invoice_payment_status(instance.invoice)

def update_invoice_payment_status(invoice):
    if invoice.balance <= 0:
        invoice.payment_status = 'paid'
    elif invoice.balance >= invoice.amount:
        invoice.payment_status = 'unpaid'
    else:
        invoice.payment_status = 'partial'
    invoice.save(update_fields=['payment_status'])
