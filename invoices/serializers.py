from rest_framework import serializers
from invoices.models import Invoice, InvoiceItem, InvoiceItemAddOn


class InvoiceItemAddOnSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItemAddOn
        fields = "__all__"


class InvoiceItemSerializer(serializers.ModelSerializer):
    add_ons = InvoiceItemAddOnSerializer(many=True)

    class Meta:
        model = InvoiceItem
        fields = "__all__"


class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True)

    class Meta:
        model = Invoice
        fields = [
            "invoice_id",
            "customer_name",
            "invoice_date",
            "invoice_url",
            "total_amount",
            "items",
        ]

    def create(self, validated_data):
        items_data = validated_data.pop("items", [])
        # invoice_amount = 0
        invoice = Invoice.objects.create(**validated_data)
        for item in items_data:
            addons_data = item.pop("add_on", [])
            invoice_item = InvoiceItem.objects.create(invoice=invoice, **item)
            for addon in addons_data:
                InvoiceItem.objects.create(invoice_item=invoice_item, **addon)


class ItemAddOnRequestSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    quantity = serializers.IntegerField()


class ItemRequestSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    add_ons = ItemAddOnRequestSerializer(many=True)


class InvoiceRequestSerializer(serializers.Serializer):
    customer_name = serializers.CharField()
    date = serializers.DateTimeField()
    items = ItemRequestSerializer(many=True)
