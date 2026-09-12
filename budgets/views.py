from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum

from .models import Budget
from transactions.models import Transaction, Category


@login_required
def budget_list(request):

    budgets = Budget.objects.filter(
        user=request.user
    ).select_related('category')

    budget_data = []

    for budget in budgets:

        if budget.category:

            spent = Transaction.objects.filter(
                user=request.user,
                category=budget.category,
                transaction_type='expense',
                date__month=budget.month,
                date__year=budget.year
            ).aggregate(
                total=Sum('amount')
            )['total'] or 0

        else:

            spent = Transaction.objects.filter(
                user=request.user,
                transaction_type='expense',
                date__month=budget.month,
                date__year=budget.year
            ).aggregate(
                total=Sum('amount')
            )['total'] or 0

        remaining = budget.amount - spent

        # Calculate percentage used
        if budget.amount > 0:
            percentage = round(
                (float(spent) / float(budget.amount)) * 100
            )
        else:
            percentage = 0

        # Determine budget status
        if percentage >= 100:

            status = 'over'

        elif percentage >= 80:

            status = 'warning'

        else:

            status = 'safe'

        budget_data.append({
            'budget': budget,
            'spent': spent,
            'remaining': remaining,
            'percentage': percentage,
            'status': status,
        })

    return render(
        request,
        'budgets/budgets.html',
        {
            'budget_data': budget_data
        }
    )


@login_required
def add_budget(request):

    categories = Category.objects.filter(
        user=request.user
    )

    if request.method == 'POST':

        amount = request.POST.get('amount')
        category_id = request.POST.get('category')
        month = request.POST.get('month')
        year = request.POST.get('year')

        if category_id:

            category = get_object_or_404(
                Category,
                id=category_id,
                user=request.user
            )

        else:

            category = None

        Budget.objects.create(
            user=request.user,
            category=category,
            amount=amount,
            month=month,
            year=year
        )

        messages.success(
            request,
            'Budget added successfully!'
        )

        return redirect('budgets')

    return render(
        request,
        'budgets/add_budget.html',
        {
            'categories': categories
        }
    )