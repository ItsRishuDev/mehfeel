from rest_framework import serializers
from invoices.models import Invoice, InvoiceItem, InvoiceItemAddOn


class InvoiceItemAddOnSerializers(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItemAddOn
        fields = "__all__"


class InvoiceItemSerializers(serializers.ModelSerializer):
    add_ons = InvoiceItemAddOnSerializers(many=True)

    class Meta:
        model = InvoiceItem
        fields = "__all__"


class InvoiceSerializers(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = "__all__"


class InvoiceDetailSerializers(serializers.ModelSerializer):
    items = InvoiceItemSerializers(many=True)

    class Meta:
        model = InvoiceItem
        fields = "__all__"
