from django.contrib import admin
from invoices.models import Invoice, InvoiceItem, InvoiceItemAddOn

# Register your models here.

admin.site.register(Invoice)
admin.site.register(InvoiceItem)
admin.site.register(InvoiceItemAddOn)
