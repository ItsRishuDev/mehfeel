from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class AddOn(models.Model):
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.name
