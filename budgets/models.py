from django.db import models
from django.contrib.auth.models import User
from transactions.models import Category


class Budget(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    month = models.PositiveIntegerField()

    year = models.PositiveIntegerField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        if self.category:
            return f"{self.category.name} - ₹{self.amount}"
        return f"Overall Budget - ₹{self.amount}"