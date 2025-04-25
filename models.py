# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    first_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    action_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class InvoiceManagerClient(models.Model):
    organization_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=50)
    email = models.CharField(max_length=254)
    address = models.TextField()
    contact_person = models.CharField(max_length=255)
    tax_id = models.CharField(max_length=100, blank=True, null=True)
    business_detail = models.TextField(blank=True, null=True)
    shipping_address = models.TextField(blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    total_invoices = models.PositiveIntegerField()
    unpaid_invoices = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'invoice_manager_client'


class InvoiceManagerCreditnote(models.Model):
    number = models.CharField(max_length=100)
    reference = models.CharField(max_length=100)
    created_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    balance = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    client = models.ForeignKey(InvoiceManagerClient, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'invoice_manager_creditnote'


class InvoiceManagerExpense(models.Model):
    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    category = models.CharField(max_length=50)
    date = models.DateField()
    recurring = models.BooleanField()
    frequency = models.CharField(max_length=20, blank=True, null=True)
    next_due_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'invoice_manager_expense'


class InvoiceManagerInvoice(models.Model):
    number = models.CharField(max_length=100)
    created_date = models.DateField()
    due_date = models.DateField()
    reference = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    discount_rate = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    discount = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    tax_rate = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    tax_amount = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    shipping_charges = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    adjustment = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    balance = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    ship_to = models.TextField()
    gross_amount = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    client = models.ForeignKey(InvoiceManagerClient, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'invoice_manager_invoice'


class InvoiceManagerInvoiceitem(models.Model):
    measurement_unit = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    rate = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    discount_rate = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    discount = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    tax = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    tax_amount = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    amount = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    description = models.TextField()
    invoice = models.ForeignKey(InvoiceManagerInvoice, models.DO_NOTHING)
    product = models.ForeignKey('InvoiceManagerProduct', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'invoice_manager_invoiceitem'


class InvoiceManagerInvoiceserviceitem(models.Model):
    quantity = models.PositiveIntegerField()
    rate = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    amount = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    discount = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    tax = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    tax_amount = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    description = models.TextField()
    invoice = models.ForeignKey(InvoiceManagerInvoice, models.DO_NOTHING)
    service = models.ForeignKey('InvoiceManagerService', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'invoice_manager_invoiceserviceitem'


class InvoiceManagerPayment(models.Model):
    contact_person = models.CharField(max_length=255)
    transaction_no = models.CharField(max_length=100)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    date = models.DateField()
    client = models.ForeignKey(InvoiceManagerClient, models.DO_NOTHING)
    invoice = models.ForeignKey(InvoiceManagerInvoice, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'invoice_manager_payment'


class InvoiceManagerProduct(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(unique=True, max_length=50)
    buy_rate = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    sale_rate = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    measurement_units = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    current_stock = models.PositiveIntegerField()
    minimum_stock = models.PositiveIntegerField()
    opening_stock = models.PositiveIntegerField()
    opening_stock_rate = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    opening_date = models.DateField()
    tax_rate = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    tax_list = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'invoice_manager_product'


class InvoiceManagerService(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(unique=True, max_length=50)
    cost = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    sale_rate = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    description = models.TextField(blank=True, null=True)
    is_inhouse = models.BooleanField()
    supplier = models.ForeignKey('InvoiceManagerSupplier', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'invoice_manager_service'


class InvoiceManagerServicepartusage(models.Model):
    quantity_used = models.PositiveIntegerField()
    source = models.CharField(max_length=20)
    product = models.ForeignKey(InvoiceManagerProduct, models.DO_NOTHING, blank=True, null=True)
    service = models.ForeignKey(InvoiceManagerService, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'invoice_manager_servicepartusage'


class InvoiceManagerSupplier(models.Model):
    organization_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=50)
    email = models.CharField(max_length=254)
    address = models.TextField()
    contact_person = models.CharField(max_length=255)
    tax_id = models.CharField(max_length=100, blank=True, null=True)
    business_detail = models.TextField(blank=True, null=True)
    shipping_address = models.TextField(blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    total_purchase = models.PositiveIntegerField()
    unpaid_purchase = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'invoice_manager_supplier'
