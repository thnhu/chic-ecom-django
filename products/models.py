from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

class Collection(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, null=True)

class ProductVariant(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    EXTRA_SMALL = 1
    SMALL = 2
    MEDIUM = 3
    LARGE = 4
    EXTRA_LARGE = 5
    SIZE_CHOICES = (
        (EXTRA_SMALL, 'XS'),
        (SMALL, 'S'),
        (MEDIUM, 'M'),
        (LARGE, 'L'),
        (EXTRA_LARGE, 'XL'),
    )
    size = models.IntegerField(choices=SIZE_CHOICES, default=SMALL)
    quantity = models.IntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
