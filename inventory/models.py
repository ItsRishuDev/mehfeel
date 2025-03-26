from django.db import models

# Create your models here.

class Category(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
class Item(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
class AddOn(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.name
