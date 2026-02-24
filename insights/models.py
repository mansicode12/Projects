
from django.db import models
from django.conf import settings
from datetime import datetime

class BudgetInsight(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.CharField(max_length=100, default="General")
    average_spending = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    forecasted_spending = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    savings_recommendation = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.user.username} - {self.category} Insights"

class SavingsGoal(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    goal_name = models.CharField(max_length=255)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    saved_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    deadline = models.DateField()
    status = models.CharField(max_length=20, choices=[("In Progress", "In Progress"), ("Completed", "Completed")], default="In Progress")
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.user.username} - {self.goal_name}"

    def update_progress(self):
        """Updates the status based on savings progress."""
        if self.saved_amount >= self.target_amount:
            self.status = "Completed"
            self.save()

class AIInsight(models.Model):
    """AI-generated insights about user spending"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    message = models.TextField()
    category = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(default=datetime.now)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"

class Bill(models.Model):
    """Upcoming bills and recurring payments"""
    FREQUENCY_CHOICES = [
        ('one-time', 'One Time'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    due_date = models.DateField()
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='monthly')
    is_paid = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now)
    
    class Meta:
        ordering = ['due_date']
    
    def __str__(self):
        return f"{self.user.username} - {self.name} (₹{self.amount})"
    
    @property
    def days_remaining(self):
        """Calculate days until due date"""
        from datetime import date
        if self.due_date:
            return (self.due_date - date.today()).days
        return 0

# ===== ADD BUDGET MODEL HERE (FIXED WITH related_name) =====
class Budget(models.Model):
    """Budget allocation for categories"""
    PERIOD_CHOICES = [
        ('monthly', 'Monthly'),
        ('weekly', 'Weekly'),
        ('yearly', 'Yearly'),
    ]
    
    # FIXED: Added related_name to avoid conflict with transactions app
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='insight_budgets')
    category = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    period = models.CharField(max_length=20, choices=PERIOD_CHOICES, default='monthly')
    month = models.IntegerField(default=datetime.now().month)
    year = models.IntegerField(default=datetime.now().year)
    created_at = models.DateTimeField(default=datetime.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'category', 'month', 'year']
        ordering = ['category']
    
    def __str__(self):
        return f"{self.user.username} - {self.category}: ₹{self.amount} ({self.get_period_display()})"
    
    @property
    def spent_amount(self):
        """Calculate how much has been spent in this category for the period"""
        from transactions.models import Transaction
        from django.db.models import Sum
        
        if self.period == 'monthly':
            return Transaction.objects.filter(
                user=self.user,
                category__name=self.category,
                category_type='expense',
                date__month=self.month,
                date__year=self.year
            ).aggregate(Sum('amount'))['amount__sum'] or 0
        elif self.period == 'weekly':
            from datetime import timedelta
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=7)
            return Transaction.objects.filter(
                user=self.user,
                category__name=self.category,
                category_type='expense',
                date__range=[start_date, end_date]
            ).aggregate(Sum('amount'))['amount__sum'] or 0
        else:  # yearly
            return Transaction.objects.filter(
                user=self.user,
                category__name=self.category,
                category_type='expense',
                date__year=self.year
            ).aggregate(Sum('amount'))['amount__sum'] or 0
    
    @property
    def percentage_used(self):
        """Calculate percentage of budget used"""
        if self.amount > 0:
            return (self.spent_amount / self.amount) * 100
        return 0
    
    @property
    def remaining(self):
        """Calculate remaining budget"""
        return self.amount - self.spent_amount