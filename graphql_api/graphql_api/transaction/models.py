import uuid
from django.db import models


class TransactionCategory(models.TextChoices):
    MARKETING = ("MARKETING", "MARKETING")
    ENGINEERING = ("ENGINEERING", "ENGINEERING")
    GROWTH = ("GROWTH", "GROWTH")
    PRODUCT = ("PRODUCT", "PRODUCT")


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.FloatField(null=False, blank=False, default=0)
    category = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        choices=TransactionCategory.choices,
    )
    created_at = models.DateTimeField(null=True, blank=True, default=None)
