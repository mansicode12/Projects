import pickle
import pandas as pd
import os
from pathlib import Path

# Get the base directory
BASE_DIR = Path(__file__).resolve().parent.parent

class TransactionClassifier:
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.categories = {}
        self.category_list = []  # Add this to store categories in order
        self.load_models()
        self.load_category_mapping()
    
    def load_models(self):
        """Load the trained ML models"""
        try:
            # Use the NEW model files
            model_path = BASE_DIR / 'transaction_classifier_new.pkl'
            vectorizer_path = BASE_DIR / 'transaction_vectorizer_new.pkl'
            
            if model_path.exists() and vectorizer_path.exists():
                with open(model_path, 'rb') as f:
                    self.model = pickle.load(f)
                with open(vectorizer_path, 'rb') as f:
                    self.vectorizer = pickle.load(f)
                print("✅ AI Models loaded successfully!")
                
                # Get category list from model if available
                if hasattr(self.model, 'classes_'):
                    self.category_list = list(self.model.classes_)
                    self.categories = {i: cat for i, cat in enumerate(self.model.classes_)}
                    print(f"📋 Model categories: {self.category_list}")
                return True
            else:
                print("❌ Model files not found")
                return False
        except Exception as e:
            print(f"❌ Error loading models: {e}")
            return False
    
    def load_category_mapping(self):
        """Load category mapping from dataset"""
        try:
            csv_path = BASE_DIR / 'transactions_dataset.csv'
            if csv_path.exists():
                df = pd.read_csv(csv_path)
                if 'Category' in df.columns:
                    unique_cats = df['Category'].unique()
                    # Only set categories if model didn't provide them
                    if not self.categories:
                        self.categories = {i: cat for i, cat in enumerate(unique_cats)}
                        self.category_list = list(unique_cats)
                    print(f"✅ Loaded {len(unique_cats)} categories from CSV")
                    print(f"📋 Categories: {sorted(unique_cats)}")
        except Exception as e:
            print(f"Error loading categories: {e}")
    
    def predict_category(self, description):
        """Predict category for a transaction"""
        if not self.model or not self.vectorizer:
            return "Other"
        
        try:
            # Vectorize the description
            features = self.vectorizer.transform([description])
            
            # Predict - get the category directly
            prediction = self.model.predict(features)[0]
            
            # If prediction is already a string, return it directly
            if isinstance(prediction, str):
                return prediction
            
            # If it's a number, use the model's classes_
            if hasattr(self.model, 'classes_'):
                return self.model.classes_[prediction]
            
            # Fallback to categories dict
            return self.categories.get(int(prediction), "Other")
            
        except Exception as e:
            print(f"Prediction error for '{description}': {e}")
            return "Other"
    
    def predict_batch(self, descriptions):
        """Predict categories for multiple transactions"""
        results = []
        for desc in descriptions:
            results.append(self.predict_category(desc))
        return results

# Create a global instance
classifier = TransactionClassifier()

# Optional: Quick test if run directly
if __name__ == "__main__":
    test_texts = ["pizza hut", "uber ride", "amazon", "movie tickets", "salary"]
    print("\n🔍 Testing predictions:")
    for text in test_texts:
        result = classifier.predict_category(text)
        print(f"   '{text}' → {result}")