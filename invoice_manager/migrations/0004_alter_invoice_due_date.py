# Generated by Django 5.2 on 2025-04-25 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice_manager', '0003_invoice_gross_total_invoice_invoice_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='due_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
