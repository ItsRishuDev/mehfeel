from rest_framework import serializers
from inventory.models import Category, Item, AddOn


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        depth = 1


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"


class AddOnSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddOn
        fields = "__all__"
