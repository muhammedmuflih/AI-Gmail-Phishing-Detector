"""
Multi-Model ML Predictor for Phishing Detection
Uses different specialized models for different email categories
Author: Your Name
Version: 2.0
"""

import joblib
import os
import re
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class MultiModelPredictor:
    """
    Advanced ML Predictor that uses multiple specialized models:
    - General phishing model
    - Job scam specific model
    - Shopping scam specific model
    """
    
    def __init__(self, models_dir='models'):
        """
        Initialize the multi-model predictor
        
        Args:
            models_dir (str): Directory containing all model files
        """
        self.models_dir = models_dir
        self.models = {}
        self.vectorizer = None
        self.model_metadata = {}
        self.loading_errors = []
        self.initialization_time = datetime.now()
        
        print("="*60)
        print("🤖 MULTI-MODEL ML PREDICTOR INITIALIZING")
        print("="*60)
        
        # Load all models
        self._load_models()
        
        # Display status
        self._show_status()
    
    def _load_models(self):
        """Load all available models from the models directory"""
        
        # Check if models directory exists
        if not os.path.exists(self.models_dir):
            error = f"Models directory not found: {self.models_dir}"
            self.loading_errors.append(error)
            print(f"❌ {error}")
            print("   Please run train_all_models.py first")
            return
        
        # ============================================
        # 1. Load Vectorizer (Required)
        # ============================================
        vec_path = os.path.join(self.models_dir, 'vectorizer.pkl')
        if os.path.exists(vec_path):
            try:
                self.vectorizer = joblib.load(vec_path)
                vec_size = os.path.getsize(vec_path) / 1024  # KB
                print(f"✅ Vectorizer loaded: {vec_size:.1f} KB")
                self.model_metadata['vectorizer'] = {
                    'loaded': True,
                    'path': vec_path,
                    'size_kb': vec_size
                }
            except Exception as e:
                error = f"Vectorizer loading failed: {e}"
                self.loading_errors.append(error)
                print(f"❌ {error}")
        else:
            error = f"Vectorizer not found: {vec_path}"
            self.loading_errors.append(error)
            print(f"❌ {error}")
        
        # ============================================
        # 2. Load General Phishing Model
        # ============================================
        self._load_single_model('general', 'phishing_model.pkl')
        
        # ============================================
        # 3. Load Job Scam Model
        # ============================================
        self._load_single_model('job', 'job_scam_model.pkl')
        
        # ============================================
        # 4. Load Shopping Scam Model
        # ============================================
        self._load_single_model('shopping', 'shopping_model.pkl')
        
        # ============================================
        # 5. Try to load additional models if available
        # ============================================
        additional_models = {
            'banking': 'banking_model.pkl',
            'tech_support': 'tech_support_model.pkl',
            'lottery': 'lottery_model.pkl'
        }
        
        for model_name, filename in additional_models.items():
            self._load_single_model(model_name, filename, required=False)
    
    def _load_single_model(self, model_name, filename, required=True):
        """Load a single model file"""
        model_path = os.path.join(self.models_dir, filename)
        
        if os.path.exists(model_path):
            try:
                self.models[model_name] = joblib.load(model_path)
                model_size = os.path.getsize(model_path) / 1024  # KB
                
                # Try to get model info
                model_info = self._extract_model_info(self.models[model_name])
                
                self.model_metadata[model_name] = {
                    'loaded': True,
                    'path': model_path,
                    'size_kb': model_size,
                    'info': model_info
                }
                print(f"✅ {model_name.capitalize()} model loaded: {model_size:.1f} KB")
                
            except Exception as e:
                error = f"{model_name.capitalize()} model loading failed: {e}"
                self.loading_errors.append(error)
                if required:
                    print(f"❌ {error}")
                else:
                    print(f"⚠️ {error}")
        else:
            if required:
                error = f"{model_name.capitalize()} model not found: {model_path}"
                self.loading_errors.append(error)
                print(f"⚠️ {error}")
    
    def _extract_model_info(self, model):
        """Extract information about the model"""
        info = {
            'type': type(model).__name__,
        }
        
        # Try to get coefficients/features if available
        if hasattr(model, 'coef_'):
            info['has_coefficients'] = True
            info['num_features'] = len(model.coef_[0]) if len(model.coef_) > 0 else 0
        
        # Try to get classes
        if hasattr(model, 'classes_'):
            info['classes'] = model.classes_.tolist()
        
        # Try to get intercept
        if hasattr(model, 'intercept_'):
            info['intercept'] = float(model.intercept_[0]) if len(model.intercept_) > 0 else None
        
        return info
    
    def _show_status(self):
        """Display initialization status"""
        print("\n" + "-"*60)
        print("📊 INITIALIZATION STATUS")
        print("-"*60)
        
        if self.vectorizer:
            print(f"✅ Vectorizer: READY")
        else:
            print(f"❌ Vectorizer: NOT LOADED")
        
        for model_name in ['general', 'job', 'shopping']:
            status = "✅ READY" if model_name in self.models else "❌ MISSING"
            print(f"   {model_name.capitalize()} model: {status}")
        
        if self.loading_errors:
            print(f"\n⚠️ Warnings/Errors: {len(self.loading_errors)}")
            for i, error in enumerate(self.loading_errors[:3]):
                print(f"   {i+1}. {error}")
        
        print("-"*60)
    
    # ============================================
    # CATEGORY DETECTION METHODS
    # ============================================
    
    def detect_category_advanced(self, text):
        """
        Advanced category detection using multiple methods
        
        Args:
            text (str): Email text to analyze
            
        Returns:
            str: Detected category ('job', 'shopping', 'general', etc.)
        """
        text = str(text).lower()
        words = text.split()
        text_length = len(words)
        
        if text_length == 0:
            return 'general'
        
        # ============================================
        # Category 1: Job-Related Keywords
        # ============================================
        job_patterns = {
            'primary': [
                'job', 'career', 'hiring', 'recruitment', 'interview',
                'salary', 'work from home', 'part time', 'full time',
                'employment', 'position', 'opening', 'vacancy',
                'resume', 'cv', 'application', 'candidate',
                'hr', 'human resources', 'recruiter', 'offer letter',
                'joining', 'appointment', 'onboarding', 'background check'
            ],
            'scam_indicators': [
                'registration fee', 'processing fee', 'training fee',
                'security deposit', 'advance payment', 'refundable',
                'pay for interview', 'buy job', 'job guarantee'
            ],
            'companies': [
                'google', 'amazon', 'microsoft', 'tcs', 'infosys',
                'wipro', 'hcl', 'tech mahindra', 'accenture', 'deloitte',
                'kpmg', 'pwc', 'ey', 'ibm', 'oracle', 'salesforce'
            ]
        }
        
        # ============================================
        # Category 2: Shopping-Related Keywords
        # ============================================
        shopping_patterns = {
            'primary': [
                'shopping', 'store', 'mall', 'market', 'supermarket',
                'gift card', 'voucher', 'coupon', 'discount', 'offer',
                'sale', 'deal', 'bargain', 'promo', 'code',
                'purchase', 'buy', 'order', 'cart', 'checkout',
                'delivery', 'shipping', 'return', 'refund',
                'product', 'item', 'merchandise', 'inventory'
            ],
            'scam_indicators': [
                'lucky winner', 'congratulations', 'you won', 'prize',
                'lottery', 'raffle', 'contest winner', 'claim now',
                'pay shipping', 'delivery charges', 'customs fee'
            ],
            'stores': [
                'big bazaar', 'd mart', 'reliance fresh', 'more',
                'amazon', 'flipkart', 'myntra', 'ajio', 'snapdeal',
                'meesho', 'nykaa', 'tata cliq', 'croma', 'vijay sales'
            ]
        }
        
        # ============================================
        # Category 3: Banking/Financial Keywords
        # ============================================
        banking_patterns = {
            'primary': [
                'bank', 'account', 'credit card', 'debit card',
                'statement', 'transaction', 'payment', 'transfer',
                'balance', 'withdrawal', 'deposit', 'loan',
                'mortgage', 'interest rate', 'emi', 'foreclosure'
            ],
            'scam_indicators': [
                'account suspended', 'unusual activity', 'unauthorized',
                'verify identity', 'confirm details', 'update information',
                'click here to verify', 'security alert'
            ],
            'banks': [
                'sbi', 'hdfc', 'icici', 'axis', 'kotak', 'yes bank',
                'pnb', 'bob', 'canara', 'union bank', 'idfc'
            ]
        }
        
        # Calculate scores for each category
        scores = {}
        
        # Job score
        job_score = 0
        for kw in job_patterns['primary']:
            if kw in text:
                job_score += 2
        for kw in job_patterns['scam_indicators']:
            if kw in text:
                job_score += 5  # Higher weight for scam indicators
        for company in job_patterns['companies']:
            if company in text:
                job_score += 3
        scores['job'] = job_score / text_length * 100  # Normalize
        
        # Shopping score
        shop_score = 0
        for kw in shopping_patterns['primary']:
            if kw in text:
                shop_score += 2
        for kw in shopping_patterns['scam_indicators']:
            if kw in text:
                shop_score += 5
        for store in shopping_patterns['stores']:
            if store in text:
                shop_score += 3
        scores['shopping'] = shop_score / text_length * 100
        
        # Banking score
        bank_score = 0
        for kw in banking_patterns['primary']:
            if kw in text:
                bank_score += 2
        for kw in banking_patterns['scam_indicators']:
            if kw in text:
                bank_score += 5
        for bank in banking_patterns['banks']:
            if bank in text:
                bank_score += 3
        scores['banking'] = bank_score / text_length * 100
        
        # Find category with highest score
        if max(scores.values()) < 2:  # Threshold for detection
            return 'general'
        
        detected = max(scores, key=scores.get)
        return detected
    
    def detect_category_fast(self, text):
        """
        Fast category detection using simple keyword matching
        
        Args:
            text (str): Email text to analyze
            
        Returns:
            str: Detected category
        """
        text = str(text).lower()
        
        # Simple keyword sets
        job_keywords = {'job', 'work', 'interview', 'salary', 'hiring', 
                       'recruitment', 'career', 'resume', 'cv'}
        shop_keywords = {'shopping', 'store', 'gift', 'voucher', 'coupon',
                        'discount', 'sale', 'order', 'delivery'}
        bank_keywords = {'bank', 'account', 'credit', 'debit', 'payment',
                        'transaction', 'balance', 'loan'}
        
        # Count matches
        job_count = sum(1 for kw in job_keywords if kw in text)
        shop_count = sum(1 for kw in shop_keywords if kw in text)
        bank_count = sum(1 for kw in bank_keywords if kw in text)
        
        if job_count > shop_count and job_count > bank_count and job_count >= 2:
            return 'job'
        elif shop_count > job_count and shop_count > bank_count and shop_count >= 2:
            return 'shopping'
        elif bank_count > job_count and bank_count > shop_count and bank_count >= 2:
            return 'banking'
        else:
            return 'general'
    
    def detect_category(self, text, method='advanced'):
        """
        Main category detection method
        
        Args:
            text (str): Email text
            method (str): 'advanced' or 'fast'
            
        Returns:
            str: Detected category
        """
        if method == 'advanced':
            return self.detect_category_advanced(text)
        else:
            return self.detect_category_fast(text)
    
    # ============================================
    # TEXT PREPROCESSING
    # ============================================
    
    def preprocess_email(self, email_data):
        """
        Extract and preprocess text from email data
        
        Args:
            email_data (dict): Email data with subject, body, etc.
            
        Returns:
            str: Preprocessed text for ML
        """
        text_parts = []
        
        # Add subject (important for phishing)
        if email_data.get('subject'):
            subject = str(email_data['subject']).lower()
            text_parts.append(f"SUBJECT: {subject}")
        
        # Add sender (for domain analysis)
        if email_data.get('from'):
            sender = str(email_data['from']).lower()
            text_parts.append(f"SENDER: {sender}")
            
            # Extract email domain
            email_match = re.search(r'@([\w.-]+)', sender)
            if email_match:
                domain = email_match.group(1)
                text_parts.append(f"DOMAIN: {domain}")
        
        # Add body text
        if email_data.get('body_text'):
            body = str(email_data['body_text']).lower()
            # Clean body
            body = re.sub(r'http\S+', ' URL ', body)  # Replace URLs with token
            body = re.sub(r'[^\w\s@.]', ' ', body)    # Remove special chars
            body = re.sub(r'\s+', ' ', body).strip()  # Remove extra spaces
            text_parts.append(body)
        
        # Add HTML content if available (clean it)
        if email_data.get('body_html'):
            html = str(email_data['body_html']).lower()
            # Simple HTML cleaning
            html = re.sub(r'<[^>]+>', ' ', html)
            html = re.sub(r'http\S+', ' URL ', html)
            html = re.sub(r'[^\w\s@.]', ' ', html)
            html = re.sub(r'\s+', ' ', html).strip()
            if len(html) > 50:  # Only if substantial content
                text_parts.append(html)
        
        # Combine all parts
        combined = ' '.join(text_parts)
        
        # Final cleaning
        combined = combined.lower()
        combined = re.sub(r'\s+', ' ', combined).strip()
        
        return combined
    
    # ============================================
    # PREDICTION METHODS
    # ============================================
    
    def predict_single(self, text, model_name):
        """
        Predict using a single specified model
        
        Args:
            text (str): Preprocessed text
            model_name (str): Name of model to use
            
        Returns:
            dict: Prediction results
        """
        if model_name not in self.models:
            return {
                'success': False,
                'error': f"Model '{model_name}' not available",
                'is_phishing': False,
                'score': 0,
                'confidence': 0
            }
        
        try:
            model = self.models[model_name]
            X = self.vectorizer.transform([text])
            
            # Get prediction
            pred = model.predict(X)[0]
            
            # Get probabilities
            if hasattr(model, 'predict_proba'):
                proba = model.predict_proba(X)[0]
                confidence = float(max(proba))
                phishing_prob = float(proba[1]) if len(proba) > 1 else 0.5
            else:
                confidence = 1.0 if pred == 1 else 0.0
                phishing_prob = confidence
            
            return {
                'success': True,
                'is_phishing': bool(pred),
                'score': round(phishing_prob * 100, 2),
                'confidence': round(confidence, 4),
                'phishing_probability': round(phishing_prob, 4)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'is_phishing': False,
                'score': 0,
                'confidence': 0
            }
    
    def predict(self, email_data, detailed=True):
        """
        Main prediction method - uses category detection and appropriate model
        
        Args:
            email_data (dict): Email data with subject, body, etc.
            detailed (bool): Whether to return detailed results
            
        Returns:
            dict: Comprehensive prediction results
        """
        # Check if vectorizer and models are available
        if self.vectorizer is None:
            return {
                'success': False,
                'error': 'Vectorizer not loaded',
                'ml_available': False,
                'is_phishing': False,
                'score': 0,
                'model_used': None
            }
        
        if not self.models:
            return {
                'success': False,
                'error': 'No models loaded',
                'ml_available': False,
                'is_phishing': False,
                'score': 0,
                'model_used': None
            }
        
        try:
            # Preprocess email
            text = self.preprocess_email(email_data)
            text_length = len(text)
            
            if text_length < 20:
                return {
                    'success': False,
                    'error': f'Text too short: {text_length} chars',
                    'ml_available': True,
                    'is_phishing': False,
                    'score': 0,
                    'model_used': None,
                    'text_length': text_length
                }
            
            # Detect category
            category = self.detect_category(text, method='advanced')
            
            # Get predictions from all models
            all_predictions = {}
            for model_name in self.models:
                all_predictions[model_name] = self.predict_single(text, model_name)
            
            # Determine which model to use for final prediction
            if category in self.models and all_predictions[category]['success']:
                # Use category-specific model
                final = all_predictions[category]
                model_used = category
            elif 'general' in self.models and all_predictions['general']['success']:
                # Fallback to general model
                final = all_predictions['general']
                model_used = 'general'
            else:
                # Use any available model
                for model_name, pred in all_predictions.items():
                    if pred['success']:
                        final = pred
                        model_used = model_name
                        break
                else:
                    # No working models
                    return {
                        'success': False,
                        'error': 'No working models',
                        'ml_available': True,
                        'is_phishing': False,
                        'score': 0,
                        'model_used': None
                    }
            
            # Determine risk level
            score = final['score']
            if score >= 80:
                risk_level = 'Critical'
            elif score >= 60:
                risk_level = 'High'
            elif score >= 40:
                risk_level = 'Medium'
            elif score >= 20:
                risk_level = 'Low'
            else:
                risk_level = 'Safe'
            
            # Prepare result
            result = {
                'success': True,
                'ml_available': True,
                'category_detected': category,
                'model_used': model_used,
                'is_phishing': final['is_phishing'],
                'score': final['score'],
                'confidence': final['confidence'],
                'risk_level': risk_level,
                'text_length': text_length,
                'text_preview': text[:200] + '...' if text_length > 200 else text
            }
            
            # Add detailed predictions if requested
            if detailed:
                result['all_predictions'] = {}
                for model_name, pred in all_predictions.items():
                    if pred['success']:
                        result['all_predictions'][model_name] = {
                            'is_phishing': pred['is_phishing'],
                            'score': pred['score'],
                            'confidence': pred['confidence']
                        }
                    else:
                        result['all_predictions'][model_name] = {
                            'error': pred.get('error', 'Unknown error')
                        }
            
            return result
            
        except Exception as e:
            import traceback
            return {
                'success': False,
                'error': str(e),
                'traceback': traceback.format_exc(),
                'ml_available': True,
                'is_phishing': False,
                'score': 0,
                'model_used': None
            }
    
    # ============================================
    # BATCH PREDICTION
    # ============================================
    
    def predict_batch(self, emails_data):
        """
        Predict for multiple emails
        
        Args:
            emails_data (list): List of email data dictionaries
            
        Returns:
            list: List of prediction results
        """
        results = []
        for email_data in emails_data:
            result = self.predict(email_data, detailed=False)
            results.append(result)
        return results
    
    # ============================================
    # UTILITY METHODS
    # ============================================
    
    def get_status(self):
        """
        Get detailed status of all models
        
        Returns:
            dict: Status information
        """
        return {
            'initialization_time': self.initialization_time.isoformat(),
            'models_loaded': list(self.models.keys()),
            'model_count': len(self.models),
            'vectorizer_loaded': self.vectorizer is not None,
            'model_metadata': self.model_metadata,
            'loading_errors': self.loading_errors,
            'error_count': len(self.loading_errors),
            'is_ready': self.vectorizer is not None and len(self.models) > 0
        }
    
    def get_model_info(self, model_name=None):
        """
        Get information about specific model or all models
        
        Args:
            model_name (str, optional): Specific model name
            
        Returns:
            dict: Model information
        """
        if model_name:
            if model_name in self.model_metadata:
                return self.model_metadata[model_name]
            else:
                return {'error': f'Model {model_name} not found'}
        else:
            return self.model_metadata
    
    def reload_models(self):
        """Reload all models (useful after training new models)"""
        print("\n🔄 Reloading all models...")
        self.models = {}
        self.model_metadata = {}
        self.loading_errors = []
        self._load_models()
        self._show_status()
        return self.get_status()
    
    def test_prediction(self, text):
        """
        Quick test method for a text string
        
        Args:
            text (str): Text to analyze
            
        Returns:
            dict: Prediction result
        """
        email_data = {
            'subject': '',
            'body_text': text,
            'from': ''
        }
        return self.predict(email_data)


# ============================================
# Create global instance
# ============================================
print("\n" + "="*60)
print("🔧 INITIALIZING MULTI-MODEL PREDICTOR")
print("="*60)

try:
    ml_predictor = MultiModelPredictor(models_dir='models')
    
    # Test if predictor is ready
    if ml_predictor.vectorizer and ml_predictor.models:
        print("\n✅ Multi-Model Predictor is READY!")
        print(f"   Models loaded: {', '.join(ml_predictor.models.keys())}")
    else:
        print("\n⚠️ Predictor initialized but not fully ready")
        print("   Please check the errors above")
        
except Exception as e:
    print(f"\n❌ Failed to initialize predictor: {e}")
    
    # Create a dummy predictor as fallback
    class DummyPredictor:
        def __init__(self):
            self.models = {}
            self.vectorizer = None
            
        def predict(self, email_data):
            return {
                'success': False,
                'error': 'ML predictor not available',
                'ml_available': False,
                'is_phishing': False,
                'score': 0,
                'model_used': None
            }
        
        def get_status(self):
            return {
                'models_loaded': [],
                'vectorizer_loaded': False,
                'is_ready': False,
                'error': 'Dummy predictor (ML not available)'
            }
    
    ml_predictor = DummyPredictor()
    print("⚠️ Using dummy predictor as fallback")

print("\n" + "="*60)