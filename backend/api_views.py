from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.db.models.functions import ExtractMonth
from datetime import datetime, timedelta
from transactions.models import Transaction, Category
import json

@login_required
def category_breakdown(request):
    """API endpoint to get spending breakdown by category for pie chart"""
    try:
        user = request.user
        
        # Get expense transactions grouped by category
        transactions = Transaction.objects.filter(
            user=user, 
            category_type='expense'
        ).values('category__name').annotate(
            total=Sum('amount')
        ).order_by('-total')[:7]  # Top 7 categories
        
        labels = []
        values = []
        
        for t in transactions:
            category_name = t['category__name']
            if category_name:  # Handle null categories
                labels.append(category_name)
            else:
                labels.append('Other')
            values.append(float(t['total']))
        
        # If no transactions, return sample data
        if not labels:
            labels = ['Food', 'Transport', 'Shopping', 'Entertainment', 'Bills', 'Healthcare', 'Other']
            values = [30, 15, 20, 10, 12, 8, 5]
        
        return JsonResponse({
            'labels': labels, 
            'values': values
        })
        
    except Exception as e:
        return JsonResponse({
            'error': str(e),
            'labels': ['Food', 'Transport', 'Shopping', 'Entertainment', 'Bills', 'Healthcare', 'Other'],
            'values': [30, 15, 20, 10, 12, 8, 5]
        })

@login_required
def monthly_trend(request):
    """API endpoint to get monthly income, expenses, and savings trend"""
    try:
        user = request.user
        today = datetime.now()
        
        # Get last 6 months of data
        six_months_ago = today - timedelta(days=180)
        
        # Get monthly data
        transactions = Transaction.objects.filter(
            user=user,
            date__gte=six_months_ago
        ).annotate(
            month=ExtractMonth('date')
        ).values('month').annotate(
            income=Sum('amount', filter=Q(category_type='income')),
            expenses=Sum('amount', filter=Q(category_type='expense'))
        ).order_by('month')
        
        # Month labels (last 6 months)
        month_names = []
        for i in range(5, -1, -1):
            month_date = today - timedelta(days=30*i)
            month_names.append(month_date.strftime('%b'))
        
        # Initialize data arrays
        income_data = [0] * 6
        expense_data = [0] * 6
        
        # Fill in actual data
        for t in transactions:
            month_idx = t['month'] % 6
            if 0 <= month_idx < 6:
                income_data[month_idx] = float(t['income'] or 0)
                expense_data[month_idx] = float(t['expenses'] or 0)
        
        # Calculate savings (income - expenses)
        savings_data = [income_data[i] - expense_data[i] for i in range(6)]
        
        return JsonResponse({
            'labels': month_names,
            'income': income_data,
            'expenses': expense_data,
            'savings': savings_data
        })
        
    except Exception as e:
        # Return sample data if error
        return JsonResponse({
            'error': str(e),
            'labels': ['Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr'],
            'income': [44000, 45000, 46000, 44000, 50000, 48000],
            'expenses': [24000, 25000, 26000, 24000, 28000, 27000],
            'savings': [20000, 20000, 20000, 20000, 22000, 21000]
        })

@login_required
def delete_transaction(request, id):
    """API endpoint to delete a transaction"""
    if request.method == 'POST':
        try:
            transaction = Transaction.objects.get(id=id, user=request.user)
            transaction.delete()
            return JsonResponse({'message': 'Transaction deleted successfully'})
        except Transaction.DoesNotExist:
            return JsonResponse({'error': 'Transaction not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Method not allowed'}, status=405)