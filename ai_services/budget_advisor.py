import pickle
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

class BudgetAdvisor:
    def __init__(self):
        self.model = None
        self.load_model()
    
    def load_model(self):
        """Load the trained gradient boosting model"""
        try:
            # If you have a budget model, load it here
            model_path = BASE_DIR / 'budget_model.pkl'
            if model_path.exists():
                with open(model_path, 'rb') as f:
                    self.model = pickle.load(f)
                print("✅ Budget model loaded")
            else:
                print("ℹ️ Using rule-based budget suggestions")
        except Exception as e:
            print(f"Budget model not found: {e}")
    
    def analyze_spending_patterns(self, transactions):
        """Analyze user spending patterns"""
        if not transactions:
            return {}
        
        patterns = {}
        for t in transactions:
            cat = t.category.name if hasattr(t, 'category') else 'Other'
            if cat not in patterns:
                patterns[cat] = {
                    'total': 0,
                    'count': 0,
                    'avg': 0
                }
            patterns[cat]['total'] += float(t.amount)
            patterns[cat]['count'] += 1
        
        for cat in patterns:
            patterns[cat]['avg'] = patterns[cat]['total'] / patterns[cat]['count']
        
        return patterns
    
    def suggest_budget(self, user, transactions=None):
        """Generate AI-powered budget suggestions"""
        if not transactions:
            from transactions.models import Transaction
            transactions = Transaction.objects.filter(user=user).order_by('-date')[:50]
        
        # Analyze spending patterns
        patterns = self.analyze_spending_patterns(transactions)
        
        # Calculate monthly income (last 30 days)
        month_ago = datetime.now() - timedelta(days=30)
        income = sum(float(t.amount) for t in transactions 
                    if hasattr(t, 'transaction_type') and t.transaction_type == 'income'
                    and t.date >= month_ago.date())
        
        # Generate budget suggestions using Gradient Boosting logic
        suggestions = {}
        
        if self.model:
            # Use ML model if available
            try:
                # Prepare features for model
                features = self.prepare_features(patterns, income)
                predictions = self.model.predict([features])[0]
                # Process predictions...
                pass
            except:
                # Fallback to rule-based
                suggestions = self.rule_based_budget(patterns, income)
        else:
            # Rule-based suggestions
            suggestions = self.rule_based_budget(patterns, income)
        
        return suggestions
    
    def rule_based_budget(self, patterns, income):
        """Simple rule-based budget suggestions"""
        budget = {
            'Food': min(patterns.get('Food', {}).get('avg', 0) * 1.1, income * 0.3),
            'Transport': min(patterns.get('Transport', {}).get('avg', 0) * 1.1, income * 0.15),
            'Shopping': min(patterns.get('Shopping', {}).get('avg', 0) * 1.1, income * 0.2),
            'Entertainment': min(patterns.get('Entertainment', {}).get('avg', 0) * 1.1, income * 0.1),
            'Bills': min(patterns.get('Bills', {}).get('avg', 0) * 1.1, income * 0.25),
            'Savings': income * 0.2,
        }
        return budget
    
    def prepare_features(self, patterns, income):
        """Prepare features for ML model"""
        features = []
        # Create feature vector based on your model's training data
        # This needs to match your model's expected input
        return features

# Global instance
budget_advisor = BudgetAdvisor()