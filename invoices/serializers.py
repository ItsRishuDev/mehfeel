from rest_framework import serializers
from invoices.models import Invoice, InvoiceItem

class InvoiceSerializers(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = "__all__"


class InvoiceItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = "__all__"
