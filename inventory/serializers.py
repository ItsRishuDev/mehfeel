from rest_framework import serializers
from inventory.models import Category, Item, AddOn


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class AddOnSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddOn
        fields = "__all__"


class ItemSerializer(serializers.ModelSerializer):
    add_ons = AddOnSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Item
        fields = "__all__"
