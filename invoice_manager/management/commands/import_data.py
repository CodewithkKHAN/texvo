from django.core.management.base import BaseCommand
import csv
from datetime import datetime
from invoice_manager.models import Client, Supplier, Product, Invoice, InvoiceItem, Payment, CreditNote
from django.utils.dateparse import parse_date
import os

# --- Import All CSV Data into Corresponding Tables ---
class Command(BaseCommand):
    help = 'Import all CSVs into clients, suppliers, products, invoices, items, payments, and credit notes.'

    def handle(self, *args, **kwargs):
        base_dir = 'invoice_manager/data_exported'
    
        clients_csv = os.path.join(base_dir, '23Apr2025_Clients.csv')
        suppliers_csv = os.path.join(base_dir, '23Apr2025_Suppliers.csv')
        products_csv = os.path.join(base_dir, '23Apr2025_Products.csv')
        invoices_csv = os.path.join(base_dir, '23Apr2025_Invoices.csv')
        items_csv = os.path.join(base_dir, '23Apr2025_InvoiceItems.csv')
        payments_csv = os.path.join(base_dir, '23Apr2025_Payments.csv')
        creditnotes_csv = os.path.join(base_dir, '23Apr2025_CreditNote.csv')
    
        # Clear existing data
        CreditNote.objects.all().delete()
        Payment.objects.all().delete()
        InvoiceItem.objects.all().delete()
        Invoice.objects.all().delete()
        Product.objects.all().delete()
        Supplier.objects.all().delete()
        Client.objects.all().delete()
        self.stdout.write(self.style.WARNING("Deleted existing records from all tables."))
    
        self.import_clients(clients_csv)
        self.import_suppliers(suppliers_csv)
        self.import_products(products_csv)
        self.import_invoices(invoices_csv)
        self.import_invoice_items(items_csv)
        self.import_payments(payments_csv)
        self.import_credit_notes(creditnotes_csv)  # Corrected method name
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

    def safe_date(self, value):
        try:
            return datetime.strptime(value.strip(), "%d %B %Y").date()
        except (ValueError, TypeError):
            return None

    def import_clients(self, path):
        with open(path, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Client.objects.create(
                    organization_name=row['Organization Name'],
                    contact_number=row['Contact Number'],
                    email=row['Email'],
                    address=row['Address'],
                    contact_person=row['Contact Person'],
                    tax_id=row.get('Tax Id') or None,
                    business_detail=row.get('Business Detail') or None,
                    shipping_address=row.get('Shipping Address') or None,
                    balance=self.safe_float(row.get('Balance')),
                    total_invoices=self.safe_int(row.get('Total Invoices')),
                    unpaid_invoices=self.safe_int(row.get('Unpaid Invoices'))
                )
        self.stdout.write(self.style.SUCCESS("Imported Clients."))

    def import_suppliers(self, path):
        with open(path, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Supplier.objects.create(
                    organization_name=row['Organization Name'],
                    contact_number=row['Contact Number'],
                    email=row['Email'],
                    address=row['Address'],
                    contact_person=row['Contact Person'],
                    tax_id=row.get('Tax Id') or None,
                    business_detail=row.get('Business Detail') or None,
                    shipping_address=row.get('Shipping Address') or None,
                    balance=self.safe_float(row.get('Balance')),
                    total_purchase=self.safe_int(row.get('Total Purchase')),
                    unpaid_purchase=self.safe_int(row.get('Unpaid Purchase'))
                )
        self.stdout.write(self.style.SUCCESS("Imported Suppliers."))

    def import_products(self, path):
        with open(path, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    pcode = row['Product Code'].strip()
                    pname = row['Product Name'].strip()
                    if pcode.upper() == 'N/A':
                        composite_code = pname
                    else:
                        composite_code = f"{pcode}|{pname}"

                    Product.objects.create(
                        name=pname,
                        code=composite_code,
                        buy_rate=self.safe_float(row['Buy Rate']),
                        sale_rate=self.safe_float(row['Sale Rate']),
                        measurement_units=row['Measurement Units'],
                        description=row.get('Description') or '',
                        current_stock=self.safe_int(row['Current Stock']),
                        minimum_stock=self.safe_int(row['Minimum Stock']),
                        opening_stock=self.safe_int(row['Opening Stock']),
                        opening_stock_rate=self.safe_float(row['Opening Stock Rate']),
                        opening_date=parse_date(row['Opening Date']),
                        tax_rate=self.safe_float(row['Tax Rate']),
                        tax_list=row.get('Tax List') or ''
                    )
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Failed to import product: {row.get('Product Name', 'N/A')} | Error: {e}"))
        self.stdout.write(self.style.SUCCESS("Imported Products."))

    def import_invoices(self, csv_file_path):
        with open(csv_file_path, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    # Get or create the client instance
                    client, _ = Client.objects.get_or_create(organization_name=row['Client Name'])
    
                    # Clean and parse the Tax Rate
                    tax_rate_raw = row['Tax Rate']
                    tax_rate = self.parse_tax_rate(tax_rate_raw)
    
                    # Prepare invoice data
                    invoice_data = {
                        'invoice_number': row['Invoice No.'],
                        'client': client,
                        'created_date': self.safe_date(row['Created Date']),
                        'due_date': self.safe_date(row['Due Date']) if row['Due Date'] != 'N/A' else None,
                        'reference': row['Ref. :'],
                        'amount': self.safe_float(row['Amount']),
                        'discount_rate': self.safe_float(row['Discount Rate']),
                        'discount': self.safe_float(row['Discount']),
                        'tax_rate': tax_rate,
                        'tax_amount': self.safe_float(row['Tax Amount']),
                        'shipping_charges': self.safe_float(row['Shipping Charges']),
                        'adjustment': self.safe_float(row['Adjustment']),
                        'balance': self.safe_float(row['Balance']),
                        'ship_to': row['Ship To'],
                        'gross_amount': self.safe_float(row['Gross Amount']),
                    }
    
                    # Create the invoice
                    Invoice.objects.create(**invoice_data)
                    self.stdout.write(self.style.SUCCESS(f"Successfully imported invoice: {row['Invoice No.']}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Failed to import invoice: {row['Invoice No.']} | Error: {e}"))
    
    def parse_tax_rate(self, tax_rate_raw):
        """
        Parse the Tax Rate field to extract a valid float value.
        Handles cases like '(0.0 %) 0.0' or '0.0%'.
        """
        try:
            # Remove parentheses and split by space if necessary
            tax_rate_cleaned = tax_rate_raw.replace('(', '').replace(')', '').replace('%', '').strip()
            # If there are multiple parts (e.g., '(0.0 %) 0.0'), take the last part
            tax_rate_parts = tax_rate_cleaned.split()
            return float(tax_rate_parts[-1])  # Convert the last part to float
        except (ValueError, IndexError):
            return 0.0  # Default to 0.0 if parsing fails
    def import_invoice_items(self, path):
        with open(path, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    # Fetch the related invoice
                    invoice = Invoice.objects.get(invoice_number=row['Invoice No.'])
    
                    # Fetch or create the product
                    product = None
                    if row['Product Code']:
                        product, _ = Product.objects.get_or_create(
                            code=row['Product Code'],
                            defaults={
                                'name': row['Add Items'],
                                'measurement_units': row['Measurement Unit'],
                                'sale_rate': self.safe_float(row['Rate']),
                                'buy_rate': 0.0,  # Default value for buy_rate
                                'current_stock': 0,  # Default value for current_stock
                                'minimum_stock': 0,  # Default value for minimum_stock
                                'opening_stock': 0,  # Default value for opening_stock
                                'opening_stock_rate': 0.0,  # Default value for opening_stock_rate
                                'tax_rate': 0.0,  # Default value for tax_rate
                            }
                        )
    
                    # Prepare invoice item data
                    invoice_item_data = {
                        'invoice': invoice,
                        'product': product,
                        'measurement_unit': row['Measurement Unit'],
                        'quantity': self.safe_int(row['Qty']),
                        'rate': self.safe_float(row['Rate']),
                        'discount_rate': self.safe_float(row['Discount Rate']),
                        'discount': self.safe_float(row['Discount']),
                        'tax': self.safe_float(row['Tax']),
                        'tax_amount': self.safe_float(row['Tax Amount']),
                        'amount': self.safe_float(row['Amount']),
                        'description': row['Description'],
                    }
    
                    # Create the invoice item
                    InvoiceItem.objects.create(**invoice_item_data)
                    self.stdout.write(self.style.SUCCESS(f"Successfully imported item for invoice: {row['Invoice No.']}"))
                except Invoice.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"Invoice not found: {row['Invoice No.']}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Failed to import item for invoice: {row['Invoice No.']} | Error: {e}"))
    def import_payments(self, path):
        with open(path, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    # Fetch the related invoice
                    invoice = Invoice.objects.get(invoice_number=row['Invoice No.'])
    
                    # Fetch or create the client
                    client, _ = Client.objects.get_or_create(organization_name=row['Client Name'])
    
                    # Prepare payment data
                    payment_data = {
                        'invoice': invoice,
                        'client': client,
                        'contact_person': row['Contact Person'],
                        'transaction_no': row['Transaction No.'],
                        'paid_amount': self.safe_float(row['Paid Amount']),
                        'date': self.safe_date(row['Date']),
                    }
    
                    # Create the payment
                    Payment.objects.create(**payment_data)
                    self.stdout.write(self.style.SUCCESS(f"Successfully imported payment for invoice: {row['Invoice No.']}"))
                except Invoice.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f"Invoice not found: {row['Invoice No.']}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Failed to import payment for invoice: {row['Invoice No.']} | Error: {e}"))

    def import_credit_notes(self, path):
        with open(path, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    # Fetch or create the client
                    client, _ = Client.objects.get_or_create(organization_name=row['Client Name'])
    
                    # Prepare credit note data
                    credit_note_data = {
                        'number': row['Credit Note No.'],
                        'client': client,
                        'reference': row['Ref. :'],
                        'created_date': self.safe_date(row['Created Date']),
                        'amount': self.safe_float(row['Amount']),
                        'balance': self.safe_float(row['Balance']),
                    }
    
                    # Create the credit note
                    CreditNote.objects.create(**credit_note_data)
                    self.stdout.write(self.style.SUCCESS(f"Successfully imported credit note: {row['Credit Note No.']}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Failed to import credit note: {row['Credit Note No.']} | Error: {e}"))