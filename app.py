"""
AI Phishing Detector - Gmail.com Exclusive 
Keywords Only Version with OTP Authentication and Email Categories
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_socketio import SocketIO, emit
import threading
import time
import os
import re
import json
import ssl
import imaplib
import email
from email.header import decode_header
from datetime import datetime, timedelta
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import traceback
import warnings
import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

warnings.filterwarnings('ignore')

# ============================================
# ML Integration - DISABLED (using keywords only)
# ============================================
ML_AVAILABLE = False
DATASET_AVAILABLE = False

# ============================================
# OTP Authentication Variables
# ============================================
otp_codes = {}  # Store OTP codes with expiration
otp_attempts = {}  # Track OTP attempts

# ============================================
# Email Category Keywords
# ============================================
JOB_KEYWORDS = [
    'job', 'jobs', 'hiring', 'career', 'careers', 'recruitment',
    'vacancy', 'opening', 'position', 'apply', 'linkedin',
    'naukri', 'indeed', 'monster', 'work from home', 'remote job',
    'interview', 'offer letter', 'hr', 'recruiter', 'hiring manager',
    'talent', 'recruit', 'placement', 'employment', 'work'
]

SUPERMARKET_KEYWORDS = [
    'grocery', 'supermarket', 'bigbasket', 'blinkit', 'zepto',
    'instamart', 'amazon fresh', 'flipkart grocery', 'dunzo',
    'swiggy instamart', 'jio mart', 'spencers', 'more supermarket',
    'reliance fresh', 'nature basket', 'organic', 'daily needs',
    'vegetables', 'fruits', 'groceries', 'delivery', 'order',
    'mart', 'store', 'shop', 'retail', 'superstore', 'hypermarket'
]

PERSONS_KEYWORDS = [
    # Gmail variations
    'gmail.com', 'googlemail.com', 'mail.google.com',
    
    # Yahoo
    'yahoo.com', 'yahoo.co', 'yahoo.org', 'yahoo.net', 'yahoo.co.in',
    'yahoo.co.uk', 'yahoo.com.br', 'yahoo.com.ar', 'yahoo.com.au',
    'yahoo.com.cn', 'yahoo.com.fr', 'yahoo.com.de', 'yahoo.com.gr',
    'yahoo.com.hk', 'yahoo.com.mx', 'yahoo.com.my', 'yahoo.com.ph',
    'yahoo.com.sg', 'yahoo.com.tw', 'yahoo.com.vn', 'yahoo.es',
    'yahoo.fr', 'yahoo.ie', 'yahoo.in', 'yahoo.it', 'ymail.com',
    
    # Microsoft/Hotmail/Outlook
    'hotmail.com', 'hotmail.co', 'hotmail.org', 'hotmail.net',
    'hotmail.co.uk', 'outlook.com', 'outlook.co', 'outlook.org',
    'outlook.net', 'outlook.co.in', 'live.com', 'live.co',
    'live.org', 'live.net', 'live.co.uk', 'msn.com',
    
    # Apple
    'icloud.com', 'icloud.co', 'icloud.org', 'icloud.net',
    'me.com', 'mac.com', 'mac.co', 'mac.org', 'mac.net',
    
    # AOL
    'aol.com', 'aol.co', 'aol.org', 'aol.net', 'aim.com',
    
    # Mail.com
    'mail.com', 'mail.co', 'mail.org', 'mail.net',
    
    # GMX
    'gmx.com', 'gmx.co', 'gmx.org', 'gmx.net', 'gmx.de',
    'gmx.fr', 'gmx.es', 'gmx.at', 'gmx.ch', 'gmx.li',
    
    # Secure providers
    'protonmail.com', 'protonmail.co', 'protonmail.org',
    'protonmail.net', 'proton.me', 'protonmail.ch',
    'tutanota.com', 'tutanota.co', 'tutanota.org',
    'tutanota.net', 'tutanota.de', 'tuta.io',
    
    # Yandex
    'yandex.com', 'yandex.co', 'yandex.org', 'yandex.net',
    'yandex.ru', 'ya.ru', 'yandex.ua', 'yandex.by',
    'yandex.kz', 'yandex.uz',
    
    # Indian providers
    'rediffmail.com', 'rediffmail.co', 'rediffmail.org',
    'rediffmail.net', 'rediff.com', 'sancharnet.in',
    'vsnl.net', 'vsnl.com',
    
    # Zoho
    'zoho.com', 'zoho.co', 'zoho.org', 'zoho.net',
    'zoho.eu', 'zoho.in',
    
    # Other international
    'inbox.com', 'inbox.lv', 'email.com', 'email.org',
    'fastmail.com', 'fastmail.co', 'fastmail.org',
    'fastmail.net', 'hushmail.com', 'hushmail.co',
    'hushmail.org', 'hushmail.net', 'startmail.com',
    'runbox.com', 'posteo.net', 'kolabnow.com',
    'mailfence.com', 'countermail.com', 'safemail.io',
    'privatemail.io', 'cyberfear.com', 'guerrillamail.com',
    
    # Educational
    'edu', 'ac.uk', 'edu.au', 'ac.jp', 'ac.in', 'edu.cn',
    'student', 'alumni', 'grad', 'faculty', 'college',
    'university', 'school', 'campus', 'academic'
]

# ============================================
# DATASET UPDATER (Optional)
# ============================================
class DatasetUpdater:
    """Update dataset with new phishing emails"""
    
    def __init__(self):
        self.dataset_path = "Phishing_Email.csv"
        self.backup_path = "Phishing_Email_backup.csv"
    
    def add_email_to_dataset(self, email_data, is_phishing):
        """Add a new email to the dataset"""
        try:
            import pandas as pd
            # Load existing dataset
            df = pd.read_csv(self.dataset_path)
            
            # Create new row
            new_row = {
                'Unnamed: 0': len(df),
                'Email Text': self._format_email_for_dataset(email_data),
                'Email Type': 'Phishing Email' if is_phishing else 'Safe Email',
                'added_date': datetime.now().isoformat(),
                'source': 'gmail_detector_app'
            }
            
            # Add to dataset
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            
            # Save
            df.to_csv(self.dataset_path, index=False)
            
            # Create backup
            df.to_csv(self.backup_path, index=False)
            
            print(f"✅ Added {'phishing' if is_phishing else 'safe'} email to dataset")
            return True
            
        except Exception as e:
            print(f"❌ Error adding to dataset: {e}")
            return False
    
    def _format_email_for_dataset(self, email_data):
        """Format email data for dataset storage"""
        parts = []
        
        # Add important parts
        parts.append(f"From: {email_data.get('from', '')}")
        parts.append(f"Subject: {email_data.get('subject', '')}")
        parts.append(f"Body: {email_data.get('body_text', '')}")
        
        # Add HTML content if exists
        if email_data.get('body_html'):
            clean_html = re.sub(r'<[^>]+>', ' ', email_data['body_html'])
            parts.append(f"HTML: {clean_html}")
        
        # Add analysis reasons if available
        if email_data.get('analysis_reasons'):
            parts.append(f"Analysis: {', '.join(email_data.get('analysis_reasons', []))}")
        
        return '\n'.join(parts)

# Initialize dataset updater (optional)
dataset_updater = DatasetUpdater()

# ============================================
# OTP Helper Functions
# ============================================
def generate_otp(length=6):
    """Generate a random OTP"""
    return ''.join(random.choices(string.digits, k=length))

def send_otp_email(email, otp_code):
    """Send OTP code to user's email"""
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = f"PhishGuard AI <{email}>"
        msg['To'] = email
        msg['Subject'] = "Your PhishGuard AI Verification Code"
        
        # Email body
        body = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center; border-radius: 10px 10px 0 0;">
                <h2>PhishGuard AI</h2>
                <p>Email Verification</p>
            </div>
            <div style="padding: 30px; background-color: #f9f9f9; border-radius: 0 0 10px 10px;">
                <p>Hello,</p>
                <p>You requested to sign in to PhishGuard AI with your Gmail account. Please use the verification code below to complete the sign-in process:</p>
                <div style="background-color: #ffffff; border: 2px dashed #667eea; padding: 15px; text-align: center; margin: 20px 0; border-radius: 5px;">
                    <span style="font-size: 24px; font-weight: bold; letter-spacing: 3px;">{otp_code}</span>
                </div>
                <p>This code will expire in <strong>10 minutes</strong>.</p>
                <p>If you didn't request this code, you can safely ignore this email.</p>
                <p>Thanks,<br>PhishGuard AI Security Team</p>
            </div>
        </div>
        """
        
        msg.attach(MIMEText(body, 'html'))
        
        # Connect to Gmail SMTP
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(email, session.get('gmail_config', {}).get('password', ''))
            server.send_message(msg)
        
        return True
    except Exception as e:
        print(f"Error sending OTP: {e}")
        return False

# Flask application setup
app = Flask(__name__)
app.config['SECRET_KEY'] = 'gmail-phishing-detector-keywords-only'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

socketio = SocketIO(app, async_mode='threading', cors_allowed_origins="*")

# Global variables
monitoring_active = False
monitoring_thread = None
current_user_email = None
monitoring_email = None
email_stats = {
    'total_scanned': 0,
    'phishing_detected': 0,
    'job_emails': 0,
    'supermarket_emails': 0,
    'persons_emails': 0,
    'safe_emails': 0,
    'suspicious_emails': 0,
    'last_scan': None,
    'gmail_connected': False,
    'ml_available': False,
    'ml_detections': 0,
    'dataset_available': False,
    'dataset_detections': 0,
    'ipqs_detections': 0
}

# ============================================
# 1. Gmail Email Fetcher Class
# ============================================
class GmailFetcher:
    """Gmail.com only email fetcher"""
    
    def __init__(self, email_address, password):
        self.email = email_address
        self.password = password
        self.server = 'imap.gmail.com'
        self.port = 993
        self.imap = None
        self.connected = False
        self.debug = True
        
    def log(self, message, level='info'):
        """Debug logging"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        if self.debug:
            print(f"[{timestamp}] {message}")
    
    def connect(self):
        """Establish secure connection to Gmail"""
        try:
            self.log(f"🔗 Connecting to Gmail: {self.email}")
            
            # SSL context for Windows compatibility
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            # Connect to Gmail IMAP server
            self.log(f"🌐 Connecting to {self.server}:{self.port}")
            self.imap = imaplib.IMAP4_SSL(self.server, self.port, ssl_context=context)
            self.log("✅ SSL Connection established")
            
            # Login with App Password
            self.log("🔐 Attempting login...")
            self.imap.login(self.email, self.password)
            self.log(f"✅ Login successful for: {self.email}")
            
            # Select INBOX
            self.imap.select('INBOX')
            self.log("📂 INBOX selected successfully")
            
            self.connected = True
            return True
            
        except imaplib.IMAP4.error as e:
            error_msg = str(e)
            self.log(f"❌ IMAP Error: {error_msg}", 'error')
            
            if 'Invalid credentials' in error_msg:
                return {'success': False, 'message': 'Invalid App Password. Please generate a new one.'}
            elif 'too many recent connections' in error_msg.lower():
                return {'success': False, 'message': 'Too many connections. Wait 5 minutes and try again.'}
            else:
                return {'success': False, 'message': f'IMAP Error: {error_msg}'}
                
        except Exception as e:
            error_msg = str(e)
            self.log(f"❌ Connection Error: {error_msg}", 'error')
            self.log(f"🔍 Error details: {traceback.format_exc()}", 'error')
            return {'success': False, 'message': f'Connection failed: {error_msg}'}
    
    def test_connection(self):
        """Test Gmail connection"""
        try:
            self.log(f"🧪 Testing connection for: {self.email}")
            
            result = self.connect()
            if isinstance(result, dict) and not result.get('success', True):
                return result
            
            if self.connected:
                # Check mailbox status
                status, message_count = self.imap.status('INBOX', '(MESSAGES)')
                if status == 'OK':
                    self.log(f"📊 INBOX has {message_count[0].decode()} messages")
                else:
                    self.log("⚠️ Could not get message count")
                
                self.disconnect()
                return {
                    'success': True, 
                    'message': 'Gmail connection successful!',
                    'email': self.email
                }
            else:
                return {
                    'success': False, 
                    'message': 'Failed to connect to Gmail'
                }
                
        except Exception as e:
            error_msg = str(e)
            self.log(f"❌ Test connection error: {error_msg}", 'error')
            return {
                'success': False, 
                'message': f'Gmail connection error: {error_msg}'
            }
    
    def fetch_unread_emails(self, limit=10):
        """Fetch unread emails"""
        emails = []
        
        self.log(f"🔍 Fetching unread emails (limit: {limit})")
        
        # First connect
        result = self.connect()
        if isinstance(result, dict) and not result.get('success', True):
            self.log(f"❌ Cannot connect: {result.get('message')}", 'error')
            return emails
        
        try:
            # Search for UNSEEN emails
            self.log("👁️  Searching for UNSEEN emails...")
            status, messages = self.imap.search(None, 'UNSEEN')
            self.log(f"🔎 Search status: {status}")
            
            if status == 'OK' and messages[0]:
                email_ids = messages[0].split()
                self.log(f"📬 Found {len(email_ids)} unread emails")
                
                # Get most recent unread emails
                recent_ids = email_ids[-limit:] if len(email_ids) > limit else email_ids
                self.log(f"📥 Processing {len(recent_ids)} emails")
                
                for i, email_id in enumerate(recent_ids):
                    email_id_str = email_id.decode() if isinstance(email_id, bytes) else str(email_id)
                    self.log(f"  [{i+1}/{len(recent_ids)}] Fetching email ID: {email_id_str}")
                    
                    email_data = self._fetch_single_email(email_id)
                    if email_data:
                        emails.append(email_data)
                        subject = email_data.get('subject', 'No Subject')[:50]
                        self.log(f"    ✓ Subject: {subject}")
                    else:
                        self.log(f"    ✗ Failed to fetch email")
            else:
                self.log("ℹ️ No unread emails found")
        
        except Exception as e:
            self.log(f"❌ Error fetching unread emails: {e}", 'error')
            self.log(f"🔍 Error details: {traceback.format_exc()}", 'error')
        
        finally:
            self.disconnect()
            self.log(f"📤 Disconnected. Total fetched: {len(emails)} unread emails")
        
        return emails
    
    def fetch_recent_emails(self, limit=20):
        """Fetch recent emails"""
        emails = []
        
        self.log(f"🔍 Fetching recent emails (limit: {limit})")
        
        # First connect
        result = self.connect()
        if isinstance(result, dict) and not result.get('success', True):
            self.log(f"❌ Cannot connect: {result.get('message')}", 'error')
            return emails
        
        try:
            # Search for ALL emails
            self.log("🔎 Searching for ALL emails...")
            status, messages = self.imap.search(None, 'ALL')
            self.log(f"Search status: {status}")
            
            if status == 'OK' and messages[0]:
                email_ids = messages[0].split()
                self.log(f"📊 Found {len(email_ids)} total emails in INBOX")
                
                # Get most recent emails
                recent_ids = email_ids[-limit:] if len(email_ids) > limit else email_ids
                self.log(f"📥 Processing {len(recent_ids)} recent emails")
                
                for i, email_id in enumerate(recent_ids):
                    email_id_str = email_id.decode() if isinstance(email_id, bytes) else str(email_id)
                    self.log(f"  [{i+1}/{len(recent_ids)}] Fetching email ID: {email_id_str}")
                    
                    email_data = self._fetch_single_email(email_id)
                    if email_data:
                        emails.append(email_data)
                        subject = email_data.get('subject', 'No Subject')[:50]
                        from_addr = email_data.get('from', 'Unknown')[:30]
                        self.log(f"    ✓ From: {from_addr} | Subject: {subject}")
                    else:
                        self.log(f"    ✗ Failed to fetch email")
            else:
                self.log("ℹ️ No emails found in INBOX")
        
        except Exception as e:
            self.log(f"❌ Error fetching recent emails: {e}", 'error')
            self.log(f"🔍 Error details: {traceback.format_exc()}", 'error')
        
        finally:
            self.disconnect()
            self.log(f"📤 Disconnected. Total fetched: {len(emails)} emails")
        
        return emails
    
    def _fetch_single_email(self, email_id):
        """Fetch a single email by ID"""
        try:
            # Fetch email in RFC822 format
            status, msg_data = self.imap.fetch(email_id, '(RFC822)')
            
            if status != 'OK' or not msg_data or not msg_data[0]:
                self.log(f"⚠️ Failed to fetch email {email_id}", 'warning')
                return None
            
            # Parse email message
            msg = email.message_from_bytes(msg_data[0][1])
            
            # Extract email information
            email_info = {
                'uid': email_id.decode() if isinstance(email_id, bytes) else str(email_id),
                'subject': self._decode_header(msg.get('Subject', 'No Subject')),
                'from': self._decode_header(msg.get('From', 'Unknown')),
                'to': self._decode_header(msg.get('To', '')),
                'date': msg.get('Date', ''),
                'reply_to': msg.get('Reply-To', ''),
                'body_text': '',
                'body_html': '',
                'attachments': [],
                'headers': dict(msg.items()),
                'is_gmail': 'gmail.com' in self.email.lower()
            }
            
            # Extract content from email
            self._extract_content(msg, email_info)
            
            # Log email info
            self.log(f"    📧 Subject: {email_info['subject'][:60]}...", 'debug')
            self.log(f"    👤 From: {email_info['from'][:40]}", 'debug')
            
            return email_info
            
        except Exception as e:
            self.log(f"❌ Error parsing email {email_id}: {e}", 'error')
            return None
    
    def _extract_content(self, msg, email_info):
        """Extract text, HTML, and attachments from email"""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                
                try:
                    payload = part.get_payload(decode=True)
                    if payload is None:
                        continue
                    
                    charset = part.get_content_charset() or 'utf-8'
                    
                    # Text content
                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        try:
                            email_info['body_text'] = payload.decode(charset, errors='ignore')
                        except:
                            email_info['body_text'] = str(payload)
                    
                    # HTML content
                    elif content_type == "text/html" and "attachment" not in content_disposition:
                        try:
                            email_info['body_html'] = payload.decode(charset, errors='ignore')
                        except:
                            email_info['body_html'] = str(payload)
                    
                    # Attachments
                    elif "attachment" in content_disposition:
                        filename = part.get_filename()
                        if filename:
                            email_info['attachments'].append({
                                'filename': self._decode_header(filename),
                                'content_type': content_type,
                                'size': len(payload)
                            })
                            self.log(f"    📎 Attachment: {filename}", 'debug')
                
                except Exception as e:
                    self.log(f"    ⚠️ Error extracting content: {e}", 'warning')
        
        else:
            # Non-multipart email
            content_type = msg.get_content_type()
            payload = msg.get_payload(decode=True)
            
            if payload:
                charset = msg.get_content_charset() or 'utf-8'
                
                if content_type == "text/plain":
                    try:
                        email_info['body_text'] = payload.decode(charset, errors='ignore')
                    except:
                        email_info['body_text'] = str(payload)
                elif content_type == "text/html":
                    try:
                        email_info['body_html'] = payload.decode(charset, errors='ignore')
                    except:
                        email_info['body_html'] = str(payload)
    
    def _decode_header(self, header):
        """Properly decode email headers"""
        if header is None:
            return ""
        
        try:
            decoded_parts = decode_header(header)
            decoded_header = ""
            
            for part, encoding in decoded_parts:
                if isinstance(part, bytes):
                    if encoding:
                        decoded_header += part.decode(encoding, errors='ignore')
                    else:
                        decoded_header += part.decode('utf-8', errors='ignore')
                else:
                    decoded_header += str(part)
            
            return decoded_header.strip()
        except:
            return str(header) if header else ""
    
    def disconnect(self):
        """Close IMAP connection"""
        try:
            if self.imap:
                self.imap.close()
                self.imap.logout()
                self.connected = False
                self.log(f"📴 Disconnected from Gmail")
        except:
            pass

# ============================================
# 2. Gmail Phishing Analyzer Class - Keywords Only Version
# ============================================
class GmailPhishingAnalyzer:
    """Gmail phishing detection - Keywords Only"""
    
    def __init__(self):
        # Phishing keywords - only these are checked
        self.phishing_keywords = [
            'urgent', 'verify', 'account', 'suspended', 'security',
            'login', 'password', 'confirm', 'bank', 'reset your password',
            'unusual activity', 'click here', 'limited time', 'act now',
            'your account has been', 'validate your', 'update your',
            'hacked', 'compromised', 'blocked', 'locked',
            'security alert', 'unauthorized login', 'breach', 'fraud',
            'violation', 'account terminated', 'legal action'
        ]
        
        # Job-related keywords (for categorization)
        self.job_keywords = JOB_KEYWORDS
        
        # Supermarket-related keywords (for categorization)
        self.supermarket_keywords = SUPERMARKET_KEYWORDS
        
        # Persons-related keywords (for categorization)
        self.persons_keywords = PERSONS_KEYWORDS
        
        # Suspicious display name keywords
        self.suspicious_name_keywords = [
            'security', 'alert', 'team', 'support', 'admin', 'service',
            'notification', 'verify', 'account', 'help', 'info',
            'care', 'center', 'official', 'customer', 'care',
            'google', 'gmail', 'noreply', 'no-reply'
        ]
        
        # URL shortening services
        self.url_shorteners = [
            'bit.ly', 'tinyurl.com', 'goo.gl', 'ow.ly', 'is.gd',
            'buff.ly', 'shorturl.at', 'cutt.ly', 'tiny.cc'
        ]
        
        # Dangerous file extensions
        self.dangerous_extensions = [
            '.exe', '.bat', '.cmd', '.vbs', '.js', '.jar', '.scr',
            '.pif', '.com', '.hta', '.msi', '.zip', '.rar', '.7z'
        ]

        # ✅ List of trusted domains (Whitelist)
        self.legitimate_domains = [
            'gmail.com', 'google.com', 'googleapis.com', 'gstatic.com',
            'linkedin.com', 'kaggle.com', 'microsoft.com', 'apple.com',
            'amazon.com', 'paypal.com', 'github.com', 'outlook.com',
            'youtube.com', 'twitter.com', 'facebook.com', 'instagram.com',
            'whatsapp.com', 'zoom.us', 'slack.com', 'dropbox.com',
            'spotify.com', 'netflix.com', 'adobe.com', 'salesforce.com',
            'oracle.com', 'ibm.com', 'intel.com', 'cisco.com',
            'vmware.com', 'redhat.com', 'docker.com', 'kubernetes.io',
            'python.org', 'pypi.org', 'anaconda.com', 'jupyter.org',
            'medium.com', 'substack.com', 'quora.com', 'reddit.com',
            'stackoverflow.com', 'stackexchange.com', 'github.io',
            'gitlab.com', 'bitbucket.org', 'atlassian.com', 'jira.com',
            'trello.com', 'asana.com', 'monday.com', 'notion.so',
            'evernote.com', 'box.com', 'zoho.com', 'protonmail.com',
            'tutanota.com', 'fastmail.com', 'mail.ru', 'yahoo.com',
            'aol.com', 'comcast.net', 'verizon.net', 'att.net',
            'sbcglobal.net', 'bellsouth.net', 'charter.net', 'optimum.net',
            'cox.net', 'shaw.ca', 'rogers.com', 'telus.net',
            'sympatico.ca', 'ntlworld.com', 'btinternet.com', 'sky.com',
            'talktalk.net', 'virginmedia.com', 'o2.co.uk', 'orange.fr',
            'sfr.fr', 'free.fr', 'wanadoo.fr', 'club-internet.fr',
            't-online.de', 'web.de', 'gmx.de', 'freenet.de',
            'arcor.de', 'alice.it', 'libero.it', 'tin.it',
            'virgilio.it', 'tiscali.it', 'telefonica.net', 'terra.es',
            'ya.com', 'ono.com', 'jazzfree.com', 'cyberlink.com',
            'hinet.net', 'pchome.com.tw', 'yam.com', 'seed.net.tw',
            'so-net.net.tw', 'kimo.com', 'yahoo.co.jp', 'yahoo.co.kr',
            'naver.com', 'daum.net', 'hanmail.net', 'nate.com',
            'dreamwiz.com', 'empal.com', 'korea.com', 'lycos.co.kr',
            'yahoo.co.in', 'rediffmail.com', 'sify.com', 'indiatimes.com',
            'vsnl.net', 'mtnl.net.in', 'bsnl.in', 'railnet.gov.in',
            'airtelmail.com', 'vodafone.in', 'idea.in', 'reliance.com',
            'tatacommunications.com', 'mtnl.in', 'bsnl.co.in', 'nic.in',
            'gov.in', 'edu.in', 'ac.in', 'res.in', 'ernet.in',
            'canva.com', 'analyticsvidhya.com', 'bigbasket.com', 'blinkit.com',
            'zepto.com', 'amazon.in', 'flipkart.com', 'jiomart.com',
            'spencers.in', 'relianceretail.com', 'naukri.com', 'indeed.com',
            'monster.com', 'linkedin.com'
        ]
    
    def get_email_category(self, email_data):
        """Determine email category (phishing, job, supermarket, persons, safe)"""
        subject = email_data.get('subject', '').lower()
        sender = email_data.get('from', '').lower()
        body_text = email_data.get('body_text', '').lower()
        body_html = email_data.get('body_html', '').lower()
        combined = subject + ' ' + sender + ' ' + body_text + ' ' + body_html
        
        # First check if it's phishing
        phishing_score = 0
        for keyword in self.phishing_keywords:
            if keyword in subject:
                phishing_score += 10
            if keyword in combined:
                phishing_score += 5
        
        if phishing_score >= 30:
            return 'phishing'
        
        # Check for job keywords
        for keyword in self.job_keywords:
            if keyword in combined:
                return 'job'
        
        # Check for supermarket keywords
        for keyword in self.supermarket_keywords:
            if keyword in combined:
                return 'supermarket'
        
        # Check for persons keywords (personal email domains)
        for keyword in self.persons_keywords:
            if keyword in sender:
                return 'persons'
        
        return 'safe'
        
    def analyze_email(self, email_data):
        """Main analysis function - uses only keywords"""
        subject = email_data.get('subject', '').lower()
        sender = email_data.get('from', '').lower()
        body_text = email_data.get('body_text', '').lower()
        body_html = email_data.get('body_html', '').lower()
        combined_body = body_text + ' ' + body_html
        
        reasons = []
        category = self.get_email_category(email_data)
        
        # If phishing, add reasons
        if category == 'phishing':
            # Check for keywords in subject
            subject_score = 0
            subject_keywords_found = []
            for keyword in self.phishing_keywords:
                if keyword in subject:
                    subject_score += 10
                    subject_keywords_found.append(keyword)
            
            if subject_keywords_found:
                reasons.append(f"⚠️ Phishing keywords in subject: {', '.join(subject_keywords_found[:3])}")
            
            # Check for keywords in body
            body_score = 0
            body_keywords_found = []
            for keyword in self.phishing_keywords:
                if keyword in combined_body:
                    body_score += 5
                    body_keywords_found.append(keyword)
            
            if body_keywords_found:
                reasons.append(f"⚠️ Phishing keywords in body: {', '.join(body_keywords_found[:5])}")
        elif category == 'job':
            reasons.append(f"💼 Job-related email detected")
        elif category == 'supermarket':
            reasons.append(f"🛒 Supermarket/Grocery email detected")
        elif category == 'persons':
            reasons.append(f"👤 Personal email detected")
        else:
            reasons.append(f"✅ Safe email")
        
        # URL analysis (only for phishing)
        urls = self.extract_urls(combined_body + ' ' + body_html)
        url_score = 0
        url_reasons = []
        
        if category == 'phishing':
            for url in urls[:5]:
                if re.match(r'https?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', url):
                    url_score += 15
                    url_reasons.append(f"⚠️ URL uses IP address: {url[:30]}...")
                
                for shortener in self.url_shorteners:
                    if shortener in url:
                        url_score += 10
                        url_reasons.append(f"⚠️ URL shortener: {shortener}")
                        break
            
            reasons.extend(url_reasons)
        
        # Attachment analysis (only for phishing)
        attachments = email_data.get('attachments', [])
        attachment_score = 0
        attachment_reasons = []
        
        if category == 'phishing':
            for attachment in attachments:
                filename = attachment.get('filename', '').lower()
                for ext in self.dangerous_extensions:
                    if filename.endswith(ext):
                        attachment_score += 40
                        attachment_reasons.append(f"⛔ Dangerous attachment: {filename}")
                        break
            
            reasons.extend(attachment_reasons)
        
        # Calculate total score (max 100)
        phishing_score = 0
        if category == 'phishing':
            phishing_score = subject_score + body_score + url_score + attachment_score
            phishing_score = min(100, phishing_score)
        elif category == 'job' or category == 'supermarket' or category == 'persons':
            phishing_score = 10  # Low score for legitimate business emails
        else:
            phishing_score = 5  # Very low score for safe emails
        
        # 📧 Extract display name
        full_from = email_data.get('from', '')
        display_name = ""
        if '<' in full_from and '>' in full_from:
            display_name = full_from.split('<')[0].strip().lower()
        else:
            display_name = full_from.lower()
        
        # ⚠️ Suspicious display name detection
        is_suspicious_display = False
        for keyword in self.suspicious_name_keywords:
            if keyword in display_name and len(display_name) > 0 and category == 'phishing':
                is_suspicious_display = True
                reasons.append(f"⚠️ Suspicious sender name: '{display_name}'")
                break
        
        # 📧 Extract domain
        email_match = re.search(r'@([\w.-]+)', sender)
        sender_domain = email_match.group(1).lower() if email_match else ""
        
        # ✅ Gmail impersonator / Fake Google detection
        is_impersonator = False
        if category == 'phishing' and ('gmail' in sender_domain or 'google' in sender_domain) and \
           ('gmail.com' not in sender_domain and 'google.com' not in sender_domain):
            is_impersonator = True
            reasons.append(f"⚠️ Gmail impersonator domain: {sender_domain}")
        
        # ✅ Whitelist check
        whitelisted = False
        matched_domain = None
        for domain in self.legitimate_domains:
            if sender_domain == domain or sender_domain.endswith('.' + domain):
                whitelisted = True
                matched_domain = domain
                break
        
        # 🎯 FINAL SCORE ADJUSTMENT
        print(f"\n📊 Analysis for: {display_name} <{sender_domain}>")
        print(f"   Category: {category}")
        print(f"   Base score: {phishing_score}%")
        print(f"   Suspicious display name: {is_suspicious_display}")
        print(f"   Impersonator: {is_impersonator}")
        print(f"   Whitelisted: {whitelisted}")
        
        if category == 'phishing':
            if is_impersonator:
                phishing_score = min(phishing_score, 95)
                phishing_score = max(phishing_score, 60)
                reasons.append(f"⚠️ Gmail impersonator detected (score: {phishing_score}%)")
                print(f"   → Impersonator adjustment: {phishing_score}%")
            
            elif whitelisted and sender_domain == 'gmail.com':
                if is_suspicious_display or phishing_score >= 40:
                    phishing_score = min(phishing_score + 20, 90)
                    phishing_score = max(phishing_score, 50)
                    reasons.append(f"⚠️ Gmail sender with suspicious content (score: {phishing_score}%)")
                    print(f"   → Suspicious Gmail adjustment: {phishing_score}%")
                else:
                    phishing_score = min(phishing_score, 30)
                    reasons.append(f"✅ Legitimate Gmail sender (score capped at 30%)")
                    print(f"   → Normal Gmail cap: {phishing_score}%")
            
            elif whitelisted:
                phishing_score = min(phishing_score, 30)
                reasons.append(f"✅ Domain whitelisted: {matched_domain} (score capped at 30%)")
                print(f"   → Whitelist cap: {phishing_score}%")
        else:
            # Non-phishing emails get low scores
            if whitelisted:
                phishing_score = min(phishing_score, 20)
                print(f"   → Whitelisted business email: {phishing_score}%")
        
        # Determine risk level
        if phishing_score >= 75:
            risk_level = 'Critical'
            is_phishing = True
        elif phishing_score >= 50:
            risk_level = 'High'
            is_phishing = True
        elif phishing_score >= 30:
            risk_level = 'Medium'
            is_phishing = False
        else:
            risk_level = 'Low'
            is_phishing = False
        
        # Override is_phishing for non-phishing categories
        if category != 'phishing':
            is_phishing = False
            if risk_level == 'Medium' or risk_level == 'High':
                risk_level = 'Low'
        
        print(f"   Final score: {phishing_score}% | Risk: {risk_level} | Phishing: {is_phishing}\n")

        # Return analysis results
        return {
            'phishing_score': round(phishing_score, 2),
            'is_phishing': is_phishing,
            'risk_level': risk_level,
            'category': category,
            'reasons': reasons[:10],
            'ml_analysis': {'ml_available': False},
            'dataset_analysis': {'available': False},
            'ipqs_analysis': {'urls_checked': 0},
            'details': {
                'extracted_urls': urls[:5],
                'attachments_found': len(attachments),
                'is_gmail_sender': 'gmail.com' in sender,
                'text_length': len(combined_body),
                'has_html': bool(body_html.strip()),
                'keywords_found': {
                    'subject': subject_keywords_found if category == 'phishing' else [],
                    'body': body_keywords_found[:10] if category == 'phishing' else []
                }
            },
            'analysis_time': datetime.now().isoformat(),
            'ml_used': False,
            'dataset_used': False,
            'ipqs_used': False
        }
    
    def extract_urls(self, text):
        """Extract URLs from text"""
        url_pattern = r'https?://[^\s<>"\']+|www\.[^\s<>"\']+'
        urls = re.findall(url_pattern, text, re.IGNORECASE)
        return list(set(urls))

# Initialize analyzer
analyzer = GmailPhishingAnalyzer()

# ============================================
# 3. Flask Routes
# ============================================
@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/google_signin', methods=['POST'])
def google_signin():
    """Handle Google Sign-In"""
    try:
        data = request.get_json()
        credential = data.get('credential')
        
        # In a production app, you would verify the credential with Google
        # For demo purposes, we'll extract info from the credential
        # This is a simplified version - in production use google-auth library
        
        # Decode the credential (JWT) to get user info
        # For demo, we'll create a mock response
        mock_user = {
            'success': True,
            'name': 'Gmail User',
            'email': 'user@gmail.com',
            'picture': ''
        }
        
        # Save user info in session
        session['google_user'] = mock_user
        session['email'] = mock_user['email']
        
        return jsonify(mock_user)
        
    except Exception as e:
        print(f"Google Sign-In error: {e}")
        return jsonify({
            'success': False,
            'message': str(e)
        })

@app.route('/gmail_test', methods=['POST'])
def gmail_test():
    """Test Gmail connection and send OTP"""
    try:
        data = request.get_json()
        
        if not data or 'email' not in data or 'password' not in data:
            return jsonify({
                'success': False, 
                'message': 'Gmail email and app password required'
            })
        
        # Validate Gmail email
        email_address = data['email'].strip().lower()
        if not ('@gmail.com' in email_address or '@googlemail.com' in email_address):
            return jsonify({
                'success': False,
                'message': 'Please use a Gmail.com or Googlemail.com email address'
            })
        
        # Create Gmail fetcher
        fetcher = GmailFetcher(
            email_address=email_address,
            password=data['password'].strip()
        )
        
        # Test connection
        result = fetcher.test_connection()
        
        if result['success']:
            # Store in session
            session['gmail_config'] = {
                'email': email_address,
                'password': data['password'].strip()
            }
            session['email'] = email_address
            session['otp_verified'] = False  # Reset OTP verification
            
            # Generate OTP
            otp_code = generate_otp()
            expiration = datetime.now() + timedelta(minutes=10)
            
            # Store OTP with expiration
            otp_codes[email_address] = {
                'code': otp_code,
                'expiration': expiration,
                'attempts': 0
            }
            
            # Send OTP email
            if send_otp_email(email_address, otp_code):
                return jsonify({
                    'success': True,
                    'message': 'Gmail connection successful! OTP sent to your email.',
                    'email': email_address,
                    'is_gmail': True,
                    'require_otp': True,
                    'redirect': '/otp_verification'
                })
            else:
                return jsonify({
                    'success': False,
                    'message': 'Gmail connection successful but failed to send OTP. Please try again.'
                })
        else:
            return jsonify({
                'success': False,
                'message': result.get('message', 'Connection failed')
            })
            
    except Exception as e:
        print(f"Gmail test error: {e}")
        return jsonify({
            'success': False,
            'message': f'Gmail connection error: {str(e)}'
        })

@app.route('/otp_verification')
def otp_verification():
    """OTP verification page"""
    if 'gmail_config' not in session:
        return redirect(url_for('index'))
    
    # Check if already verified
    if session.get('otp_verified', False):
        return redirect(url_for('gmail_dashboard'))
    
    return render_template('otp_verification.html')

@app.route('/send_otp', methods=['POST'])
def send_otp():
    """Generate and send OTP to user's email"""
    try:
        if 'gmail_config' not in session:
            return jsonify({
                'success': False,
                'message': 'Gmail not configured'
            })
        
        config = session['gmail_config']
        email_address = config['email']
        
        # Generate OTP
        otp_code = generate_otp()
        expiration = datetime.now() + timedelta(minutes=10)
        
        # Store OTP with expiration
        otp_codes[email_address] = {
            'code': otp_code,
            'expiration': expiration,
            'attempts': 0
        }
        
        # Send OTP email
        if send_otp_email(email_address, otp_code):
            return jsonify({
                'success': True,
                'message': 'OTP sent to your email',
                'expires_in': 600  # 10 minutes in seconds
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to send OTP'
            })
            
    except Exception as e:
        print(f"Error sending OTP: {e}")
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        })

@app.route('/verify_otp', methods=['POST'])
def verify_otp():
    """Verify OTP code"""
    try:
        data = request.get_json()
        otp_code = data.get('otp', '').strip()
        
        if 'gmail_config' not in session:
            return jsonify({
                'success': False,
                'message': 'Session expired'
            })
        
        config = session['gmail_config']
        email_address = config['email']
        
        # Check if OTP exists and is valid
        if email_address not in otp_codes:
            return jsonify({
                'success': False,
                'message': 'OTP not found or expired'
            })
        
        otp_data = otp_codes[email_address]
        
        # Check expiration
        if datetime.now() > otp_data['expiration']:
            del otp_codes[email_address]
            return jsonify({
                'success': False,
                'message': 'OTP expired'
            })
        
        # Check attempts
        if otp_data['attempts'] >= 3:
            del otp_codes[email_address]
            return jsonify({
                'success': False,
                'message': 'Too many attempts. Please request a new OTP.'
            })
        
        # Verify OTP
        if otp_code == otp_data['code']:
            # OTP is correct, mark as verified
            session['otp_verified'] = True
            del otp_codes[email_address]
            
            return jsonify({
                'success': True,
                'message': 'OTP verified successfully',
                'redirect': '/gmail_dashboard'
            })
        else:
            # Increment attempts
            otp_data['attempts'] += 1
            remaining_attempts = 3 - otp_data['attempts']
            
            return jsonify({
                'success': False,
                'message': f'Invalid OTP. {remaining_attempts} attempts remaining.',
                'attempts_remaining': remaining_attempts
            })
            
    except Exception as e:
        print(f"Error verifying OTP: {e}")
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        })

@app.route('/resend_otp', methods=['POST'])
def resend_otp():
    """Resend OTP to user's email"""
    try:
        if 'gmail_config' not in session:
            return jsonify({
                'success': False,
                'message': 'Session expired'
            })
        
        config = session['gmail_config']
        email_address = config['email']
        
        # Remove existing OTP if any
        if email_address in otp_codes:
            del otp_codes[email_address]
        
        # Generate new OTP
        otp_code = generate_otp()
        expiration = datetime.now() + timedelta(minutes=10)
        
        # Store OTP with expiration
        otp_codes[email_address] = {
            'code': otp_code,
            'expiration': expiration,
            'attempts': 0
        }
        
        # Send OTP email
        if send_otp_email(email_address, otp_code):
            return jsonify({
                'success': True,
                'message': 'New OTP sent to your email',
                'expires_in': 600  # 10 minutes in seconds
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to send OTP'
            })
            
    except Exception as e:
        print(f"Error resending OTP: {e}")
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        })

@app.route('/gmail_dashboard')
def gmail_dashboard():
    """Gmail dashboard with OTP verification"""
    if 'email' not in session or 'gmail_config' not in session:
        return redirect(url_for('index'))
    
    # Check if OTP is verified
    if not session.get('otp_verified', False):
        return redirect(url_for('otp_verification'))
    
    return render_template('dashboard.html')

@app.route('/start_gmail_monitoring', methods=['POST'])
def start_gmail_monitoring():
    """Start Gmail monitoring"""
    global monitoring_active, monitoring_thread
    
    if monitoring_active:
        return jsonify({
            'success': False, 
            'message': 'Gmail monitoring already active'
        })
    
    if 'gmail_config' not in session:
        return jsonify({
            'success': False, 
            'message': 'Gmail not configured'
        })
    
    # Check OTP verification
    if not session.get('otp_verified', False):
        return jsonify({
            'success': False,
            'message': 'OTP verification required'
        })
    
    # Copy session data for background thread
    thread_config = dict(session['gmail_config'])
    thread_email = session.get('email', thread_config.get('email', 'Unknown'))

    monitoring_active = True
    monitoring_email = thread_email

    # Start monitoring in background thread
    monitoring_thread = threading.Thread(
        target=monitor_gmail_loop,
        args=(thread_config, thread_email),
        daemon=True
    )
    monitoring_thread.start()

    print(f"🚀 Gmail monitoring started for: {thread_email}")

    return jsonify({
        'success': True,
        'message': 'Gmail monitoring started',
        'email': thread_email
    })

@app.route('/stop_monitoring', methods=['POST'])
def stop_monitoring():
    """Stop monitoring"""
    global monitoring_active
    monitoring_active = False
    print("⏹️ Monitoring stopped")
    return jsonify({'success': True, 'message': 'Monitoring stopped'})

@app.route('/get_gmail_status')
def get_gmail_status():
    """Get Gmail status"""
    global monitoring_active, email_stats
    return jsonify({
        'active': monitoring_active,
        'email': session.get('email'),
        'stats': email_stats,
        'is_gmail': True,
        'ml_available': False,
        'dataset_available': False,
        'ipqs_available': False,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/scan_gmail_inbox', methods=['POST'])
def scan_gmail_inbox():
    """Scan Gmail inbox"""
    try:
        if 'gmail_config' not in session:
            return jsonify({
                'success': False, 
                'message': 'Gmail not configured'
            })
        
        # Check OTP verification
        if not session.get('otp_verified', False):
            return jsonify({
                'success': False,
                'message': 'OTP verification required'
            })
        
        config = session['gmail_config']
        print(f"📨 Scanning Gmail inbox for: {config['email']}")
        
        # Create Gmail fetcher
        fetcher = GmailFetcher(
            email_address=config['email'],
            password=config['password']
        )
        
        # Fetch recent emails
        emails = fetcher.fetch_recent_emails(limit=15)
        print(f"📊 Found {len(emails)} emails to analyze")
        
        results = []
        job_count = 0
        supermarket_count = 0
        persons_count = 0
        phishing_count = 0
        safe_count = 0
        
        for i, email_data in enumerate(emails):
            print(f"🔍 Analyzing email {i+1}/{len(emails)}: {email_data.get('subject', 'No Subject')[:50]}")
            
            # Analyze email with keywords only
            analysis = analyzer.analyze_email(email_data)
            
            # Update category counts
            if analysis['category'] == 'phishing':
                phishing_count += 1
            elif analysis['category'] == 'job':
                job_count += 1
            elif analysis['category'] == 'supermarket':
                supermarket_count += 1
            elif analysis['category'] == 'persons':
                persons_count += 1
            else:
                safe_count += 1
            
            # Update stats
            global email_stats
            email_stats['total_scanned'] += 1
            if analysis['is_phishing']:
                email_stats['phishing_detected'] += 1
                email_stats['suspicious_emails'] += 1
                print(f"🚨 PHISHING DETECTED: {email_data.get('subject', 'No Subject')[:50]}")
                
                # SAVE TO DATASET (optional)
                try:
                    dataset_updater.add_email_to_dataset(email_data, True)
                    print(f"💾 Saved phishing email to dataset")
                except Exception as e:
                    print(f"❌ Error saving to dataset: {e}")
            else:
                email_stats['safe_emails'] += 1
            
            # Update category stats
            email_stats['job_emails'] = job_count
            email_stats['supermarket_emails'] = supermarket_count
            email_stats['persons_emails'] = persons_count
            
            # Prepare result
            result = {
                'id': email_data.get('uid', ''),
                'subject': email_data.get('subject', 'No Subject'),
                'sender': email_data.get('from', 'Unknown'),
                'date': email_data.get('date', ''),
                'phishing_score': analysis['phishing_score'],
                'is_phishing': analysis['is_phishing'],
                'risk_level': analysis['risk_level'],
                'category': analysis['category'],
                'reasons': analysis['reasons'],
                'has_attachments': len(email_data.get('attachments', [])) > 0,
                'attachments_count': len(email_data.get('attachments', [])),
                'is_gmail_sender': 'gmail.com' in email_data.get('from', '').lower(),
                'analysis_time': analysis['analysis_time']
            }
            results.append(result)
        
        email_stats['last_scan'] = datetime.now().isoformat()
        print(f"✅ Scan complete: {len(results)} emails analyzed")
        print(f"   📊 Phishing: {phishing_count}, Jobs: {job_count}, Supermarket: {supermarket_count}, Persons: {persons_count}, Safe: {safe_count}")
        
        return jsonify({
            'success': True,
            'count': len(results),
            'emails': results,
            'stats': {
                'total_scanned': email_stats['total_scanned'],
                'phishing_detected': email_stats['phishing_detected'],
                'job_emails': job_count,
                'supermarket_emails': supermarket_count,
                'persons_emails': persons_count,
                'safe_emails': safe_count,
                'last_scan': email_stats['last_scan']
            },
            'message': f'Scanned {len(results)} emails from Gmail'
        })
        
    except Exception as e:
        print(f"❌ Gmail scan error: {e}")
        print(f"🔍 Error details: {traceback.format_exc()}")
        return jsonify({
            'success': False,
            'message': f'Gmail scan failed: {str(e)}'
        })

@app.route('/gmail_demo_scan', methods=['POST'])
def gmail_demo_scan():
    """Gmail demo scan with categories"""
    print("🎭 Starting Gmail demo scan...")
    
    # Gmail-related sample emails with categories
    sample_emails = [
        # Phishing emails
        {
            'uid': 'phishing_demo1',
            'subject': 'URGENT: Your Gmail Account Has Been HACKED from Russia',
            'from': 'Security Alert <security@gmail-account-recovery.com>',
            'date': datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z'),
            'body_text': 'Dear Gmail User, Your account has been HACKED from an IP address in Russia. Unauthorized login detected 5 minutes ago. To secure your account, click here: http://gmail-security-verify.com/secure-account Failure to verify within 24 hours will result in account suspension. - Gmail Security Team',
            'body_html': '',
            'attachments': []
        },
        {
            'uid': 'phishing_demo2',
            'subject': 'SECURITY ALERT: Your Account Has Been COMPROMISED',
            'from': 'Security Department <security.department@gmail-verify.net>',
            'date': datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z'),
            'body_text': 'Dear Customer, We detected suspicious activity on your account. Your account has been COMPROMISED by an unauthorized user. Please verify your identity immediately: http://verify-account-security.net/login If not verified, your account will be BLOCKED permanently. - Security Department',
            'body_html': '',
            'attachments': []
        },
        # Job emails
        {
            'uid': 'job_demo1',
            'subject': 'New Job Alert: Software Engineer at Google',
            'from': 'LinkedIn Jobs <jobalerts-noreply@linkedin.com>',
            'date': datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z'),
            'body_text': 'Hi, We found a new job matching your profile: Software Engineer at Google. Apply now: https://www.linkedin.com/jobs/view/12345',
            'body_html': '',
            'attachments': []
        },
        {
            'uid': 'job_demo2',
            'subject': 'Your Dream Job Awaits! Apply for Senior Developer',
            'from': 'Naukri.com <recruitment@naukri.com>',
            'date': datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z'),
            'body_text': 'Dear Candidate, We have an exciting opportunity for a Senior Developer position at Microsoft. Click here to apply: https://www.naukri.com/job/54321',
            'body_html': '',
            'attachments': []
        },
        # Supermarket emails
        {
            'uid': 'supermarket_demo1',
            'subject': 'Your Grocery Order Confirmation',
            'from': 'BigBasket <orders@bigbasket.com>',
            'date': datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z'),
            'body_text': 'Thank you for shopping with BigBasket! Your order #BB12345 has been confirmed and will be delivered tomorrow between 7-9 AM. Track your order: https://www.bigbasket.com/track/12345',
            'body_html': '',
            'attachments': []
        },
        {
            'uid': 'supermarket_demo2',
            'subject': 'Flash Sale: 50% Off on Fresh Vegetables',
            'from': 'Blinkit <offers@blinkit.com>',
            'date': datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z'),
            'body_text': "Don't miss out! Get 50% off on all fresh vegetables today only. Shop now: https://blinkit.com/sale/veggies",
            'body_html': '',
            'attachments': []
        },
        # Persons emails
        {
            'uid': 'persons_demo1',
            'subject': 'Weekend Plans - Let\'s catch up!',
            'from': 'John Doe <john.doe@gmail.com>',
            'date': datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z'),
            'body_text': 'Hey, Hope you\'re doing well! Let\'s catch up this weekend over coffee. Let me know what time works for you. Best, John',
            'body_html': '',
            'attachments': []
        },
        {
            'uid': 'persons_demo2',
            'subject': 'Birthday Party Invitation',
            'from': 'Jane Smith <jane.smith@yahoo.com>',
            'date': datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z'),
            'body_text': 'Hi everyone! You\'re invited to my birthday party next Saturday at 7 PM. Please bring your friends and family. Looking forward to seeing you all! Love, Jane',
            'body_html': '',
            'attachments': []
        },
        # Safe emails
        {
            'uid': 'safe_demo1',
            'subject': 'Your Monthly Statement',
            'from': 'Bank of America <statements@bankofamerica.com>',
            'date': datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z'),
            'body_text': 'Your monthly statement is now available. Please login to view.',
            'body_html': '',
            'attachments': []
        }
    ]
    
    results = []
    job_count = 0
    supermarket_count = 0
    persons_count = 0
    phishing_count = 0
    safe_count = 0
    
    for i, email_data in enumerate(sample_emails):
        print(f"🔍 Analyzing demo email {i+1}/{len(sample_emails)}")
        analysis = analyzer.analyze_email(email_data)
        
        # Update category counts
        if analysis['category'] == 'phishing':
            phishing_count += 1
        elif analysis['category'] == 'job':
            job_count += 1
        elif analysis['category'] == 'supermarket':
            supermarket_count += 1
        elif analysis['category'] == 'persons':
            persons_count += 1
        else:
            safe_count += 1
        
        # Update stats
        global email_stats
        email_stats['total_scanned'] += 1
        if analysis['is_phishing']:
            email_stats['phishing_detected'] += 1
            email_stats['suspicious_emails'] += 1
        else:
            email_stats['safe_emails'] += 1
        
        email_stats['job_emails'] = job_count
        email_stats['supermarket_emails'] = supermarket_count
        email_stats['persons_emails'] = persons_count
        
        result = {
            'id': email_data['uid'],
            'subject': email_data['subject'],
            'sender': email_data['from'],
            'date': email_data['date'],
            'phishing_score': analysis['phishing_score'],
            'is_phishing': analysis['is_phishing'],
            'risk_level': analysis['risk_level'],
            'category': analysis['category'],
            'reasons': analysis['reasons'],
            'has_attachments': len(email_data['attachments']) > 0,
            'attachments_count': len(email_data['attachments']),
            'is_gmail_sender': 'gmail.com' in email_data['from'].lower(),
            'analysis_time': analysis['analysis_time'],
            'is_demo': True
        }
        results.append(result)
    
    email_stats['last_scan'] = datetime.now().isoformat()
    print(f"✅ Demo scan complete: {len(results)} emails analyzed")
    print(f"   📊 Phishing: {phishing_count}, Jobs: {job_count}, Supermarket: {supermarket_count}, Persons: {persons_count}, Safe: {safe_count}")
    
    return jsonify({
        'success': True,
        'count': len(results),
        'emails': results,
        'stats': email_stats,
        'message': 'Gmail demo scan completed'
    })

@app.route('/get_email_content/<email_id>')
def get_email_content(email_id):
    """Get full email content by ID"""
    try:
        if 'gmail_config' not in session:
            return jsonify({
                'success': False,
                'message': 'Gmail not configured'
            })
        
        # Check OTP verification
        if not session.get('otp_verified', False):
            return jsonify({
                'success': False,
                'message': 'OTP verification required'
            })
        
        config = session['gmail_config']
        
        # Create Gmail fetcher
        fetcher = GmailFetcher(
            email_address=config['email'],
            password=config['password']
        )
        
        # Connect to Gmail
        result = fetcher.connect()
        if isinstance(result, dict) and not result.get('success', True):
            return jsonify({
                'success': False,
                'message': result.get('message', 'Connection failed')
            })
        
        # Fetch the specific email by ID
        email_data = fetcher._fetch_single_email(email_id)
        fetcher.disconnect()
        
        if not email_data:
            return jsonify({
                'success': False,
                'message': 'Email not found'
            })
        
        # Analyze the email
        analysis = analyzer.analyze_email(email_data)
        
        # Return the email content
        return jsonify({
            'success': True,
            'email': {
                'id': email_data.get('uid'),
                'subject': email_data.get('subject', 'No Subject'),
                'from': email_data.get('from', 'Unknown'),
                'to': email_data.get('to', ''),
                'date': email_data.get('date', ''),
                'body_text': email_data.get('body_text', ''),
                'body_html': email_data.get('body_html', ''),
                'attachments': email_data.get('attachments', []),
                'analysis': analysis
            }
        })
        
    except Exception as e:
        print(f"Error fetching email content: {e}")
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        })

@app.route('/clear_stats', methods=['POST'])
def clear_stats():
    """Reset statistics"""
    global email_stats
    email_stats = {
        'total_scanned': 0,
        'phishing_detected': 0,
        'job_emails': 0,
        'supermarket_emails': 0,
        'persons_emails': 0,
        'safe_emails': 0,
        'suspicious_emails': 0,
        'last_scan': None,
        'gmail_connected': session.get('gmail_config') is not None,
        'ml_available': False,
        'ml_detections': 0,
        'dataset_available': False,
        'dataset_detections': 0,
        'ipqs_detections': 0
    }
    print("🧹 Statistics cleared")
    return jsonify({'success': True, 'message': 'Statistics cleared'})

@app.route('/gmail_logout')
def gmail_logout():
    """Gmail logout"""
    global monitoring_active
    monitoring_active = False
    
    # Clear session
    session.clear()
    
    # Reset stats
    global email_stats
    email_stats['gmail_connected'] = False
    email_stats['persons_emails'] = 0
    
    print("👋 User logged out")
    return redirect(url_for('index'))

# ============================================
# 4. Background Monitoring Function
# ============================================
def monitor_gmail_loop(gmail_config, user_email):
    """Background monitoring for Gmail"""
    global monitoring_active

    checked_uids = set()
    error_count = 0
    max_errors = 5

    print(f"🔄 Starting Gmail monitoring loop for: {user_email}")
    print(f"🔍 Using keywords-only detection with categories")

    while monitoring_active and error_count < max_errors:
        try:
            if not gmail_config:
                print("⏸️ No Gmail config provided, stopping monitor...")
                break

            config = gmail_config
            
            # Create Gmail fetcher
            fetcher = GmailFetcher(
                email_address=config['email'],
                password=config['password']
            )
            
            # Fetch unread emails
            emails = fetcher.fetch_unread_emails(limit=10)
            print(f"📥 Monitoring cycle: Found {len(emails)} new emails")
            
            for email_data in emails:
                email_uid = email_data.get('uid')
                
                # Skip if already processed
                if email_uid in checked_uids:
                    continue
                
                checked_uids.add(email_uid)
                
                # Analyze email with keywords only
                analysis = analyzer.analyze_email(email_data)
                
                # Update stats
                global email_stats
                email_stats['total_scanned'] += 1
                
                if analysis['category'] == 'phishing':
                    email_stats['phishing_detected'] += 1
                    email_stats['suspicious_emails'] += 1
                    
                    # Send phishing alert via WebSocket
                    socketio.emit('gmail_phishing_alert', {
                        'id': email_uid,
                        'subject': email_data.get('subject', 'No Subject'),
                        'sender': email_data.get('from', 'Unknown'),
                        'timestamp': datetime.now().isoformat(),
                        'phishing_score': analysis['phishing_score'],
                        'risk_level': analysis['risk_level'],
                        'category': analysis['category'],
                        'reasons': analysis['reasons'][:3],
                        'message': '🚨 PHISHING DETECTED!',
                        'is_gmail': True,
                        'has_attachments': len(email_data.get('attachments', [])) > 0
                    })
                    
                    print(f"🚨 REAL-TIME ALERT: Phishing email detected - {email_data.get('subject', 'No Subject')[:50]}")
                    
                    # SAVE TO DATASET (optional)
                    try:
                        dataset_updater.add_email_to_dataset(email_data, True)
                        print(f"💾 Saved real-time phishing email to dataset")
                    except Exception as e:
                        print(f"❌ Error saving to dataset: {e}")
                else:
                    if analysis['category'] == 'job':
                        email_stats['job_emails'] = email_stats.get('job_emails', 0) + 1
                    elif analysis['category'] == 'supermarket':
                        email_stats['supermarket_emails'] = email_stats.get('supermarket_emails', 0) + 1
                    elif analysis['category'] == 'persons':
                        email_stats['persons_emails'] = email_stats.get('persons_emails', 0) + 1
                    else:
                        email_stats['safe_emails'] += 1
                
                # Send email update via WebSocket
                socketio.emit('gmail_email_update', {
                    'id': email_uid,
                    'subject': email_data.get('subject', 'No Subject'),
                    'sender': email_data.get('from', 'Unknown'),
                    'timestamp': datetime.now().isoformat(),
                    'phishing_score': analysis['phishing_score'],
                    'is_phishing': analysis['is_phishing'],
                    'risk_level': analysis['risk_level'],
                    'category': analysis['category'],
                    'is_gmail': 'gmail.com' in email_data.get('from', '').lower(),
                    'has_attachments': len(email_data.get('attachments', [])) > 0
                })
            
            # Manage checked UIDs
            if len(checked_uids) > 1000:
                checked_uids = set(list(checked_uids)[-500:])
            
            # Reset error count on success
            error_count = 0
            
        except Exception as e:
            error_count += 1
            print(f"❌ Monitoring error ({error_count}/{max_errors}): {e}")
            
            socketio.emit('gmail_monitoring_error', {
                'message': f'Gmail monitoring error: {str(e)}',
                'timestamp': datetime.now().isoformat(),
                'error_count': error_count
            })
            
            if error_count >= max_errors:
                print(f"🛑 Too many errors, stopping monitoring")
                monitoring_active = False
                socketio.emit('gmail_monitoring_stopped', {
                    'message': 'Monitoring stopped due to too many errors',
                    'timestamp': datetime.now().isoformat()
                })
                break
        
        # Wait before next check
        time.sleep(30)
    
    print(f"🛑 Gmail monitoring loop stopped")

# ============================================
# 5. WebSocket Handlers
# ============================================
@socketio.on('connect')
def handle_gmail_connect():
    """WebSocket connection"""
    print(f'🔌 WebSocket client connected: {request.sid}')
    emit('gmail_connection_status', {
        'status': 'connected',
        'timestamp': datetime.now().isoformat(),
        'service': 'Gmail.com',
        'ml_available': False,
        'dataset_available': False,
        'ipqs_available': False,
        'server_time': datetime.now().strftime('%H:%M:%S')
    })

@socketio.on('disconnect')
def handle_gmail_disconnect():
    """WebSocket disconnection"""
    print(f'🔌 WebSocket client disconnected: {request.sid}')

@socketio.on('request_gmail_status')
def handle_gmail_status_request():
    """Send Gmail status"""
    emit('gmail_status_update', {
        'monitoring_active': monitoring_active,
        'current_email': session.get('email'),
        'stats': email_stats,
        'is_gmail': True,
        'ml_available': False,
        'dataset_available': False,
        'ipqs_available': False,
        'timestamp': datetime.now().isoformat(),
        'server_time': datetime.now().strftime('%H:%M:%S')
    })

# ============================================
# 6. Error Handlers
# ============================================
@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Page not found', 
        'status': 404,
        'message': 'The requested URL was not found on the server.'
    }), 404

@app.errorhandler(405)
def method_not_allowed(e):
    """Handle 405 errors"""
    return jsonify({
        'error': 'Method not allowed',
        'status': 405,
        'message': 'The requested HTTP method is not allowed for this URL.'
    }), 405

@app.errorhandler(400)
def bad_request(e):
    """Handle 400 errors"""
    return jsonify({
        'error': 'Bad request',
        'status': 400,
        'message': 'Invalid request format. Please send valid JSON data.'
    }), 400

@app.errorhandler(500)
def internal_server_error(e):
    """Handle 500 errors"""
    return jsonify({
        'error': 'Internal server error', 
        'status': 500,
        'message': 'An internal server error occurred.'
    }), 500

# ============================================
# 7. Main Entry Point
# ============================================
if __name__ == '__main__':
    print("""
    ╔════════════════════════════════════════════════════════════════╗
    ║     AI PHISHING DETECTOR - Gmail.com (Enhanced Version)       ║
    ╠════════════════════════════════════════════════════════════════╣
    ║                    EMAIL CATEGORIZATION ACTIVE                ║
    ╠════════════════════════════════════════════════════════════════╣
    ║                                                                ║
    ║  🌐 Server: http://localhost:5000                              ║
    ║  📧 Service: Gmail.com Only                                   ║
    ║  🔍 Detection: Keywords + Display Name + Domain Analysis      ║
    ║  📊 Categories: Phishing | Jobs | Supermarket | Persons | Safe   ║
    ║  🔐 Security: OTP Authentication Required                      ║
    ║                                                                ║
    ║  Features:                                                     ║
    ║  • Phishing keyword detection                                  ║
    ║  • Email categorization (Job/Supermarket/Persons/Safe)          ║
    ║  • Display name analysis                                       ║
    ║  • Gmail impersonator detection                                ║
    ║  • Real-time email monitoring                                  ║
    ║  • Whitelist for trusted domains                               ║
    ║  • OTP email verification (2FA)                                ║
    ║  • Secure session management                                   ║
    ║  • Full email content viewing                                  ║
    ║                                                                ║
    ║  Press Ctrl+C to stop                                          ║
    ╚══════════════════════════════════════════════════════════════════╝
    """)
    
    # Create directories if they don't exist
    os.makedirs('templates', exist_ok=True)
    
    # Check if templates exist
    required_templates = ['index.html', 'otp_verification.html', 'dashboard.html']
    for template in required_templates:
        template_path = os.path.join('templates', template)
        if not os.path.exists(template_path):
            print(f"⚠️ Warning: {template_path} not found")
            print(f"   Please create this file in the templates folder")
    
    # Run the application
    try:
        socketio.run(
            app,
            host='0.0.0.0',
            port=5000,
            debug=True,
            allow_unsafe_werkzeug=True,
            log_output=True
        )
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down Gmail Phishing Detector...")
        print("✅ Application stopped successfully")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        print("🔧 Check if port 5000 is available")
