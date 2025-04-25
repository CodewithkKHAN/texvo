from django.core.management.base import BaseCommand
import csv
from datetime import datetime
from invoice_manager.models import Client, Supplier, Product
from django.utils.dateparse import parse_date

# --- Import Clients, Suppliers, Products ---
class Command(BaseCommand):
    help = 'Import clients, suppliers, or products from CSV files'

    def add_arguments(self, parser):
        parser.add_argument('mode', type=str, help='clients | suppliers | products')
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        mode = kwargs['mode']
        csv_file = kwargs['csv_file']

        if mode == 'clients':
            self.import_clients(csv_file)
        elif mode == 'suppliers':
            self.import_suppliers(csv_file)
        elif mode == 'products':
            self.import_products(csv_file)
        else:
            self.stdout.write(self.style.ERROR("Invalid mode. Use 'clients', 'suppliers', or 'products'."))

    def safe_int(self, value):
        try:
            if value is None:
                return 0
            value = str(value).strip()
            return int(float(value))
        except (ValueError, TypeError):
            return 0

    def safe_float(self, value):
        try:
            return float(str(value).strip())
        except (ValueError, TypeError):
            return 0.0

    def import_clients(self, path):
        with open(path, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                client, created = Client.objects.get_or_create(
                    organization_name=row['Organization Name'],
                    contact_number=row['Contact Number'],
                    email=row['Email'],
                    address=row['Address'],
                    contact_person=row['Contact Person'],
                    tax_id=row.get('Tax Id') or None,
                    business_detail=row.get('Business Detail') or None,
                    shipping_address=row.get('Shipping Address') or None,
                    defaults={
                        'balance': self.safe_float(row.get('Balance')),
                        'total_invoices': self.safe_int(row.get('Total Invoices')),
                        'unpaid_invoices': self.safe_int(row.get('Unpaid Invoices'))
                    }
                )
                action = 'Created' if created else 'Exists'
                self.stdout.write(self.style.SUCCESS(f'{action} Client: {client.organization_name}'))

    def import_suppliers(self, path):
        with open(path, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                supplier, created = Supplier.objects.get_or_create(
                    organization_name=row['Organization Name'],
                    contact_number=row['Contact Number'],
                    email=row['Email'],
                    address=row['Address'],
                    contact_person=row['Contact Person'],
                    tax_id=row.get('Tax Id') or None,
                    business_detail=row.get('Business Detail') or None,
                    shipping_address=row.get('Shipping Address') or None,
                    defaults={
                        'balance': self.safe_float(row.get('Balance')),
                        'total_purchase': self.safe_int(row.get('Total Purchase')),
                        'unpaid_purchase': self.safe_int(row.get('Unpaid Purchase'))
                    }
                )
                action = 'Created' if created else 'Exists'
                self.stdout.write(self.style.SUCCESS(f'{action} Supplier: {supplier.organization_name}'))

    def import_products(self, path):
        with open(path, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    product = Product.objects.filter(code=row['Product Code']).first()
                    if not product:
                        fields = {
                            'name': row['Product Name'],
                            'code': row['Product Code'],
                            'buy_rate': self.safe_float(row['Buy Rate']),
                            'sale_rate': self.safe_float(row['Sale Rate']),
                            'measurement_units': row['Measurement Units'],
                            'description': row.get('Description') or '',
                            'current_stock': self.safe_int(row['Current Stock']),
                            'minimum_stock': self.safe_int(row['Minimum Stock']),
                            'opening_stock': self.safe_int(row['Opening Stock']),
                            'opening_stock_rate': self.safe_float(row['Opening Stock Rate']),
                            'opening_date': parse_date(row['Opening Date']),
                            'tax_rate': self.safe_float(row['Tax Rate']),
                            'tax_list': row.get('Tax List') or ''
                        }
                        self.stdout.write(f"Creating product with data: {fields}")
                        product = Product.objects.create(**fields)
                        self.stdout.write(self.style.SUCCESS(f'Created Product: {product.name}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'Exists Product: {product.name}'))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Failed to import product: {row.get('Product Name', 'N/A')} | Error: {e}"))
