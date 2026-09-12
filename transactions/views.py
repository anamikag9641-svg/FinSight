from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Transaction, Category


@login_required
def transaction_list(request):

    transactions = Transaction.objects.filter(
        user=request.user
    ).order_by('-date', '-created_at')

    return render(
        request,
        'transactions/transactions.html',
        {
            'transactions': transactions
        }
    )


@login_required
def add_transaction(request):

    categories = Category.objects.filter(
        user=request.user
    )

    if request.method == 'POST':

        amount = request.POST.get('amount')
        transaction_type = request.POST.get('transaction_type')
        category_id = request.POST.get('category')
        description = request.POST.get('description')
        date = request.POST.get('date')

        category = get_object_or_404(
            Category,
            id=category_id,
            user=request.user
        )

        Transaction.objects.create(
            user=request.user,
            amount=amount,
            transaction_type=transaction_type,
            category=category,
            description=description,
            date=date
        )

        messages.success(
            request,
            'Transaction added successfully!'
        )

        return redirect('transactions')

    return render(
        request,
        'transactions/add_transaction.html',
        {
            'categories': categories
        }
    )


@login_required
def delete_transaction(request, id):

    transaction = get_object_or_404(
        Transaction,
        id=id,
        user=request.user
    )

    transaction.delete()

    messages.success(
        request,
        'Transaction deleted successfully.'
    )

    return redirect('transactions')