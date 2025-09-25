from dataclasses import dataclass

from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class Category(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    def __str__(self):
        return f"{self.name} - {self.description}"

class Collection(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    def __str__(self):
        return f"{self.name} - {self.description}"

class Product(BaseModel):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_quantity = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return (f"{self.name} - {self.base_price} - {self.total_quantity} - {self.is_active}\n"
                f"{self.category.name} - {self.collection.name} - {self.description}")

class ProductColor(BaseModel):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=20, unique=True)
    description = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.name} - {self.code} - {self.description}"

class ProductSize(BaseModel):
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
    def __str__(self):
        return f"{self.size}"

class ProductStatus(BaseModel):
    IN_STOCK = 1
    ON_ORDER = 2
    UNAVAILABLE = 3
    HIDDEN = 4
    STATUS_CHOICES = (
        (IN_STOCK, 'In stock'),
        (ON_ORDER, 'On order'),
        (UNAVAILABLE, 'Unavailable'),
        (HIDDEN, 'Hidden'),
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=IN_STOCK)
    def __str__(self):
        return f"{self.status}"

class ProductVariant(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(ProductColor, on_delete=models.CASCADE)
    size = models.ForeignKey(ProductSize, on_delete=models.CASCADE)
    status = models.ForeignKey(ProductStatus, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0.0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sku =models.CharField(max_length=50, unique=True)
    def __str__(self):
        return (f"{self.product.name} - {self.sku} - {self.color.description}\n"
                f"{self.color.name} - {self.size} - {self.quantity} - {self.price} - {self.status}\n")
    class Meta:
        unique_together = ('product', 'color', 'size')

class Image(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    image = models.ImageField()
    alt_text = models.CharField(max_length=100)
    is_primary = models.BooleanField(default=False)
    class Meta:
        unique_together = ('variant', 'image')