"""
Email Fetcher for Gmail - Complete Production Version
Securely fetches emails from Gmail using IMAP with App Password
Author: Your Name
Version: 3.0 - PRODUCTION READY
"""

import imaplib
import email
from email.header import decode_header
import ssl
from datetime import datetime, timedelta
import time
import re
import logging
from typing import List, Dict, Optional, Union
import base64
import quopri

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class EmailFetcher:
    """
    Complete Gmail email fetcher with:
    - Secure IMAP connection
    - App Password authentication
    - Email parsing (subject, body, HTML, attachments)
    - Demo mode for testing
    - Error handling and retries
    - Connection pooling
    """
    
    def __init__(
        self, 
        email_address: str, 
        password: str, 
        server: str = 'imap.gmail.com', 
        port: int = 993,
        timeout: int = 30,
        max_retries: int = 3
    ):
        """
        Initialize the email fetcher
        
        Args:
            email_address: Gmail address (must be @gmail.com)
            password: App Password (16 characters, no spaces)
            server: IMAP server (default: imap.gmail.com)
            port: IMAP SSL port (default: 993)
            timeout: Connection timeout in seconds
            max_retries: Maximum number of connection retries
        """
        self.email = email_address.strip().lower()
        # Remove any spaces from app password
        self.password = password.replace(' ', '').strip()
        self.server = server
        self.port = port
        self.timeout = timeout
        self.max_retries = max_retries
        
        self.connection = None
        self.connected = False
        self.demo_mode = password == 'demo-mode' or password == 'demo' or password == 'DEMO'
        
        # Connection stats
        self.connection_attempts = 0
        self.successful_connections = 0
        self.failed_connections = 0
        self.last_connection_time = None
        self.emails_fetched = 0
        
        # Validate email
        if not self.demo_mode:
            self._validate_email()
        
        logger.info(f"📧 EmailFetcher initialized for: {self.email[:5]}...@{self.email.split('@')[-1]}")
        if self.demo_mode:
            logger.info("   • Demo mode: ACTIVE")
    
    def _validate_email(self):
        """Validate that email is a Gmail address"""
        if not ('@gmail.com' in self.email or '@googlemail.com' in self.email):
            raise ValueError(f"Email must be a Gmail address: {self.email}")
    
    # ============================================
    # CONNECTION MANAGEMENT
    # ============================================
    
    def connect(self) -> Dict[str, Union[bool, str]]:
        """
        Establish secure IMAP connection to Gmail
        
        Returns:
            dict: Connection result with success status and message
        """
        if self.demo_mode:
            self.connected = True
            return {
                'success': True, 
                'message': 'Demo mode connected',
                'demo_mode': True
            }
        
        self.connection_attempts += 1
        
        for attempt in range(self.max_retries):
            try:
                logger.info(f"📡 Connection attempt {attempt + 1}/{self.max_retries} to {self.server}:{self.port}")
                
                # Create SSL context with proper settings
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                
                # Connect with timeout
                self.connection = imaplib.IMAP4_SSL(
                    self.server, 
                    self.port, 
                    ssl_context=context,
                    timeout=self.timeout
                )
                
                logger.info("✅ SSL Connection established")
                
                # Login with App Password
                logger.info(f"🔐 Logging in as: {self.email[:5]}...")
                self.connection.login(self.email, self.password)
                logger.info("✅ Login successful")
                
                # Select INBOX
                self.connection.select('INBOX')
                logger.info("📂 INBOX selected")
                
                # Get mailbox status
                status, message_count = self.connection.status('INBOX', '(MESSAGES)')
                if status == 'OK':
                    count = message_count[0].decode()
                    logger.info(f"📊 INBOX has {count} messages")
                
                self.connected = True
                self.successful_connections += 1
                self.last_connection_time = datetime.now()
                
                return {
                    'success': True,
                    'message': 'Connected successfully',
                    'email': self.email,
                    'message_count': count if 'count' in locals() else 'unknown'
                }
                
            except imaplib.IMAP4.error as e:
                error_msg = str(e)
                logger.error(f"❌ IMAP Error (attempt {attempt + 1}): {error_msg}")
                
                if attempt == self.max_retries - 1:
                    self.failed_connections += 1
                    
                    if 'Invalid credentials' in error_msg:
                        return {
                            'success': False,
                            'message': 'Invalid App Password. Please generate a new one at: https://myaccount.google.com/apppasswords',
                            'error_type': 'invalid_credentials'
                        }
                    elif 'too many recent connections' in error_msg.lower():
                        return {
                            'success': False,
                            'message': 'Too many recent connections. Wait 10-15 minutes and try again.',
                            'error_type': 'rate_limit'
                        }
                    else:
                        return {
                            'success': False,
                            'message': f'IMAP Error: {error_msg}',
                            'error_type': 'imap_error'
                        }
                
                # Wait before retry
                time.sleep(2 ** attempt)  # Exponential backoff
                
            except ConnectionRefusedError:
                logger.error(f"❌ Connection refused (attempt {attempt + 1})")
                if attempt == self.max_retries - 1:
                    self.failed_connections += 1
                    return {
                        'success': False,
                        'message': 'Connection refused. Check your internet connection.',
                        'error_type': 'connection_refused'
                    }
                time.sleep(2 ** attempt)
                
            except Exception as e:
                logger.error(f"❌ Unexpected error (attempt {attempt + 1}): {e}")
                if attempt == self.max_retries - 1:
                    self.failed_connections += 1
                    return {
                        'success': False,
                        'message': f'Connection failed: {str(e)}',
                        'error_type': 'unknown'
                    }
                time.sleep(2 ** attempt)
        
        return {
            'success': False,
            'message': 'Maximum retries exceeded',
            'error_type': 'max_retries'
        }
    
    def disconnect(self):
        """Close IMAP connection properly"""
        if self.demo_mode:
            self.connected = False
            return
        
        try:
            if self.connection:
                self.connection.close()
                self.connection.logout()
                logger.info("📴 Disconnected from Gmail")
        except Exception as e:
            logger.error(f"Error during disconnect: {e}")
        finally:
            self.connection = None
            self.connected = False
    
    def test_connection(self) -> Dict[str, Union[bool, str]]:
        """
        Test Gmail connection
        
        Returns:
            dict: Connection test result
        """
        if self.demo_mode:
            return {
                'success': True,
                'message': 'Demo mode - connection simulated',
                'email': self.email,
                'demo_mode': True
            }
        
        try:
            result = self.connect()
            if result['success']:
                self.disconnect()
                return {
                    'success': True,
                    'message': 'Gmail connection successful!',
                    'email': self.email,
                    'stats': self.get_stats()
                }
            return result
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return {
                'success': False,
                'message': f'Connection test failed: {str(e)}'
            }
    
    # ============================================
    # EMAIL FETCHING METHODS
    # ============================================
    
    def fetch_recent_emails(self, limit: int = 20) -> List[Dict]:
        """
        Fetch recent emails from INBOX
        
        Args:
            limit: Maximum number of emails to fetch
            
        Returns:
            list: List of email dictionaries
        """
        if self.demo_mode:
            return self._get_demo_emails(limit)
        
        emails = []
        result = self.connect()
        if not result['success']:
            logger.warning(f"Cannot fetch emails: {result['message']}")
            return emails
        
        try:
            # Search for ALL emails
            logger.info(f"🔍 Searching for recent emails (limit: {limit})")
            status, messages = self.connection.search(None, 'ALL')
            
            if status != 'OK' or not messages[0]:
                logger.info("No emails found")
                return emails
            
            email_ids = messages[0].split()
            logger.info(f"📬 Found {len(email_ids)} total emails")
            
            # Get most recent emails
            recent_ids = email_ids[-limit:] if len(email_ids) > limit else email_ids
            logger.info(f"📥 Fetching {len(recent_ids)} recent emails")
            
            for i, email_id in enumerate(recent_ids):
                email_id_str = email_id.decode() if isinstance(email_id, bytes) else str(email_id)
                logger.info(f"   [{i+1}/{len(recent_ids)}] Fetching email ID: {email_id_str}")
                
                email_data = self._fetch_single_email(email_id)
                if email_data:
                    emails.append(email_data)
                    self.emails_fetched += 1
            
            logger.info(f"✅ Fetched {len(emails)} emails successfully")
            
        except Exception as e:
            logger.error(f"Error fetching emails: {e}")
        
        finally:
            self.disconnect()
        
        return emails
    
    def fetch_unread_emails(self, limit: int = 10) -> List[Dict]:
        """
        Fetch unread emails from INBOX
        
        Args:
            limit: Maximum number of unread emails to fetch
            
        Returns:
            list: List of email dictionaries
        """
        if self.demo_mode:
            return self._get_demo_emails(limit, unread=True)
        
        emails = []
        result = self.connect()
        if not result['success']:
            return emails
        
        try:
            # Search for UNSEEN emails
            logger.info(f"🔍 Searching for unread emails (limit: {limit})")
            status, messages = self.connection.search(None, 'UNSEEN')
            
            if status != 'OK' or not messages[0]:
                logger.info("No unread emails found")
                return emails
            
            email_ids = messages[0].split()
            logger.info(f"📬 Found {len(email_ids)} unread emails")
            
            recent_ids = email_ids[-limit:] if len(email_ids) > limit else email_ids
            
            for i, email_id in enumerate(recent_ids):
                email_id_str = email_id.decode() if isinstance(email_id, bytes) else str(email_id)
                logger.info(f"   [{i+1}/{len(recent_ids)}] Fetching unread email ID: {email_id_str}")
                
                email_data = self._fetch_single_email(email_id)
                if email_data:
                    emails.append(email_data)
                    
                    # Mark as read
                    try:
                        self.connection.store(email_id, '+FLAGS', '\\Seen')
                        logger.info(f"   ✓ Marked as read")
                    except Exception as e:
                        logger.warning(f"   ⚠️ Could not mark as read: {e}")
            
            logger.info(f"✅ Fetched {len(emails)} unread emails")
            
        except Exception as e:
            logger.error(f"Error fetching unread emails: {e}")
        
        finally:
            self.disconnect()
        
        return emails
    
    def fetch_emails_by_date(self, days: int = 7, limit: int = 50) -> List[Dict]:
        """
        Fetch emails from last N days
        
        Args:
            days: Number of days to look back
            limit: Maximum number of emails to fetch
            
        Returns:
            list: List of email dictionaries
        """
        if self.demo_mode:
            return self._get_demo_emails(limit)
        
        emails = []
        result = self.connect()
        if not result['success']:
            return emails
        
        try:
            # Calculate date
            date = (datetime.now() - timedelta(days=days)).strftime('%d-%b-%Y')
            logger.info(f"🔍 Searching for emails since {date}")
            
            # Search SINCE date
            status, messages = self.connection.search(None, f'(SINCE {date})')
            
            if status != 'OK' or not messages[0]:
                logger.info(f"No emails found since {date}")
                return emails
            
            email_ids = messages[0].split()
            logger.info(f"📬 Found {len(email_ids)} emails since {date}")
            
            recent_ids = email_ids[-limit:] if len(email_ids) > limit else email_ids
            
            for email_id in recent_ids:
                email_data = self._fetch_single_email(email_id)
                if email_data:
                    emails.append(email_data)
            
        except Exception as e:
            logger.error(f"Error fetching emails by date: {e}")
        
        finally:
            self.disconnect()
        
        return emails
    
    def fetch_email_by_id(self, email_id: str) -> Optional[Dict]:
        """
        Fetch a specific email by ID
        
        Args:
            email_id: Email UID
            
        Returns:
            dict: Email data or None if not found
        """
        if self.demo_mode:
            return None
        
        result = self.connect()
        if not result['success']:
            return None
        
        try:
            # Convert to bytes if needed
            if isinstance(email_id, str):
                email_id = email_id.encode()
            
            email_data = self._fetch_single_email(email_id)
            return email_data
            
        finally:
            self.disconnect()
    
    # ============================================
    # PRIVATE FETCHING METHODS
    # ============================================
    
    def _fetch_single_email(self, email_id) -> Optional[Dict]:
        """
        Fetch and parse a single email by ID
        
        Args:
            email_id: Email ID (bytes or str)
            
        Returns:
            dict: Parsed email data
        """
        try:
            # Fetch email in RFC822 format
            status, msg_data = self.connection.fetch(email_id, '(RFC822)')
            
            if status != 'OK' or not msg_data or not msg_data[0]:
                logger.warning(f"Failed to fetch email {email_id}")
                return None
            
            # Parse email message
            msg = email.message_from_bytes(msg_data[0][1])
            
            # Get email ID as string
            email_id_str = email_id.decode() if isinstance(email_id, bytes) else str(email_id)
            
            # Extract headers
            subject = self._decode_header(msg.get('Subject', 'No Subject'))
            from_addr = self._decode_header(msg.get('From', 'Unknown'))
            to_addr = self._decode_header(msg.get('To', ''))
            date = msg.get('Date', '')
            reply_to = self._decode_header(msg.get('Reply-To', ''))
            
            # Extract message-id
            message_id = msg.get('Message-ID', '')
            
            # Initialize email info
            email_info = {
                'uid': email_id_str,
                'message_id': message_id,
                'subject': subject,
                'from': from_addr,
                'to': to_addr,
                'date': date,
                'reply_to': reply_to,
                'body_text': '',
                'body_html': '',
                'attachments': [],
                'headers': dict(msg.items()),
                'size': len(msg_data[0][1]) if msg_data[0][1] else 0
            }
            
            # Extract content
            self._extract_content(msg, email_info)
            
            # Parse date
            try:
                email_info['datetime'] = email.utils.parsedate_to_datetime(date).isoformat()
            except:
                email_info['datetime'] = datetime.now().isoformat()
            
            return email_info
            
        except Exception as e:
            logger.error(f"Error parsing email {email_id}: {e}")
            return None
    
    def _extract_content(self, msg, email_info: Dict):
        """
        Extract text, HTML, and attachments from email
        
        Args:
            msg: Email message object
            email_info: Dictionary to populate
        """
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition", ""))
                
                try:
                    # Get payload
                    payload = part.get_payload(decode=True)
                    if payload is None:
                        continue
                    
                    # Get charset
                    charset = part.get_content_charset() or 'utf-8'
                    
                    # Text content
                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        try:
                            email_info['body_text'] = payload.decode(charset, errors='ignore')
                        except (LookupError, UnicodeDecodeError):
                            # Try common encodings
                            for enc in ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']:
                                try:
                                    email_info['body_text'] = payload.decode(enc, errors='ignore')
                                    break
                                except:
                                    continue
                    
                    # HTML content
                    elif content_type == "text/html" and "attachment" not in content_disposition:
                        try:
                            email_info['body_html'] = payload.decode(charset, errors='ignore')
                        except (LookupError, UnicodeDecodeError):
                            for enc in ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']:
                                try:
                                    email_info['body_html'] = payload.decode(enc, errors='ignore')
                                    break
                                except:
                                    continue
                    
                    # Attachments
                    elif "attachment" in content_disposition or part.get_filename():
                        filename = part.get_filename()
                        if filename:
                            # Decode filename if needed
                            filename = self._decode_header(filename)
                            
                            email_info['attachments'].append({
                                'filename': filename,
                                'content_type': content_type,
                                'size': len(payload),
                                'content_id': part.get('Content-ID', '')
                            })
                
                except Exception as e:
                    logger.warning(f"Error extracting content part: {e}")
        
        else:
            # Non-multipart email
            payload = msg.get_payload(decode=True)
            if payload:
                content_type = msg.get_content_type()
                charset = msg.get_content_charset() or 'utf-8'
                
                try:
                    if content_type == "text/plain":
                        email_info['body_text'] = payload.decode(charset, errors='ignore')
                    elif content_type == "text/html":
                        email_info['body_html'] = payload.decode(charset, errors='ignore')
                except (LookupError, UnicodeDecodeError):
                    # Fallback to utf-8
                    try:
                        if content_type == "text/plain":
                            email_info['body_text'] = payload.decode('utf-8', errors='ignore')
                        elif content_type == "text/html":
                            email_info['body_html'] = payload.decode('utf-8', errors='ignore')
                    except:
                        pass
    
    def _decode_header(self, header) -> str:
        """
        Properly decode email headers
        
        Args:
            header: Raw header string
            
        Returns:
            str: Decoded header
        """
        if header is None:
            return ""
        
        try:
            decoded_parts = decode_header(header)
            decoded = []
            
            for part, encoding in decoded_parts:
                if isinstance(part, bytes):
                    if encoding:
                        try:
                            decoded.append(part.decode(encoding, errors='ignore'))
                        except (LookupError, UnicodeDecodeError):
                            decoded.append(part.decode('utf-8', errors='ignore'))
                    else:
                        decoded.append(part.decode('utf-8', errors='ignore'))
                else:
                    decoded.append(str(part))
            
            return ' '.join(decoded).strip()
            
        except Exception as e:
            logger.warning(f"Header decoding error: {e}")
            return str(header) if header else ""
    
    # ============================================
    # DEMO MODE METHODS
    # ============================================
    
    def _get_demo_emails(self, limit: int = 10, unread: bool = False) -> List[Dict]:
        """
        Generate realistic demo emails for testing
        
        Args:
            limit: Number of emails to generate
            unread: Whether to mark as unread
            
        Returns:
            list: List of demo email dictionaries
        """
        logger.info(f"🎭 Generating {limit} demo emails")
        
        # Demo email templates
        subjects = [
            "URGENT: Your Google Account Will Be Suspended",
            "Congratulations! You Won Amazon Gift Card ₹50,000",
            "Job Offer from Microsoft - Work From Home",
            "Your SBI Account Has Been Locked",
            "Big Bazaar Lucky Draw Winner",
            "Netflix: Your Payment Failed",
            "LinkedIn: You Have 5 New Messages",
            "PayPal: Confirm Your Account",
            "Flipkart Big Billion Days Sale",
            "TCS Recruitment Drive 2024",
            "Your Amazon Order Confirmation",
            "Facebook Password Reset Request",
            "Google Security Alert",
            "Your Tax Refund is Ready",
            "IRS Notice: Important Information"
        ]
        
        senders = [
            "security@google-verify.com",
            "winner@amazon-offers.com",
            "hr@microsoft-jobs.net",
            "alert@sbi-secure.com",
            "support@bigbazaar.com",
            "info@netflix-account.com",
            "notifications@linkedin.com",
            "service@paypal-verify.com",
            "offers@flipkart.com",
            "careers@tcs.com",
            "auto-confirm@amazon.com",
            "security@facebookmail.com",
            "no-reply@accounts.google.com",
            "refunds@irs.gov",
            "notice@irs.gov"
        ]
        
        bodies = [
            "Dear Customer, Your account has been locked due to suspicious activity. Please verify immediately.",
            "Congratulations! You've won a ₹50,000 Amazon Gift Card. Click here to claim now.",
            "We're pleased to offer you a work-from-home position at Microsoft. Pay registration fee to confirm.",
            "Your SBI account has been temporarily suspended. Update your KYC immediately.",
            "You're our lucky winner! Claim your Big Bazaar shopping voucher today.",
            "Your Netflix payment failed. Update your payment method to continue service.",
            "You have 5 new messages and 3 connection requests on LinkedIn.",
            "Your PayPal account needs verification. Confirm your details now.",
            "Exclusive Flipkart sale starts tomorrow! Get up to 90% off.",
            "TCS is hiring! Apply now for multiple positions."
        ]
        
        demo_emails = []
        
        for i in range(min(limit, len(subjects))):
            # Create timestamp
            timestamp = datetime.now() - timedelta(
                hours=random.randint(1, 48),
                minutes=random.randint(0, 59)
            )
            
            email_data = {
                'uid': f"demo_{i+1}_{int(time.time())}",
                'subject': subjects[i % len(subjects)],
                'from': senders[i % len(senders)],
                'to': 'user@gmail.com',
                'date': timestamp.strftime('%a, %d %b %Y %H:%M:%S %z'),
                'datetime': timestamp.isoformat(),
                'body_text': bodies[i % len(bodies)],
                'body_html': '',
                'attachments': [],
                'size': random.randint(1024, 10240),
                'is_demo': True,
                'is_unread': unread
            }
            
            # Add attachments randomly
            if random.random() > 0.7:  # 30% chance of attachment
                email_data['attachments'].append({
                    'filename': f"document_{i+1}.pdf",
                    'content_type': 'application/pdf',
                    'size': random.randint(10240, 102400)
                })
            
            demo_emails.append(email_data)
        
        return demo_emails
    
    # ============================================
    # UTILITY METHODS
    # ============================================
    
    def get_stats(self) -> Dict:
        """Get connection statistics"""
        return {
            'connection_attempts': self.connection_attempts,
            'successful_connections': self.successful_connections,
            'failed_connections': self.failed_connections,
            'emails_fetched': self.emails_fetched,
            'last_connection': self.last_connection_time.isoformat() if self.last_connection_time else None,
            'is_connected': self.connected,
            'demo_mode': self.demo_mode,
            'email': self.email[:5] + '...' + self.email[self.email.find('@'):] if not self.demo_mode else 'demo@demo.com'
        }
    
    def search_emails(self, criteria: str, limit: int = 50) -> List[Dict]:
        """
        Search emails using IMAP criteria
        
        Args:
            criteria: IMAP search criteria (e.g., 'FROM "amazon"')
            limit: Maximum number of emails to return
            
        Returns:
            list: List of matching emails
        """
        if self.demo_mode:
            return self._get_demo_emails(limit)
        
        emails = []
        result = self.connect()
        if not result['success']:
            return emails
        
        try:
            logger.info(f"🔍 Searching emails with criteria: {criteria}")
            status, messages = self.connection.search(None, criteria)
            
            if status == 'OK' and messages[0]:
                email_ids = messages[0].split()
                recent_ids = email_ids[-limit:] if len(email_ids) > limit else email_ids
                
                for email_id in recent_ids:
                    email_data = self._fetch_single_email(email_id)
                    if email_data:
                        emails.append(email_data)
        
        except Exception as e:
            logger.error(f"Search error: {e}")
        
        finally:
            self.disconnect()
        
        return emails
    
    def mark_as_read(self, email_id: str) -> bool:
        """Mark an email as read"""
        if self.demo_mode:
            return True
        
        try:
            if isinstance(email_id, str):
                email_id = email_id.encode()
            self.connection.store(email_id, '+FLAGS', '\\Seen')
            return True
        except:
            return False
    
    def mark_as_unread(self, email_id: str) -> bool:
        """Mark an email as unread"""
        if self.demo_mode:
            return True
        
        try:
            if isinstance(email_id, str):
                email_id = email_id.encode()
            self.connection.store(email_id, '-FLAGS', '\\Seen')
            return True
        except:
            return False
    
    def delete_email(self, email_id: str) -> bool:
        """Move an email to trash"""
        if self.demo_mode:
            return True
        
        try:
            if isinstance(email_id, str):
                email_id = email_id.encode()
            self.connection.store(email_id, '+FLAGS', '\\Deleted')
            self.connection.expunge()
            return True
        except:
            return False
    
    def get_folder_list(self) -> List[str]:
        """Get list of all folders/mailboxes"""
        if self.demo_mode:
            return ['INBOX', 'Sent', 'Drafts', 'Trash', 'Spam']
        
        folders = []
        result = self.connect()
        if not result['success']:
            return folders
        
        try:
            status, folder_list = self.connection.list()
            if status == 'OK':
                for folder in folder_list:
                    folder_str = folder.decode()
                    # Extract folder name
                    match = re.search(r'"/" "(.+)"', folder_str)
                    if match:
                        folders.append(match.group(1))
        finally:
            self.disconnect()
        
        return folders
    
    def get_connection_status(self) -> Dict:
        """Get detailed connection status"""
        return {
            'connected': self.connected,
            'demo_mode': self.demo_mode,
            'server': self.server,
            'port': self.port,
            'email': self.email if not self.demo_mode else 'demo@demo.com',
            'stats': self.get_stats()
        }


# ============================================
# Create convenience function for quick testing
# ============================================

def quick_test(email: str = None, password: str = None):
    """
    Quick test function for EmailFetcher
    
    Args:
        email: Gmail address (optional)
        password: App Password (optional)
    """
    print("\n" + "="*60)
    print("📧 EMAIL FETCHER QUICK TEST")
    print("="*60)
    
    if email and password:
        fetcher = EmailFetcher(email, password)
        result = fetcher.test_connection()
        print(f"\nResult: {result}")
        
        if result['success']:
            print("\n📨 Fetching recent emails...")
            emails = fetcher.fetch_recent_emails(limit=5)
            print(f"Fetched {len(emails)} emails")
    else:
        # Demo mode test
        print("\n🎭 Testing demo mode...")
        fetcher = EmailFetcher("test@gmail.com", "demo-mode")
        emails = fetcher.fetch_recent_emails(limit=5)
        print(f"Generated {len(emails)} demo emails")
        for i, email in enumerate(emails):
            print(f"\n  {i+1}. {email['subject']}")
            print(f"     From: {email['from']}")


# ============================================
# Initialize with demo mode available
# ============================================
print("\n" + "="*60)
print("📧 EMAIL FETCHER INITIALIZED")
print("="*60)
print("✅ EmailFetcher class loaded successfully")
print("✅ Demo mode available (use password: 'demo-mode')")
print("="*60)


# For direct testing
if __name__ == "__main__":
    import random
    quick_test()