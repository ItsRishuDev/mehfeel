from uuid import uuid4
from django.db import models
from django.utils import timezone
from inventory.models import Item, AddOn


class Invoice(models.Model):
    invoice_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    customer_name = models.CharField(max_length=200, default="")
    invoice_date = models.DateTimeField(default=timezone.now)
    invoice_url = models.URLField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Invoice {self.invoice_id} - {self.customer_name}"


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="items")
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    item_name_at_purchase = models.CharField(max_length=200, blank=True)
    item_price_at_purchase = models.PositiveIntegerField(default=0)

    @property
    def total_price(self):
        return self.quantity * self.item_price_at_purchase

    def __str__(self):
        return f"{self.item_name_at_purchase} - {self.quantity} x {self.item_price_at_purchase}"

    def save(self, *args, **kwargs):
        if self.item:
            self.item_name_at_purchase = self.item.name
            self.item_price_at_purchase = self.item.price
        super().save(*args, **kwargs)


class InvoiceItemAddOn(models.Model):
    invoice_item = models.ForeignKey(InvoiceItem, on_delete=models.CASCADE)
    add_on = models.ForeignKey(AddOn, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    addon_name_at_purchase = models.CharField(max_length=200, blank=True)
    addon_price_at_purchase = models.PositiveIntegerField(default=0)

    @property
    def total_price(self):
        return self.quantity * self.addon_price_at_purchase

    def __str__(self):
        return f"{self.addon_name_at_purchase} - {self.quantity} x {self.addon_price_at_purchase}"

    def save(self, *args, **kwargs):
        if self.add_on:
            self.addon_name_at_purchase = self.add_on.name
            self.addon_price_at_purchase = self.add_on.price
        super().save(*args, **kwargs)
