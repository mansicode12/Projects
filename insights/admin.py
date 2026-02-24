from django.contrib import admin
from .models import BudgetInsight, SavingsGoal, AIInsight, Bill, Budget

@admin.register(BudgetInsight)
class BudgetInsightAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'average_spending', 'forecasted_spending', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('user__username', 'category')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Budget Data', {
            'fields': ('category', 'average_spending', 'forecasted_spending')
        }),
        ('Recommendations', {
            'fields': ('savings_recommendation',)
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )
    readonly_fields = ('created_at',)

@admin.register(SavingsGoal)
class SavingsGoalAdmin(admin.ModelAdmin):
    list_display = ('user', 'goal_name', 'target_amount', 'saved_amount', 'deadline', 'status')
    list_filter = ('status', 'deadline')
    search_fields = ('user__username', 'goal_name')
    date_hierarchy = 'deadline'
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Goal Details', {
            'fields': ('goal_name', 'target_amount', 'saved_amount', 'deadline')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )
    readonly_fields = ('created_at',)
    
    actions = ['mark_as_completed']
    
    def mark_as_completed(self, request, queryset):
        queryset.update(status='Completed')
    mark_as_completed.short_description = "Mark selected goals as completed"

@admin.register(AIInsight)
class AIInsightAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'category', 'amount', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('user__username', 'title', 'message')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Insight Details', {
            'fields': ('title', 'message', 'category', 'amount')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )
    readonly_fields = ('created_at',)

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'amount', 'category', 'due_date', 'frequency', 'is_paid', 'days_remaining_display')
    list_filter = ('category', 'frequency', 'is_paid', 'due_date')
    search_fields = ('user__username', 'name', 'description')
    date_hierarchy = 'due_date'
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Bill Details', {
            'fields': ('name', 'amount', 'category', 'description')
        }),
        ('Payment Schedule', {
            'fields': ('due_date', 'frequency', 'is_paid')
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )
    readonly_fields = ('created_at',)
    
    def days_remaining_display(self, obj):
        days = obj.days_remaining
        if days < 0:
            return f"Overdue by {abs(days)} days"
        elif days == 0:
            return "Due today"
        else:
            return f"{days} days left"
    days_remaining_display.short_description = 'Days Remaining'
    
    actions = ['mark_as_paid', 'mark_as_unpaid']
    
    def mark_as_paid(self, request, queryset):
        queryset.update(is_paid=True)
    mark_as_paid.short_description = "Mark selected bills as paid"
    
    def mark_as_unpaid(self, request, queryset):
        queryset.update(is_paid=False)
    mark_as_unpaid.short_description = "Mark selected bills as unpaid"

# ===== ADD BUDGET ADMIN =====
@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'amount', 'period', 'month', 'year', 'spent_amount', 'percentage_used', 'remaining')
    list_filter = ('period', 'month', 'year', 'category')
    search_fields = ('user__username', 'category')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Budget Details', {
            'fields': ('category', 'amount', 'period', 'month', 'year')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    readonly_fields = ('created_at', 'updated_at', 'spent_amount', 'percentage_used', 'remaining')
    
    def spent_amount(self, obj):
        return f"₹{obj.spent_amount}"
    spent_amount.short_description = 'Spent'
    
    def percentage_used(self, obj):
        return f"{obj.percentage_used:.1f}%"
    percentage_used.short_description = '% Used'
    
    def remaining(self, obj):
        remaining = obj.remaining
        if remaining >= 0:
            return f"₹{remaining}"
        else:
            return f"-₹{abs(remaining)}"
    remaining.short_description = 'Remaining'