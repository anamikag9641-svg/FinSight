from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Avg, Max

from transactions.models import Transaction


@login_required
def analytics_dashboard(request):

    # -----------------------------------------
    # ALL EXPENSE TRANSACTIONS
    # -----------------------------------------

    transactions = Transaction.objects.filter(
        user=request.user,
        transaction_type='expense'
    )

    # -----------------------------------------
    # TOTAL SPENDING
    # -----------------------------------------

    total_spending = transactions.aggregate(
        total=Sum('amount')
    )['total'] or 0

    # -----------------------------------------
    # AVERAGE EXPENSE
    # -----------------------------------------

    average_expense = transactions.aggregate(
        average=Avg('amount')
    )['average'] or 0

    # -----------------------------------------
    # HIGHEST EXPENSE
    # -----------------------------------------

    highest_expense = transactions.aggregate(
        highest=Max('amount')
    )['highest'] or 0

    # -----------------------------------------
    # NUMBER OF EXPENSES
    # -----------------------------------------

    expense_count = transactions.count()

    # -----------------------------------------
    # CATEGORY-WISE SPENDING
    # -----------------------------------------

    category_query = transactions.values(
        'category__name'
    ).annotate(
        total=Sum('amount')
    ).order_by('-total')

    # Convert QuerySet into normal Python list
    # so it can be converted into JSON.

    category_data = []

    for item in category_query:

        category_data.append({
            'category__name': item['category__name'],
            'total': float(item['total'])
        })

    # -----------------------------------------
    # CONTEXT
    # -----------------------------------------

    context = {

        'total_spending': total_spending,

        'average_expense': average_expense,

        'highest_expense': highest_expense,

        'expense_count': expense_count,

        'category_data': category_data,

    }

    return render(
        request,
        'analytics/analytics.html',
        context
    )