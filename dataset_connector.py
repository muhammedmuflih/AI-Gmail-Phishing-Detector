"""
Dataset Connector for Phishing Email Detection
Connects the Phishing_Email.csv dataset with the ML model and app
"""

import pandas as pd
import numpy as np
import os
import re
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Try to import ML libraries, but don't fail if not available
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score
    from sklearn.model_selection import train_test_split
    import joblib
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    print("⚠️ Scikit-learn not available. Dataset ML features will be limited.")

class DatasetConnector:
    """Connect Phishing_Email.csv dataset with the application"""
    
    def __init__(self, dataset_path="Phishing_Email.csv", model_path="TRAIN/dataset_model.pkl"):
        self.dataset_path = dataset_path
        self.model_path = model_path
        self.dataset = None
        self.phishing_keywords = []
        self.safe_keywords = []
        self.model = None
        self.vectorizer = None
        self.is_loaded = False
        self.stats = {
            'total_emails': 0,
            'phishing_count': 0,
            'safe_count': 0,
            'phishing_percentage': 0,
            'safe_percentage': 0,
            'keywords_extracted': 0
        }
        
    def load_dataset(self):
        """Load the phishing email dataset"""
        try:
            if not os.path.exists(self.dataset_path):
                print(f"❌ Dataset file not found: {self.dataset_path}")
                return False
            
            print(f"📂 Loading dataset from {self.dataset_path}...")
            self.dataset = pd.read_csv(self.dataset_path)
            
            # Clean dataset
            self._clean_dataset()
            
            # Calculate stats
            self._calculate_stats()
            
            # Extract keywords
            self._extract_keywords()
            
            # Try to load or train model
            self._load_or_train_model()
            
            self.is_loaded = True
            print(f"✅ Dataset loaded successfully: {self.stats['total_emails']} emails")
            print(f"   Phishing: {self.stats['phishing_count']} ({self.stats['phishing_percentage']:.1f}%)")
            print(f"   Safe: {self.stats['safe_count']} ({self.stats['safe_percentage']:.1f}%)")
            print(f"   Keywords: {self.stats['keywords_extracted']}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error loading dataset: {e}")
            return False
    
    def _clean_dataset(self):
        """Clean and prepare the dataset"""
        if self.dataset is None:
            return
        
        # Drop rows with missing email text
        if 'Email Text' in self.dataset.columns:
            self.dataset = self.dataset.dropna(subset=['Email Text'])
        
        # Create label column if not exists
        if 'Email Type' in self.dataset.columns and 'label' not in self.dataset.columns:
            self.dataset['label'] = self.dataset['Email Type'].map({
                'Safe Email': 0,
                'Phishing Email': 1
            })
        
        # Fill any remaining NaN values
        self.dataset = self.dataset.fillna('')
    
    def _calculate_stats(self):
        """Calculate dataset statistics"""
        if self.dataset is None:
            return
        
        self.stats['total_emails'] = len(self.dataset)
        
        if 'Email Type' in self.dataset.columns:
            phishing_mask = self.dataset['Email Type'] == 'Phishing Email'
            safe_mask = self.dataset['Email Type'] == 'Safe Email'
            
            self.stats['phishing_count'] = phishing_mask.sum()
            self.stats['safe_count'] = safe_mask.sum()
            
            if self.stats['total_emails'] > 0:
                self.stats['phishing_percentage'] = (self.stats['phishing_count'] / self.stats['total_emails']) * 100
                self.stats['safe_percentage'] = (self.stats['safe_count'] / self.stats['total_emails']) * 100
    
    def _extract_keywords(self, top_n=100):
        """Extract important keywords from phishing emails"""
        if self.dataset is None or 'Email Text' not in self.dataset.columns:
            self.phishing_keywords = self._get_default_keywords()
            self.stats['keywords_extracted'] = len(self.phishing_keywords)
            return
        
        try:
            # Separate phishing and safe emails
            phishing_texts = []
            safe_texts = []
            
            for _, row in self.dataset.iterrows():
                text = str(row.get('Email Text', ''))
                email_type = str(row.get('Email Type', ''))
                
                if 'phishing' in email_type.lower():
                    phishing_texts.append(text)
                else:
                    safe_texts.append(text)
            
            # Extract keywords using TF-IDF if sklearn available
            if SKLEARN_AVAILABLE and len(phishing_texts) > 0:
                # Combine all phishing texts
                all_phishing = ' '.join(phishing_texts)
                
                # Use TF-IDF to find important words
                vectorizer = TfidfVectorizer(
                    max_features=200,
                    stop_words='english',
                    ngram_range=(1, 2),
                    min_df=2
                )
                
                try:
                    # Create TF-IDF matrix for phishing emails
                    tfidf_matrix = vectorizer.fit_transform(phishing_texts[:min(1000, len(phishing_texts))])
                    
                    # Get feature names and their average TF-IDF scores
                    feature_names = vectorizer.get_feature_names_out()
                    avg_tfidf = np.array(tfidf_matrix.mean(axis=0)).flatten()
                    
                    # Sort by importance
                    top_indices = avg_tfidf.argsort()[-top_n:][::-1]
                    
                    # Extract keywords
                    self.phishing_keywords = [feature_names[i] for i in top_indices if len(feature_names[i]) > 3]
                    
                except Exception as e:
                    print(f"⚠️ Error extracting keywords with TF-IDF: {e}")
                    self.phishing_keywords = self._get_default_keywords()
            else:
                # Fallback to simple frequency analysis
                self.phishing_keywords = self._get_default_keywords()
            
            # Ensure we have at least some keywords
            if len(self.phishing_keywords) < 20:
                self.phishing_keywords = self._get_default_keywords()
            
            self.stats['keywords_extracted'] = len(self.phishing_keywords)
            
        except Exception as e:
            print(f"⚠️ Error in keyword extraction: {e}")
            self.phishing_keywords = self._get_default_keywords()
    
    def _get_default_keywords(self):
        """Get default phishing keywords if dataset extraction fails"""
        return [
            'urgent', 'verify', 'account', 'suspended', 'security', 'login',
            'password', 'confirm', 'bank', 'paypal', 'amazon', 'facebook',
            'click', 'here', 'limited', 'winner', 'prize', 'lottery',
            'verify your account', 'password expired', 'unusual activity',
            'security alert', 'unauthorized login', 'click the link',
            'reset your password', 'update your information', 'google',
            'gmail', 'account recovery', 'sign in', 'credit card',
            'ssn', 'social security', 'irs', 'tax refund', 'inheritance',
            'wire transfer', 'western union', 'money gram', 'gift card',
            'itunes card', 'amazon gift', 'paypal payment', 'bank transfer',
            'fedex', 'ups', 'dhl', 'shipping', 'delivery', 'invoice',
            'statement', 'overdue', 'payment failed', 'transaction failed',
            'suspicious activity', 'limited access', 'restricted account',
            'unlock account', 'verify identity', 'confirm information',
            'update details', 'validate account', 'keep account',
            'prevent closure', 'immediate action', 'respond within',
            'failure to respond', 'will be closed', 'will be suspended'
        ]
    
    def _load_or_train_model(self):
        """Load existing model or train a new one"""
        if not SKLEARN_AVAILABLE:
            print("⚠️ Scikit-learn not available. Skipping model training.")
            return
        
        try:
            # Try to load existing model
            if os.path.exists(self.model_path):
                print(f"📦 Loading existing dataset model from {self.model_path}...")
                model_data = joblib.load(self.model_path)
                self.model = model_data.get('model')
                self.vectorizer = model_data.get('vectorizer')
                print("✅ Dataset model loaded successfully")
            else:
                # Train new model
                print("🔄 Training new dataset model...")
                self._train_model()
                
        except Exception as e:
            print(f"⚠️ Error loading dataset model: {e}")
            print("🔄 Will train new model on demand")
    
    def _train_model(self):
        """Train a model using the dataset"""
        if not SKLEARN_AVAILABLE or self.dataset is None:
            return False
        
        try:
            # Prepare data
            texts = self.dataset['Email Text'].astype(str).tolist()
            labels = self.dataset['label'].tolist() if 'label' in self.dataset.columns else None
            
            if labels is None:
                print("⚠️ No labels found in dataset")
                return False
            
            # Create train/test split
            X_train, X_test, y_train, y_test = train_test_split(
                texts, labels, test_size=0.2, random_state=42, stratify=labels
            )
            
            # Create vectorizer and model
            self.vectorizer = TfidfVectorizer(
                max_features=3000,
                stop_words='english',
                ngram_range=(1, 2),
                min_df=2,
                max_df=0.95
            )
            
            # Transform texts
            X_train_vec = self.vectorizer.fit_transform(X_train)
            X_test_vec = self.vectorizer.transform(X_test)
            
            # Train model
            self.model = LogisticRegression(
                max_iter=1000,
                class_weight='balanced',
                random_state=42
            )
            
            self.model.fit(X_train_vec, y_train)
            
            # Evaluate
            y_pred = self.model.predict(X_test_vec)
            accuracy = accuracy_score(y_test, y_pred)
            
            print(f"✅ Dataset model trained with accuracy: {accuracy:.3f}")
            
            # Save model
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            joblib.dump({
                'model': self.model,
                'vectorizer': self.vectorizer,
                'accuracy': accuracy,
                'timestamp': datetime.now().isoformat()
            }, self.model_path)
            
            return True
            
        except Exception as e:
            print(f"❌ Error training dataset model: {e}")
            return False
    
    def get_keywords_for_app(self):
        """Get phishing keywords for the main app"""
        return self.phishing_keywords
    
    def predict_with_dataset(self, email_text):
        """Predict if an email is phishing using the dataset-trained model"""
        result = {
            'is_phishing': False,
            'probability': 0.0,
            'confidence': 0.0,
            'dataset_trained': False,
            'keywords_matched': []
        }
        
        # Check keywords first (always available)
        if self.phishing_keywords:
            text_lower = email_text.lower()
            matched = [kw for kw in self.phishing_keywords if kw in text_lower]
            result['keywords_matched'] = matched[:10]
            
            if len(matched) > 5:
                result['is_phishing'] = True
                result['probability'] = min(0.5 + (len(matched) * 0.05), 0.95)
                result['confidence'] = result['probability']
        
        # Use ML model if available
        if SKLEARN_AVAILABLE and self.model is not None and self.vectorizer is not None:
            try:
                # Vectorize the text
                text_vec = self.vectorizer.transform([email_text])
                
                # Get prediction
                prediction = self.model.predict(text_vec)[0]
                probabilities = self.model.predict_proba(text_vec)[0]
                
                # Get probability of phishing (class 1)
                prob_phishing = probabilities[1] if len(probabilities) > 1 else 0.5
                
                result['is_phishing'] = bool(prediction)
                result['probability'] = float(prob_phishing)
                result['confidence'] = float(max(probabilities))
                result['dataset_trained'] = True
                
            except Exception as e:
                print(f"⚠️ Error in dataset prediction: {e}")
        
        return result
    
    def find_similar_emails(self, email_text, n=5):
        """Find similar emails in the dataset"""
        similar = []
        
        if self.dataset is None or 'Email Text' not in self.dataset.columns:
            return similar
        
        try:
            # Simple similarity based on common keywords
            text_lower = email_text.lower()
            words = set(re.findall(r'\b\w+\b', text_lower))
            
            # Score each email based on word overlap
            scores = []
            for idx, row in self.dataset.iterrows():
                email_text = str(row.get('Email Text', ''))
                email_words = set(re.findall(r'\b\w+\b', email_text.lower()))
                
                # Calculate Jaccard similarity
                if len(words) > 0 and len(email_words) > 0:
                    intersection = len(words.intersection(email_words))
                    union = len(words.union(email_words))
                    score = intersection / union if union > 0 else 0
                    
                    scores.append({
                        'index': idx,
                        'score': score,
                        'text': email_text[:200] + '...' if len(email_text) > 200 else email_text,
                        'type': row.get('Email Type', 'Unknown'),
                        'similarity': f"{score:.2%}"
                    })
            
            # Sort by score and get top n
            scores.sort(key=lambda x: x['score'], reverse=True)
            similar = scores[:n]
            
        except Exception as e:
            print(f"⚠️ Error finding similar emails: {e}")
        
        return similar
    
    def get_dataset_stats(self):
        """Get dataset statistics"""
        return self.stats
    
    def search_dataset(self, query, limit=20):
        """Search the dataset for emails containing query"""
        results = []
        
        if self.dataset is None or 'Email Text' not in self.dataset.columns:
            return results
        
        try:
            query_lower = query.lower()
            mask = self.dataset['Email Text'].str.lower().str.contains(query_lower, na=False)
            matching = self.dataset[mask].head(limit)
            
            for _, row in matching.iterrows():
                results.append({
                    'text': row['Email Text'][:300] + '...' if len(row['Email Text']) > 300 else row['Email Text'],
                    'type': row.get('Email Type', 'Unknown'),
                    'index': row.get('Unnamed: 0', 0)
                })
                
        except Exception as e:
            print(f"⚠️ Error searching dataset: {e}")
        
        return results
    
    def get_phishing_patterns(self):
        """Get common phishing patterns from dataset"""
        patterns = {
            'urgent_actions': [],
            'threatening_language': [],
            'promises': [],
            'generic_greetings': [],
            'suspicious_links': []
        }
        
        # Analyze phishing emails to find patterns
        if self.dataset is not None and 'Email Text' in self.dataset.columns:
            phishing_emails = self.dataset[self.dataset['Email Type'] == 'Phishing Email']['Email Text'].tolist()
            
            if len(phishing_emails) > 0:
                # Combine all phishing texts
                all_text = ' '.join(phishing_emails[:500]).lower()
                
                # Extract patterns using regex
                urgent_patterns = re.findall(r'\b(urgent|immediate|asap|right away|now)\s+\w+', all_text)
                threat_patterns = re.findall(r'\b(suspended|closed|terminated|blocked|restricted|limited)\s+\w+', all_text)
                promise_patterns = re.findall(r'\b(winner|prize|won|award|congratulations|free|gift)\s+\w+', all_text)
                greeting_patterns = re.findall(r'\b(dear\s+(customer|user|account|sir|madam))\b', all_text)
                
                patterns['urgent_actions'] = list(set(urgent_patterns))[:10]
                patterns['threatening_language'] = list(set(threat_patterns))[:10]
                patterns['promises'] = list(set(promise_patterns))[:10]
                patterns['generic_greetings'] = list(set([g[0] for g in greeting_patterns]))[:10]
        
        return patterns

# Create global instance
dataset_connector = DatasetConnector()

# Auto-load if possible
if __name__ != "__main__":
    # When imported, try to load dataset
    try:
        dataset_connector.load_dataset()
    except Exception as e:
        print(f"⚠️ Could not auto-load dataset: {e}")