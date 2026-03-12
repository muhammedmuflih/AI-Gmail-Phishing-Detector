"""
Train Multiple Models for Different Categories
Run this script once to train all models
"""

import pandas as pd
import numpy as np
import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import warnings
warnings.filterwarnings('ignore')

print("="*60)
print("🤖 TRAINING ALL PHISHING DETECTION MODELS")
print("="*60)

# Create models directory
os.makedirs('models', exist_ok=True)

# ============================================
# 1. Load Enhanced Dataset
# ============================================
print("\n📂 Loading enhanced dataset...")
df = pd.read_csv("Phishing_Email.csv")

# Clean text
def clean_text(text):
    if pd.isna(text):
        return ""
    text = str(text).lower()
    text = ' '.join(text.split())
    return text

df['clean_text'] = df['Email Text'].apply(clean_text)

# Create label
df['label'] = df['Email Type'].map({
    'Safe Email': 0,
    'Phishing Email': 1
})

print(f"   Total emails: {len(df)}")
print(f"   Phishing: {len(df[df['label']==1])}")
print(f"   Safe: {len(df[df['label']==0])}")

# ============================================
# 2. Create Category-Specific Datasets
# ============================================

# Job scam emails (if category column exists)
if 'Category' in df.columns:
    df_job = df[df['Category'].str.contains('Job', na=False)]
    df_shopping = df[df['Category'].str.contains('Shopping', na=False)]
    df_general = df[~df['Category'].str.contains('Job|Shopping', na=False)]
else:
    # If no category, use keywords to identify
    job_keywords = ['job', 'work from home', 'interview', 'salary', 'recruitment', 'career']
    shopping_keywords = ['shopping', 'store', 'mall', 'gift card', 'voucher', 'coupon']
    
    df_job = df[df['clean_text'].str.contains('|'.join(job_keywords), na=False)]
    df_shopping = df[df['clean_text'].str.contains('|'.join(shopping_keywords), na=False)]
    df_general = df[~df.index.isin(df_job.index) & ~df.index.isin(df_shopping.index)]

print("\n📊 Category Distribution:")
print(f"   📧 General Phishing: {len(df_general)}")
print(f"   💼 Job Scams: {len(df_job)}")
print(f"   🛍️ Shopping Scams: {len(df_shopping)}")

# ============================================
# 3. Train Common Vectorizer
# ============================================
print("\n🔄 Training common vectorizer...")

vectorizer = TfidfVectorizer(
    max_features=10000,
    stop_words='english',
    ngram_range=(1, 3),
    min_df=2,
    max_df=0.95,
    sublinear_tf=True
)

# Fit on all data
all_texts = df['clean_text'].tolist()
X_all = vectorizer.fit_transform(all_texts)

# Save vectorizer
joblib.dump(vectorizer, 'models/vectorizer.pkl')
print("   ✅ Vectorizer saved to models/vectorizer.pkl")

# ============================================
# 4. Train General Phishing Model
# ============================================
print("\n🔄 Training General Phishing Model...")

X_gen = vectorizer.transform(df_general['clean_text'].tolist())
y_gen = df_general['label'].tolist()

X_train, X_test, y_train, y_test = train_test_split(
    X_gen, y_gen, test_size=0.2, random_state=42, stratify=y_gen
)

model_general = LogisticRegression(
    max_iter=2000,
    class_weight='balanced',
    C=1.5,
    solver='saga',
    random_state=42
)

model_general.fit(X_train, y_train)

# Evaluate
y_pred = model_general.predict(X_test)
print("\n📊 General Model Performance:")
print(classification_report(y_test, y_pred))

# Save
joblib.dump(model_general, 'models/phishing_model.pkl')
print("   ✅ Saved to models/phishing_model.pkl")

# ============================================
# 5. Train Job Scam Model
# ============================================
if len(df_job) > 100:
    print("\n🔄 Training Job Scam Specific Model...")
    
    X_job = vectorizer.transform(df_job['clean_text'].tolist())
    y_job = df_job['label'].tolist()
    
    X_train, X_test, y_train, y_test = train_test_split(
        X_job, y_job, test_size=0.2, random_state=42, stratify=y_job
    )
    
    model_job = LogisticRegression(
        max_iter=2000,
        class_weight='balanced',
        C=2.0,  # Stronger for specific patterns
        solver='saga',
        random_state=42
    )
    
    model_job.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model_job.predict(X_test)
    print("\n📊 Job Model Performance:")
    print(classification_report(y_test, y_pred))
    
    # Save
    joblib.dump(model_job, 'models/job_scam_model.pkl')
    print("   ✅ Saved to models/job_scam_model.pkl")
else:
    print("\n⚠️ Not enough job scam data for separate model")

# ============================================
# 6. Train Shopping Scam Model
# ============================================
if len(df_shopping) > 100:
    print("\n🔄 Training Shopping Scam Specific Model...")
    
    X_shop = vectorizer.transform(df_shopping['clean_text'].tolist())
    y_shop = df_shopping['label'].tolist()
    
    X_train, X_test, y_train, y_test = train_test_split(
        X_shop, y_shop, test_size=0.2, random_state=42, stratify=y_shop
    )
    
    model_shop = LogisticRegression(
        max_iter=2000,
        class_weight='balanced',
        C=2.0,
        solver='saga',
        random_state=42
    )
    
    model_shop.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model_shop.predict(X_test)
    print("\n📊 Shopping Model Performance:")
    print(classification_report(y_test, y_pred))
    
    # Save
    joblib.dump(model_shop, 'models/shopping_model.pkl')
    print("   ✅ Saved to models/shopping_model.pkl")
else:
    print("\n⚠️ Not enough shopping scam data for separate model")

print("\n" + "="*60)
print("✅ ALL MODELS TRAINED SUCCESSFULLY!")
print("="*60)
print("\nModels saved in 'models/' directory:")
print("   📦 models/vectorizer.pkl")
print("   📦 models/phishing_model.pkl")
print("   📦 models/job_scam_model.pkl")
print("   📦 models/shopping_model.pkl")