from django.db import models
from django.utils import timezone
from inventory.models import Item
from uuid import uuid4

# Create your models here.


class Invoice(models.Model):
    invoice_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    customer_name = models.CharField(max_length=200, default="")
    invoice_date = models.DateTimeField(default=timezone.now)
    invoice_url = models.URLField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Invoice {self.id} - {self.customer_name}"


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        if self.item:
            return self.quantity * self.item.price
        else:
            return 0

    def __str__(self):
        if self.item:
            return f"{self.item.name} - {self.quantity} x {self.item.price}"
        else:
            return "Item Deleted"
