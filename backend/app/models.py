from django.db import models
from django.contrib.auth.hashers import make_password

# Abstract base class for common fields and behavior
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
