# Generated by Django 5.1.7 on 2025-03-27 13:54

import django.db.models.deletion
import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("inventory", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Invoice",
            fields=[
                (
                    "invoice_id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("customer_name", models.CharField(default="", max_length=200)),
                (
                    "invoice_date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("invoice_url", models.URLField()),
                (
                    "total_amount",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
                ),
            ],
        ),
        migrations.CreateModel(
            name="InvoiceItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.PositiveIntegerField(default=1)),
                (
                    "invoice",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="invoices.invoice",
                    ),
                ),
                (
                    "item",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="inventory.item",
                    ),
                ),
            ],
        ),
    ]
