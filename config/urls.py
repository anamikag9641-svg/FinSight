from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.utils import timezone

from transactions.models import Transaction
from budgets.models import Budget


def home(request):
    return redirect('login')


@login_required
def dashboard(request):

    # -----------------------------------------
    # TRANSACTIONS
    # -----------------------------------------

    transactions = Transaction.objects.filter(
        user=request.user
    )

    # Recent 5 transactions
    recent_transactions = transactions.order_by(
        '-date',
        '-created_at'
    )[:5]

    # -----------------------------------------
    # TOTAL INCOME
    # -----------------------------------------

    total_income = transactions.filter(
        transaction_type='income'
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    # -----------------------------------------
    # TOTAL EXPENSES
    # -----------------------------------------

    total_expenses = transactions.filter(
        transaction_type='expense'
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    # -----------------------------------------
    # CURRENT BALANCE
    # -----------------------------------------

    current_balance = total_income - total_expenses

    # -----------------------------------------
    # CURRENT MONTH
    # -----------------------------------------

    today = timezone.now().date()

    monthly_expenses = transactions.filter(
        transaction_type='expense',
        date__year=today.year,
        date__month=today.month
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    # -----------------------------------------
    # CATEGORY-WISE EXPENSES
    # -----------------------------------------

    category_expenses_query = transactions.filter(
        transaction_type='expense'
    ).values(
        'category__name'
    ).annotate(
        total=Sum('amount')
    ).order_by('-total')

    category_expenses = []

    for item in category_expenses_query:

        category_expenses.append({
            'category__name': item['category__name'],
            'total': float(item['total'])
        })

    # -----------------------------------------
    # MONTHLY EXPENSES
    # -----------------------------------------

    monthly_expenses_query = transactions.filter(
        transaction_type='expense'
    ).annotate(
        month=TruncMonth('date')
    ).values(
        'month'
    ).annotate(
        total=Sum('amount')
    ).order_by('month')

    monthly_expenses_data = []

    for item in monthly_expenses_query:

        monthly_expenses_data.append({
            'month': item['month'].strftime('%b %Y'),
            'total': float(item['total'])
        })

    # -----------------------------------------
    # BUDGET ANALYTICS
    # -----------------------------------------

    budgets = Budget.objects.filter(
        user=request.user
    ).select_related('category')

    total_budget = 0
    total_budget_spent = 0

    budget_overview = []

    for budget in budgets:

        total_budget += budget.amount

        if budget.category:

            spent = transactions.filter(
                transaction_type='expense',
                category=budget.category,
                date__month=budget.month,
                date__year=budget.year
            ).aggregate(
                total=Sum('amount')
            )['total'] or 0

        else:

            spent = transactions.filter(
                transaction_type='expense',
                date__month=budget.month,
                date__year=budget.year
            ).aggregate(
                total=Sum('amount')
            )['total'] or 0

        total_budget_spent += spent

        budget_overview.append({
            'category': (
                budget.category.name
                if budget.category
                else 'Overall Budget'
            ),
            'budget': float(budget.amount),
            'spent': float(spent),
        })

    # -----------------------------------------
    # REMAINING BUDGET
    # -----------------------------------------

    total_budget_remaining = (
        total_budget - total_budget_spent
    )

    # -----------------------------------------
    # CONTEXT
    # -----------------------------------------

    context = {

        'total_income': total_income,

        'total_expenses': total_expenses,

        'current_balance': current_balance,

        'monthly_expenses': monthly_expenses,

        'category_expenses': category_expenses,

        'monthly_expenses_data': monthly_expenses_data,

        'total_budget': total_budget,

        'total_budget_spent': total_budget_spent,

        'total_budget_remaining': total_budget_remaining,

        'budget_overview': budget_overview,

        'recent_transactions': recent_transactions,

    }

    return render(
        request,
        'dashboard.html',
        context
    )


# =========================================
# URL PATTERNS
# =========================================

urlpatterns = [

    path(
        'admin/',
        admin.site.urls
    ),

    path(
        '',
        home,
        name='home'
    ),

    path(
        'accounts/',
        include('accounts.urls')
    ),

    path(
        'dashboard/',
        dashboard,
        name='dashboard'
    ),

    path(
        'transactions/',
        include('transactions.urls')
    ),

    path(
        'budgets/',
        include('budgets.urls')
    ),

    # NEW: ANALYTICS
    path(
        'analytics/',
        include('analytics.urls')
    ),

]