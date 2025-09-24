from django.db import models
from django.contrib.auth.hashers import make_password

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

class Collection(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

class ProductSize(models.Model):
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

class ProductDetail(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
