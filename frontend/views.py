from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Avg, Q
from datetime import datetime, timedelta, date
from users.models import User
from transactions.models import Transaction, Category
from group_expenses.models import Settlement
from insights.models import BudgetInsight, SavingsGoal, AIInsight, Bill
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import redirect
from ai_services.classifier import classifier
import json
from django.core.paginator import Paginator
from calendar import month_name
from django.core.paginator import Paginator
from datetime import datetime
from django.db.models import Sum

@login_required
def dashboard_stats(request):
    user = request.user
    today = datetime.now().date()
    current_month = today.month
    current_year = today.year
    
    # Calculate total balance correctly (income - expenses)
    total_income = Transaction.objects.filter(
        user=user, 
        category_type='income'
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    total_expenses = Transaction.objects.filter(
        user=user, 
        category_type='expense'
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    total_balance = total_income - total_expenses
    
    monthly_income = Transaction.objects.filter(
        user=user, 
        date__month=current_month,
        date__year=current_year,
        category_type='income'
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    monthly_expenses = Transaction.objects.filter(
        user=user, 
        date__month=current_month,
        date__year=current_year,
        category_type='expense'
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Calculate last month for comparison
    last_month = current_month - 1 if current_month > 1 else 12
    last_month_year = current_year if current_month > 1 else current_year - 1
    
    # Last month total balance (income - expenses for last month)
    last_month_income = Transaction.objects.filter(
        user=user,
        date__month=last_month,
        date__year=last_month_year,
        category_type='income'
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    last_month_expenses = Transaction.objects.filter(
        user=user,
        date__month=last_month,
        date__year=last_month_year,
        category_type='expense'
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    last_month_balance = last_month_income - last_month_expenses
    
    balance_change = 0
    if last_month_balance:
        balance_change = round(((total_balance - last_month_balance) / last_month_balance) * 100, 2)
    
    # Income change
    last_month_income_total = Transaction.objects.filter(
        user=user,
        date__month=last_month,
        date__year=last_month_year,
        category_type='income'
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    income_change = 0
    if last_month_income_total:
        income_change = round(((monthly_income - last_month_income_total) / last_month_income_total) * 100, 2)
    
    # Expense change
    last_month_expenses_total = Transaction.objects.filter(
        user=user,
        date__month=last_month,
        date__year=last_month_year,
        category_type='expense'
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    expense_change = 0
    if last_month_expenses_total:
        expense_change = round(((monthly_expenses - last_month_expenses_total) / last_month_expenses_total) * 100, 2)
    
    # Savings goals
    monthly_savings = SavingsGoal.objects.filter(user=user).aggregate(Sum('saved_amount'))['saved_amount__sum'] or 0
    
    total_goal = SavingsGoal.objects.filter(user=user).aggregate(Sum('target_amount'))['target_amount__sum'] or 1
    savings_progress = round((monthly_savings / total_goal) * 100, 2) if total_goal else 0
    
    # Print for debugging
    print(f"Debug - User: {user.email}")
    print(f"Debug - Total Income: {total_income}")
    print(f"Debug - Total Expenses: {total_expenses}")
    print(f"Debug - Total Balance: {total_balance}")
    print(f"Debug - Monthly Income: {monthly_income}")
    print(f"Debug - Monthly Expenses: {monthly_expenses}")
    print(f"Debug - Savings: {monthly_savings}")
    
    # ===== FIXED CODE FOR AI INSIGHTS AND BILLS =====
    # Get AI Insights
    today_date = date.today()
    
    ai_insights = AIInsight.objects.filter(user=user).order_by('-created_at')[:5]
    
    # Get Upcoming Bills
    upcoming_bills_queryset = Bill.objects.filter(
        user=user, 
        is_paid=False,
        due_date__gte=today_date
    ).order_by('due_date')[:5]
    
    # Convert to list of dictionaries with days_remaining
    upcoming_bills = []
    for bill in upcoming_bills_queryset:
        # Calculate days remaining
        days_remaining = (bill.due_date - today_date).days
        # Create a dictionary with bill data plus days_remaining
        bill_data = {
            'id': bill.id,
            'name': bill.name,
            'amount': bill.amount,
            'category': bill.category,
            'due_date': bill.due_date,
            'frequency': bill.frequency,
            'is_paid': bill.is_paid,
            'description': getattr(bill, 'description', ''),
            'days_remaining': days_remaining,
        }
        upcoming_bills.append(bill_data)
    
    print(f"Debug - AI Insights count: {ai_insights.count()}")
    print(f"Debug - Bills count: {len(upcoming_bills)}")
    # ===== END FIXED CODE =====
    
    context = {
        # Financial data
        'total_balance': total_balance,
        'balance_change': balance_change,
        'monthly_income': monthly_income,
        'income_change': income_change,
        'monthly_expenses': monthly_expenses,
        'expense_change': expense_change,
        
        # Savings data
        'monthly_savings': monthly_savings,
        'savings_progress': savings_progress,
        
        # User info
        'user': user,
        
        # AI Insights and Bills
        'ai_insights': ai_insights,
        'upcoming_bills': upcoming_bills,
    }
    
    return render(request, 'frontend/dashboard.html', context)

@login_required
def financial_summary(request):
    user = request.user  

    today = datetime.today()
    current_month = today.month
    current_year = today.year
    last_month = current_month - 1 if current_month > 1 else 12
    last_month_year = current_year if current_month > 1 else current_year - 1

    total_balance = Transaction.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0

    monthly_income = Transaction.objects.filter(
        user=user, 
        date__month=current_month,
        date__year=current_year,
        category_type='income'
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    monthly_expenses = Transaction.objects.filter(
        user=user, 
        date__month=current_month,
        date__year=current_year,
        category_type='expense'
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    last_month_balance = Transaction.objects.filter(
        user=user, 
        date__month=last_month,
        date__year=last_month_year
    ).aggregate(Sum('amount'))['amount__sum'] or 1
    
    balance_change = round(((total_balance - last_month_balance) / last_month_balance) * 100, 2) if last_month_balance else 0

    last_month_income = Transaction.objects.filter(
        user=user, 
        date__month=last_month,
        date__year=last_month_year,
        category_type='income'
    ).aggregate(Sum('amount'))['amount__sum'] or 1
    
    income_change = round(((monthly_income - last_month_income) / last_month_income) * 100, 2) if last_month_income else 0

    last_month_expenses = Transaction.objects.filter(
        user=user, 
        date__month=last_month,
        date__year=last_month_year,
        category_type='expense'
    ).aggregate(Sum('amount'))['amount__sum'] or 1
    
    expense_change = round(((monthly_expenses - last_month_expenses) / last_month_expenses) * 100, 2) if last_month_expenses else 0

    total_goal = SavingsGoal.objects.filter(user=user).aggregate(Sum('target_amount'))['target_amount__sum'] or 1
    total_savings = SavingsGoal.objects.filter(user=user).aggregate(Sum('saved_amount'))['saved_amount__sum'] or 0
    savings_progress = round((total_savings / total_goal) * 100, 2) if total_goal else 0

    context = {
        'total_balance': total_balance,
        'balance_change': balance_change,
        'monthly_income': monthly_income,
        'income_change': income_change,
        'monthly_expenses': monthly_expenses,
        'expense_change': expense_change,
        'savings_progress': savings_progress,
    }

    return render(request, 'dashboard.html', context) 

def spending_analysis(request):
    user_id = request.user.id if request.user.is_authenticated else None
    if not user_id:
        return {
            'dates': [],
            'income': [],
            'expenses': [],
            'expense_categories': [],
            'months': [],
            'monthly_expenses': []
        }
    
    period = request.GET.get('period', 'month')

    # Determine date range
    today = datetime.today().date()
    if period == 'week':
        start_date = today - timedelta(days=today.weekday())
    elif period == 'year':
        start_date = today.replace(month=1, day=1)
    else:  # Default to month
        start_date = today.replace(day=1)

    transactions = Transaction.objects.filter(user_id=user_id, date__gte=start_date)

    # Group by date
    datewise_income = transactions.filter(category_type="income").values('date').annotate(total=Sum('amount'))
    datewise_expense = transactions.filter(category_type="expense").values('date').annotate(total=Sum('amount'))

    # Prepare chart data
    dates = [entry['date'].strftime('%Y-%m-%d') for entry in datewise_income] if datewise_income else []
    income = [float(entry['total']) for entry in datewise_income] if datewise_income else []
    expenses = [float(entry['total']) for entry in datewise_expense] if datewise_expense else []

    # Expense category breakdown
    expense_categories = transactions.filter(category_type="expense").values('category_id').annotate(total=Sum('amount'))
    category_data = []
    for entry in expense_categories:
        try:
            category_name = Category.objects.get(id=entry["category_id"]).name
            category_data.append({"category": category_name, "amount": float(entry["total"])})
        except:
            pass

    # Monthly expense trend
    from django.db.models.functions import ExtractMonth
    monthly_expenses_qs = transactions.filter(category_type="expense").annotate(
        month=ExtractMonth('date')
    ).values('month').annotate(total=Sum('amount')).order_by('month')
    
    months = [f"Month {entry['month']}" for entry in monthly_expenses_qs]
    monthly_totals = [float(entry['total']) for entry in monthly_expenses_qs]

    result = {
        "dates": dates,
        "income": income,
        "expenses": expenses,
        "expense_categories": category_data,
        "months": months,
        "monthly_expenses": monthly_totals,
    }
    
    # If this is called as a view function (not from dashboard_stats)
    if request.path.startswith('/spending-analysis/'):
        return JsonResponse(result)
    
    return result


# Simple page views
def homepage(request):
    return render(request, 'frontend/homepage.html')

def signup_view(request):
    return render(request, 'frontend/signup.html')

def budget_view(request):
    user = request.user
    from datetime import datetime
    from django.db.models import Sum, Q
    from transactions.models import Transaction, Category
    from insights.models import AIInsight, Budget
    from calendar import month_name
    
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    # Calculate total income for the month
    total_income = Transaction.objects.filter(
        user=user,
        date__month=current_month,
        date__year=current_year,
        category_type='income'
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Calculate income by category
    income_by_category = Transaction.objects.filter(
        user=user,
        date__month=current_month,
        date__year=current_year,
        category_type='income'
    ).values('category__name').annotate(
        total=Sum('amount')
    ).order_by('-total')
    
    # Calculate income percentages
    income_with_percentages = []
    for item in income_by_category:
        percentage = (item['total'] / total_income * 100) if total_income > 0 else 0
        income_with_percentages.append({
            'name': item['category__name'] or 'Other',
            'amount': item['total'],
            'percentage': round(percentage)
        })
    
    # Get all budgets for current month/year
    budgets = Budget.objects.filter(
        user=user,
        period='monthly',
        month=current_month,
        year=current_year
    ).order_by('category')
    
    # Calculate budget totals
    total_budget = sum(budget.amount for budget in budgets)
    total_spent = sum(budget.spent_amount for budget in budgets)
    remaining_budget = total_budget - total_spent
    
    # Calculate budget health
    if total_budget > 0:
        budget_health_percentage = (total_spent / total_budget) * 100
        if budget_health_percentage < 40:
            budget_health = "Excellent"
            budget_health_color = "green"
        elif budget_health_percentage < 70:
            budget_health = "Good"
            budget_health_color = "blue"
        elif budget_health_percentage < 90:
            budget_health = "Fair"
            budget_health_color = "yellow"
        else:
            budget_health = "Critical"
            budget_health_color = "red"
    else:
        budget_health = "No Budget Set"
        budget_health_color = "gray"
    
    # Get warnings for categories exceeding budget
    budget_warnings = []
    for budget in budgets:
        if budget.percentage_used > 100:
            budget_warnings.append({
                'category': budget.category,
                'percentage': round(budget.percentage_used)
            })
    
    # Get AI insights
    ai_insights = AIInsight.objects.filter(user=user).order_by('-created_at')[:2]
    
    # Get recent transactions
    recent_transactions = Transaction.objects.filter(
        user=user
    ).order_by('-date')[:4]
    
    context = {
        'total_income': total_income,
        'income_by_category': income_with_percentages,
        'budgets': budgets,
        'total_budget': total_budget,
        'total_spent': total_spent,
        'remaining_budget': remaining_budget,
        'budget_health': budget_health,
        'budget_health_color': budget_health_color,
        'budget_health_percentage': round(budget_health_percentage) if total_budget > 0 else 0,
        'budget_warnings': budget_warnings,
        'ai_insights': ai_insights,
        'recent_transactions': recent_transactions,
        'current_month_name': month_name[current_month],
        'current_year': current_year,
        'user': user,
    }
    return render(request, 'frontend/budget.html', context)

def goals_view(request):
    return render(request, 'frontend/goals.html')
def transactions_view(request):
    user = request.user
    
    
    # Get all transactions for the user
    all_transactions = Transaction.objects.filter(user=user).order_by('-date')
    
    # Apply filters if any
    date_filter = request.GET.get('date')
    category_filter = request.GET.get('category')
    min_amount = request.GET.get('min_amount')
    search_text = request.GET.get('search')
    
    if date_filter:
        all_transactions = all_transactions.filter(date=date_filter)
    if category_filter:
        all_transactions = all_transactions.filter(category__name=category_filter)
    if min_amount:
        all_transactions = all_transactions.filter(amount__gte=min_amount)
    if search_text:
        all_transactions = all_transactions.filter(description__icontains=search_text)
    
    # Pagination - 10 transactions per page
    paginator = Paginator(all_transactions, 10)
    page_number = request.GET.get('page', 1)
    transactions_page = paginator.get_page(page_number)
    
    # Calculate totals
    total_balance = Transaction.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0
    
    monthly_income = Transaction.objects.filter(
        user=user, 
        date__month=datetime.now().month,
        date__year=datetime.now().year,
        category_type='income'
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    monthly_expenses = Transaction.objects.filter(
        user=user, 
        date__month=datetime.now().month,
        date__year=datetime.now().year,
        category_type='expense'
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    # Get categories for filter dropdown
    categories = Category.objects.filter(user=user).values_list('name', flat=True).distinct()
    
    context = {
        'transactions': transactions_page,
        'total_balance': total_balance,
        'monthly_income': monthly_income,
        'monthly_expenses': monthly_expenses,
        'categories': categories,
        'user': user,
    }
    return render(request, 'frontend/transaction.html', context)

def group_expenses_view(request):
    return render(request, 'frontend/group_expenses.html')