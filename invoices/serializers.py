from datetime import datetime
from rest_framework import serializers
from invoices.models import Invoice, InvoiceItem, InvoiceItemAddOn
from inventory.models import Item, AddOn
from inventory.serializers import ItemSerializer


class InvoiceItemAddOnDetailSerializer(serializers.ModelSerializer):
    addon_name = serializers.CharField(source="addon_name_at_purchase")
    addon_price = serializers.CharField(source="addon_price_at_purchase")

    class Meta:
        model = InvoiceItemAddOn
        fields = ["id", "addon_name", "addon_price", "quantity"]


class InvoiceItemDetailSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source="item_name_at_purchase")
    item_price = serializers.CharField(source="item_price_at_purchase")
    item_addons = InvoiceItemAddOnDetailSerializer(many=True)

    class Meta:
        model = InvoiceItem
        fields = ["id", "item_name", "item_price", "quantity", "item_addons"]


class InvoiceDetailSerializer(serializers.ModelSerializer):
    items = InvoiceItemDetailSerializer(many=True)

    class Meta:
        model = Invoice
        fields = [
            "invoice_id",
            "customer_name",
            "invoice_date",
            "invoice_url",
            "total_amount",
            "invoice_items",
        ]


class AllInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = "__all__"


class BaseItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    quantity = serializers.IntegerField()


class ItemAddOnSerializer(BaseItemSerializer):
    pass


class ItemSerializer(BaseItemSerializer):
    add_ons = ItemAddOnSerializer(many=True, required=False)

    def validate_add_ons(self, add_ons):
        if add_ons:
            add_on_ids = set()
            for add_on in add_ons:
                add_on_ids.add(add_on["id"])

            add_on_response = AddOn.objects.filter(id__in=list(add_on_ids))
            if len(add_on_response) != len(add_on_ids):
                raise serializers.ValidationError("Invalid add_on id provided")

            db_add_ons = {db_add_on.id: db_add_on for db_add_on in add_on_response}

            for add_on in add_ons:
                add_on["add_on"] = db_add_ons[add_on["id"]]

        return add_ons


class InvoiceSerializer(serializers.Serializer):
    customer_name = serializers.CharField()
    invoice_date = serializers.DateTimeField(default=datetime.now)
    items = ItemSerializer(many=True, required=True)

    def validate_items(self, items):
        if not items:
            raise serializers.ValidationError("At least one item is required.")

        item_ids = set()
        for item in items:
            item_ids.add(item["id"])

        items_response = Item.objects.filter(id__in=list(item_ids))

        if len(items_response) != len(item_ids):
            raise serializers.ValidationError("Invalid item id provided")

        db_items = {db_item.id: db_item for db_item in items_response}

        for item in items:
            item["item"] = db_items[item["id"]]

        return items

    def create(self, validated_data):
        items_data = validated_data.pop("items", [])
        invoice_amount = 0
        invoice = Invoice.objects.create(**validated_data)
        for item in items_data:
            addons_data = item.pop("add_ons", [])
            item.pop("id")
            invoice_amount += item.get("item").price * item.get("quantity")
            invoice_item = InvoiceItem.objects.create(invoice=invoice, **item)
            for addon in addons_data:
                addon.pop("id")
                invoice_amount += addon.get("add_on").price * addon.get("quantity")
                InvoiceItemAddOn.objects.create(invoice_item=invoice_item, **addon)

        invoice.total_amount = invoice_amount
        invoice.save()
        return invoice
