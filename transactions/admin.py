from django.contrib import admin
from .models import Category, Transaction


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'amount',
        'transaction_type',
        'category',
        'date',
    )

    list_filter = (
        'transaction_type',
        'category',
        'date',
    )

    search_fields = (
        'description',
        'category__name',
    )