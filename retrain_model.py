import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import GradientBoostingClassifier
import os

print("="*50)
print("RETRAINING AI MODEL")
print("="*50)

# Check if CSV exists
if not os.path.exists('transactions_dataset.csv'):
    print("❌ CSV file not found!")
    exit()

# Load dataset
print("\n📂 Loading dataset...")
df = pd.read_csv('transactions_dataset.csv')
print(f"✅ Loaded {len(df)} transactions")
print(f"📋 Columns: {list(df.columns)}")

# Use the columns from your CSV
X = df['Description'].fillna('')  # Text descriptions
y = df['Category']  # Categories

print(f"\n🎯 Categories found: {y.unique()}")
print(f"📊 Number of categories: {len(y.unique())}")

# Convert text to numbers
print("\n🔄 Vectorizing text...")
vectorizer = TfidfVectorizer(max_features=500)
X_vec = vectorizer.fit_transform(X)
print(f"✅ Vectorized to {X_vec.shape[1]} features")

# Train the model
print("\n🧠 Training Gradient Boosting model...")
model = GradientBoostingClassifier(n_estimators=100, random_state=42)
model.fit(X_vec, y)
print("✅ Model trained successfully!")

# Save the new models
print("\n💾 Saving new models...")
with open('transaction_classifier_new.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('transaction_vectorizer_new.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)

print("✅ New models saved!")
print("   - transaction_classifier_new.pkl")
print("   - transaction_vectorizer_new.pkl")

# Test the model
print("\n🔍 Testing with examples:")
test_texts = [
    "pizza hut delivery",
    "uber ride to airport", 
    "amazon headphones",
    "movie tickets",
    "salary deposit",
    "groceries at walmart",
    "electricity bill"
]

for text in test_texts:
    vec = vectorizer.transform([text])
    pred = model.predict(vec)[0]
    # Get confidence score
    proba = model.predict_proba(vec)[0].max()
    print(f"   '{text}' → {pred} (confidence: {proba:.2f})")

print("\n" + "="*50)
print("🎉 DONE! AI Model is ready!")
print("="*50)