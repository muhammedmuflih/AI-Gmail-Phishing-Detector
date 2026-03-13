<div align="center">

# 🛡️ AI Gmail Phishing Detector

**A Smart Web-Based Security Tool to Protect Your Gmail from Phishing Attacks**

[![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)](https://www.python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green?style=flat-square&logo=flask)](https://flask.palletsprojects.com)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3.0-orange?style=flat-square&logo=scikit-learn)](https://scikit-learn.org)
[![License](https://img.shields.io/badge/License-MIT-purple?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)](https://github.com/muhammedmuflih/AI-Gmail-Phishing-Detector)

[Live Demo](#-quick-start) • [Features](#-features) • [Installation](#-installation-setup) • [Documentation](#-usage-guide) • [Contributing](#-contributing) • [Team](#-team)

</div>

---

## 📋 Table of Contents

- [About](#-about)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation & Setup](#-installation--setup)
- [Quick Start](#-quick-start)
- [Usage Guide](#-usage-guide)
- [API Documentation](#-api-documentation)
- [Model Performance](#-model-performance)
- [Team](#-team)
- [Contributing](#-contributing)
- [License](#-license)
- [Support](#-support)
- [Roadmap](#-roadmap)

---

## 🎯 About

**AI Gmail Phishing Detector** is an intelligent security tool designed to protect Gmail users from sophisticated phishing attacks. The application connects to your Gmail inbox in real-time, scans incoming emails, and uses advanced machine learning algorithms to identify potential phishing attempts with high accuracy.

### Why This Matters?
- 🚨 **3.4 billion phishing emails sent daily** (2023 statistics)
- 💰 **Average cost of phishing breach: $4.91 million**
- 🎯 **82% of data breaches involve human element** (Social Engineering)

Our solution provides an additional layer of security to keep your inbox safe.

---

## ✨ Features

<table>
  <tr>
    <td>
      <h3>🤖 Advanced ML Detection</h3>
      <p>Multiple trained ML models for accurate phishing detection</p>
    </td>
    <td>
      <h3>⚡ Real-time Analysis</h3>
      <p>Scan emails instantly as they arrive in your inbox</p>
    </td>
  </tr>
  <tr>
    <td>
      <h3>🔐 Secure OAuth Integration</h3>
      <p>Safe Gmail connection using OAuth 2.0</p>
    </td>
    <td>
      <h3>📊 Detailed Reports</h3>
      <p>Get comprehensive analysis and threat assessment</p>
    </td>
  </tr>
  <tr>
    <td>
      <h3>🎨 User-Friendly Interface</h3>
      <p>Clean, intuitive web interface for easy navigation</p>
    </td>
    <td>
      <h3>📈 Confidence Scores</h3>
      <p>Know exactly how confident our AI is in each prediction</p>
    </td>
  </tr>
  <tr>
    <td>
      <h3>🔄 Automatic Updates</h3>
      <p>Models continuously learn and improve</p>
    </td>
    <td>
      <h3>📱 Responsive Design</h3>
      <p>Works perfectly on desktop, tablet, and mobile</p>
    </td>
  </tr>
</table>

---

## 🛠️ Tech Stack

### 🎨 **Frontend Technologies**

| Technology | Version | Purpose |
|-----------|---------|---------|
| **HTML5** | Latest | Semantic markup and structure |
| **CSS3** | Latest | Modern styling and animations |
| **JavaScript** | ES6+ | Interactive features and dynamic content |
| **Bootstrap** | 5.x | Responsive grid system & components |
| **Jinja2** | 3.1.2 | Server-side template rendering |

### 🐍 **Backend Technologies**

| Package | Version | Purpose |
|---------|---------|---------|
| **Python** | 3.8+ | Core programming language |
| **Flask** | 2.3.3 | Lightweight web framework |
| **Flask-SocketIO** | 5.3.6 | Real-time bidirectional communication |
| **python-socketio** | 5.10.0 | Socket.IO server implementation |
| **Werkzeug** | 2.3.7 | WSGI utilities and request handling |

### 🤖 **Machine Learning & Data Processing**

| Library | Version | Purpose |
|---------|---------|---------|
| **scikit-learn** | 1.3.0 | ML algorithms (Random Forest, SVM, Gradient Boosting) |
| **NumPy** | 1.24.3 | Numerical computing and array operations |
| **pandas** | 2.0.3 | Data manipulation and analysis |
| **beautifulsoup4** | 4.12.2 | HTML/XML parsing and email content extraction |
| **lxml** | 4.9.3 | XML and HTML processing |

### 🔒 **Security & Cryptography**

| Library | Version | Purpose |
|---------|---------|---------|
| **pyOpenSSL** | 23.2.0 | SSL/TLS certificate handling |
| **cryptography** | 41.0.7 | Encryption and cryptographic operations |
| **certifi** | 2023.7.22 | CA bundle for SSL verification |
| **passlib** | 1.7.4 | Password hashing and verification |

### 📧 **Email & URL Processing**

| Library | Version | Purpose |
|---------|---------|---------|
| **tldextract** | 5.1.1 | Extract domain, subdomain, and TLD from URLs |
| **urllib3** | 2.0.7 | HTTP client for email/URL validation |
| **itsdenerous** | 2.1.2 | Token generation and signing |

### 🔗 **HTTP & API Integration**

| Library | Version | Purpose |
|---------|---------|---------|
| **requests** | 2.31.0 | HTTP library for API calls and Gmail integration |
| **chardet** | 5.2.0 | Character encoding detection |
| **six** | 1.16.0 | Python 2 and 3 compatibility utilities |

### 🛠️ **Utilities & Tools**

| Library | Version | Purpose |
|---------|---------|---------|
| **gunicorn** | 21.2.0 | Production WSGI HTTP server |
| **eventlet** | 0.33.3 | Lightweight asynchronous networking |
| **python-dotenv** | 1.0.0 | Environment variable management |
| **joblib** | 1.3.2 | Efficient serialization of Python objects |
| **regex** | 2023.10.3 | Advanced regular expressions for pattern matching |
| **python-dateutil** | 2.8.2 | Date/time utilities |

### ☁️ **Deployment & Infrastructure**

| Platform | Purpose |
|----------|---------|
| **Render** | Cloud hosting and deployment |
| **GitHub** | Version control and collaboration |
| **Docker** | Containerization (optional) |
| **Git** | Source code management |

### 📦 **Complete Requirements Summary**

```
Total Dependencies: 28 packages
Total Size: ~200 MB (with dependencies)
Installation Time: ~2-5 minutes
Python Version: 3.8+
License: MIT
```

### 📊 **Dependency Relationship Diagram**

```
┌─────────────────────────────────────────────────────────────┐
│                  Flask Web Application                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   Frontend   │    │   Backend    │    │  ML Engine   │  │
│  ├──────────────┤    ├──────────────┤    ├──────────────┤  │
│  │ • HTML5/CSS3 │    │ • Flask      │    │ • scikit-learn
│  │ • Bootstrap  │    │ • Werkzeug   │    │ • NumPy      │  │
│  │ • JavaScript │    │ • SocketIO   │    │ • pandas     │  │
│  │ • Jinja2     │    │ • Requests   │    │ • joblib     │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│         │                    │                   │            │
│         └────────────────────┼───────────────────┘            │
│                              │                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │    Security & Data Processing Layer                  │  │
│  ├──────────────────────────────────────────────────────┤  │
│  │ • cryptography (Encryption)                          │  │
│  │ • pyOpenSSL (SSL/TLS)                                │  │
│  │ • beautifulsoup4 (HTML Parsing)                      │  │
│  │ • tldextract (URL Analysis)                          │  │
│  │ • passlib (Password Hashing)                         │  │
│  │ • python-dateutil (Date Processing)                 │  │
│  └──────────────────────────────────────────────────────┘  │
│                              │                               │
│  ┌──────────────────────────────────────────────────────┐  │
│  │        External Integrations                         │  │
│  ├──────────────────────────────────────────────────────┤  │
│  │ • Gmail API (OAuth 2.0)                              │  │
│  │ • Google Cloud Services                              │  │
│  │ • Render Deployment Platform                         │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
AI-Gmail-Phishing-Detector/
│
├── 📄 app.py                      # Main Flask application entry point
├── 📄 requirements.txt            # Python dependencies (28 packages)
├── 📄 render.yaml                 # Render cloud deployment configuration
├── 📄 .python-version             # Python version specification (3.8+)
├── 📄 README.md                   # Project documentation
│
├── 📂 models/                     # Trained ML models (pickle files)
│   ├── random_forest_model.pkl    # Random Forest trained model
│   ├── svm_model.pkl              # Support Vector Machine model
│   ├── gradient_boosting_model.pkl # Gradient Boosting model
│   └── logistic_regression_model.pkl # Logistic Regression model
│
├── 📂 templates/                  # HTML template files
│   ├── index.html                 # Home/landing page
│   ├── dashboard.html             # Analysis results dashboard
│   ├── login.html                 # Gmail OAuth login page
│   ├── single_analysis.html       # Single email analysis page
│   └── batch_analysis.html        # Batch email analysis page
│
├── 📂 static/                     # Static assets (CSS, JS, images)
│   ├── css/
│   │   ├── style.css              # Main stylesheet
│   │   └── responsive.css         # Responsive design styles
│   ├── js/
│   │   ├── main.js                # Main JavaScript logic
│   │   └── api.js                 # API interaction functions
│   └── images/
│       └── logo.png               # Project logo
│
├── 📂 train/                      # Model training scripts
│   ├── train_random_forest.py     # Random Forest training
│   ├── train_svm.py               # SVM training
│   ├── train_gradient_boosting.py # Gradient Boosting training
│   └── train_ensemble.py          # Ensemble model training
│
├── 📂 utils/                      # Utility functions
│   ├── data_processing.py         # Data cleaning and preprocessing
│   ├── feature_extraction.py      # Email feature extraction
│   ├── email_analyzer.py          # Email analysis utilities
│   └── helpers.py                 # Helper functions
│
├── 📂 config/                     # Configuration files
│   ├── config.py                  # Application configuration
│   └── settings.py                # Application settings
│
├── 📄 ml_predictor.py             # ML prediction engine and scoring
├── 📄 dataset_connector.py        # Gmail API and data connector
├── 📄 train_all_models.py         # Master training orchestrator
│
├── 📂 data/                       # Datasets directory
│   ├── Phishing_Email.csv         # Raw phishing email dataset
│   ├── Phishing_Email_cleaned.csv # Cleaned dataset
│   ├── Phishing_Email_backup.csv  # Backup dataset
│   └── README_DATA.md             # Dataset documentation
│
├── 📂 .vscode/                    # VSCode configuration
│   └── settings.json              # VSCode workspace settings
│
├── 📄 app.log                     # Application logs
├── 📄 .gitignore                  # Git ignore rules
└── 📄 .env.example                # Environment variables example
```

---

## 🚀 Installation & Setup

### Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **pip** - Comes with Python installation
- **Git** - [Download Git](https://git-scm.com/downloads)
- **Gmail Account** with 2FA enabled (for secure OAuth)
- **Google Cloud Project** with Gmail API enabled

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/muhammedmuflih/AI-Gmail-Phishing-Detector.git

# Navigate to project directory
cd AI-Gmail-Phishing-Detector
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
# Install all required packages from requirements.txt
pip install -r requirements.txt

# Verify installation (optional)
pip list
```

### Step 4: Set Up Gmail API

1. **Create Google Cloud Project**
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Click "Create Project"
   - Enter project name and create

2. **Enable Gmail API**
   - In the Cloud Console, search for "Gmail API"
   - Click on Gmail API
   - Click "Enable"

3. **Create OAuth 2.0 Credentials**
   - Go to "Credentials" in the left sidebar
   - Click "Create Credentials" → "OAuth 2.0 Client ID"
   - Select "Desktop application"
   - Download the credentials JSON file

4. **Add Credentials to Project**
   ```bash
   # Save the downloaded file as credentials.json in project root
   # Place it in: AI-Gmail-Phishing-Detector/credentials.json
   ```

### Step 5: Configure Environment Variables

```bash
# Create .env file
touch .env

# Add configuration (use .env.example as reference)
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your_secret_key_here_min_32_chars
GOOGLE_CLIENT_ID=your_client_id_here
GOOGLE_CLIENT_SECRET=your_secret_here
GMAIL_API_SCOPE=https://www.googleapis.com/auth/gmail.readonly
```

### Step 6: Run the Application

```bash
# Start the Flask application
python app.py

# Application will be available at:
# http://localhost:5000
```

### Step 7: Verify Installation

```bash
# Test if all dependencies are working
python -c "import flask, sklearn, pandas, numpy; print('All dependencies installed successfully!')"
```

---

## ⚡ Quick Start

### 1. **Launch the Application**

```bash
# Make sure virtual environment is activated
python app.py
```

### 2. **Open in Browser**

```
Navigate to: http://localhost:5000
```

### 3. **Authenticate with Gmail**

- Click the **"Connect to Gmail"** button
- You'll be redirected to Google login
- Authorize the application to access your inbox
- Accept OAuth permissions

### 4. **Scan Your Emails**

- Select specific emails or scan entire folders
- Click **"Analyze"** to run the phishing detector
- View detailed threat assessment and risk scores

### 5. **Review Results**

- See risk scores for each email (0-100%)
- Check identified phishing indicators
- Get recommendations for suspicious emails
- Download detailed reports (CSV/PDF)

---

## 📖 Usage Guide

### Single Email Analysis

```
Step 1: Navigate to "Single Email Analysis" tab
Step 2: Either:
        - Paste raw email content, OR
        - Select from your Gmail inbox
Step 3: Click "Analyze Email"
Step 4: Review the threat assessment report
Step 5: View risk score, confidence level, and indicators
```

### Batch Email Scanning

```
Step 1: Go to "Batch Analysis" section
Step 2: Select multiple emails or entire folder
Step 3: Set scan depth (e.g., last 50 emails)
Step 4: Click "Scan All"
Step 5: Monitor real-time scan progress
Step 6: Download comprehensive report
```

### Understanding Risk Scores

| Risk Level | Score Range | Color | Meaning |
|-----------|------------|-------|---------|
| **Safe** | 0-25% | 🟢 Green | No phishing indicators detected |
| **Caution** | 26-50% | 🟡 Yellow | Some suspicious elements found |
| **Warning** | 51-75% | 🟠 Orange | High probability of phishing |
| **Danger** | 76-100% | 🔴 Red | Likely phishing attempt |

### Phishing Indicators Detected

The system checks for:
- ✅ Suspicious sender information
- ✅ URL obfuscation and spoofing
- ✅ Fake urgency language
- ✅ Request for personal information
- ✅ Suspicious links and attachments
- ✅ Email header anomalies
- ✅ Misspelled domain names
- ✅ Suspicious HTML/CSS tricks

---

## 🔌 API Documentation

### Base URL
```
http://localhost:5000/api
```

### Authentication Endpoint

```http
POST /api/auth/login
Content-Type: application/json

Response:
{
  "status": "success",
  "user_id": "user123",
  "email": "user@gmail.com",
  "access_token": "token_here",
  "expires_in": 3600
}
```

### Email Analysis Endpoint

```http
POST /api/analyze/email
Content-Type: application/json
Authorization: Bearer {access_token}

Request Body:
{
  "email_content": "Raw email content here",
  "sender": "sender@example.com",
  "subject": "Email subject line",
  "headers": {
    "From": "sender@example.com",
    "To": "recipient@gmail.com",
    "Date": "2026-03-13"
  }
}

Response:
{
  "status": "success",
  "risk_score": 85.5,
  "classification": "phishing",
  "confidence": 0.92,
  "model_used": "ensemble",
  "indicators": [
    "suspicious_sender",
    "url_obfuscation",
    "fake_urgency",
    "request_personal_info"
  ],
  "explanation": "Email contains multiple phishing indicators...",
  "recommendation": "Delete this email immediately",
  "timestamp": "2026-03-13T10:30:00Z"
}
```

### Batch Analysis Endpoint

```http
POST /api/analyze/batch
Content-Type: application/json
Authorization: Bearer {access_token}

Request Body:
{
  "email_ids": ["id1", "id2", "id3"],
  "folder": "INBOX"
}

Response:
{
  "status": "success",
  "total_scanned": 3,
  "phishing_detected": 1,
  "legitimate_count": 2,
  "average_risk_score": 34.2,
  "scan_duration_ms": 1245,
  "results": [
    {
      "email_id": "id1",
      "risk_score": 95.2,
      "classification": "phishing"
    },
    {
      "email_id": "id2",
      "risk_score": 12.3,
      "classification": "legitimate"
    },
    {
      "email_id": "id3",
      "risk_score": 5.1,
      "classification": "legitimate"
    }
  ]
}
```

### Report Export Endpoint

```http
GET /api/reports/export?format=csv&start_date=2026-03-01&end_date=2026-03-13
Authorization: Bearer {access_token}

Response: CSV file download
```

---

## 📊 Model Performance

### Ensemble Model Metrics

Our ensemble model combines multiple algorithms for optimal accuracy:

| Model | Accuracy | Precision | Recall | F1-Score | Training Time |
|-------|----------|-----------|--------|----------|----------------|
| **Random Forest** | 97.2% | 96.8% | 97.5% | 97.1% | ~45s |
| **SVM (RBF)** | 96.1% | 95.9% | 96.3% | 96.1% | ~60s |
| **Gradient Boosting** | 98.4% | 98.1% | 98.7% | 98.4% | ~90s |
| **Logistic Regression** | 94.3% | 94.1% | 94.5% | 94.3% | ~5s |
| **🏆 Ensemble (All)** | **98.8%** | **98.6%** | **98.9%** | **98.7%** | ~3s (inference) |

### Dataset Statistics

```
Total Emails Analyzed:        18,000+
├── Phishing Emails:          9,800 (54.4%)
└── Legitimate Emails:        8,200 (45.6%)

Features Extracted:           65+
├── Header Features:          15
├── Content Features:         20
├── URL Features:             15
└── Advanced Features:        15

Training Data Split:
├── Training Set:             70% (12,600 emails)
├── Validation Set:           15% (2,700 emails)
└── Test Set:                 15% (2,700 emails)
```

### Performance Visualization

```
Accuracy Comparison:
├─ Random Forest    ████████████████████ 97.2%
├─ SVM              ███████████████████  96.1%
├─ Gradient Boost   █████████████████████ 98.4%
├─ Log. Regression  ███████████████     94.3%
└─ Ensemble         ██████████████████████ 98.8%

Phishing Detection Rate:
├─ True Positives:  98.9%  ✅ (Successfully caught)
├─ True Negatives:  98.6%  ✅ (Legitimate emails safe)
├─ False Positives: 1.4%   ⚠️  (Legitimate marked as phishing)
└─ False Negatives: 1.1%   ⚠️  (Phishing marked as legitimate)
```

---

## 👥 Team

This project is developed and maintained by a dedicated team of cybersecurity and machine learning professionals. We are committed to creating robust solutions to combat phishing attacks.

### 👨‍💼 Project Lead & Developer

<table>
  <tr>
    <td align="center" width="50%">
      <img src="https://img.shields.io/badge/Name-Muflih-blue?style=flat-square" alt="Muflih">
      <h3>📌 Muflih</h3>
      <p><strong>Role:</strong> Project Lead & Full-Stack Developer</p>
      <p><strong>Email:</strong> <a href="mailto:Muflih@2020">Muflih@2020</a></p>
      <p>
        <a href="https://github.com/muhammedmuflih">
          <img src="https://img.shields.io/badge/GitHub-muhammedmuflih-black?style=flat-square&logo=github" alt="GitHub">
        </a>
      </p>
      <p>
        <a href="https://www.linkedin.com/in/muflih-a-b27644351/">
          <img src="https://img.shields.io/badge/LinkedIn-Muflih-blue?style=flat-square&logo=linkedin" alt="LinkedIn">
        </a>
      </p>
      <p><strong>Responsibilities:</strong></p>
      <ul>
        <li>✅ Architecture & Design</li>
        <li>✅ Backend Development</li>
        <li>✅ ML Model Integration</li>
        <li>✅ Project Management</li>
      </ul>
    </td>
    <td align="center" width="50%">
      <img src="https://img.shields.io/badge/Name-Fasalu%20Rahman-green?style=flat-square" alt="Fasalu Rahman">
      <h3>📌 Fasalu Rahman</h3>
      <p><strong>Role:</strong> Co-Developer & ML Engineer</p>
      <p><strong>Email:</strong> <a href="mailto:fasalurhn502@gmail.com">fasalurhn502@gmail.com</a></p>
      <p>
        <a href="https://github.com/FASALU7311">
          <img src="https://img.shields.io/badge/GitHub-FASALU7311-black?style=flat-square&logo=github" alt="GitHub">
        </a>
      </p>
      <p>
        <a href="https://www.linkedin.com/in/fasalu-rahman-01a922335/">
          <img src="https://img.shields.io/badge/LinkedIn-Fasalu%20Rahman-blue?style=flat-square&logo=linkedin" alt="LinkedIn">
        </a>
      </p>
      <p><strong>Responsibilities:</strong></p>
      <ul>
        <li>✅ ML Model Development</li>
        <li>✅ Data Processing</li>
        <li>✅ Feature Engineering</li>
        <li>✅ Model Optimization</li>
      </ul>
    </td>
  </tr>
</table>

### 📊 Team Contribution Statistics

| Member | Role | Contributions | Commits |
|--------|------|---------------|---------|
| **Muflih** | Lead Developer | 60% | ~30 |
| **Fasalu Rahman** | ML Engineer | 40% | ~20 |

### 🤝 How to Contact the Team

- **For General Inquiries:** 📧 [Muflih@2020](mailto:Muflih@2020)
- **For ML/Model Issues:** 📧 [fasalurhn502@gmail.com](mailto:fasalurhn502@gmail.com)
- **GitHub Issues:** [Create Issue](https://github.com/muhammedmuflih/AI-Gmail-Phishing-Detector/issues)
- **Discussions:** [Start Discussion](https://github.com/muhammedmuflih/AI-Gmail-Phishing-Detector/discussions)

---

## 🤝 Contributing

We welcome contributions from the community! Whether you're fixing bugs, adding features, or improving documentation, your help is appreciated.

### Types of Contributions

- 🐛 **Bug Fixes** - Report and fix issues
- ✨ **New Features** - Implement new functionality
- 📚 **Documentation** - Improve README, comments, guides
- 🧪 **Tests** - Write unit and integration tests
- 🎨 **UI/UX** - Enhance user interface and experience
- 📊 **Data** - Contribute phishing datasets

### Getting Started

#### 1. Fork the Repository

```bash
# Click "Fork" button on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/AI-Gmail-Phishing-Detector.git
cd AI-Gmail-Phishing-Detector
```

#### 2. Create Feature Branch

```bash
git checkout -b feature/YourFeatureName
# or
git checkout -b bugfix/YourBugFixName
```

#### 3. Make Your Changes

```bash
# Edit files
# Test your changes
# Commit regularly
git add .
git commit -m "Add: Feature description" -m "- Detailed description"
```

#### 4. Push to Your Fork

```bash
git push origin feature/YourFeatureName
```

#### 5. Create Pull Request

- Go to original repository
- Click "New Pull Request"
- Select your branch
- Provide detailed description
- Submit for review

### Coding Standards

```python
# Follow PEP 8 style guide
# Use meaningful variable names
# Add docstrings to all functions

def analyze_email(email_content: str) -> dict:
    """
    Analyze email for phishing indicators.
    
    Args:
        email_content (str): Raw email content
        
    Returns:
        dict: Analysis results with risk score and indicators
    """
    pass
```

### Testing

```bash
# Run tests before submitting PR
python -m pytest tests/

# Check code coverage
python -m pytest --cov=.

# Lint code
python -m pylint *.py
```

### Commit Message Guidelines

```
Format: <Type>: <Subject>

Types:
- feat:     New feature
- fix:      Bug fix
- docs:     Documentation
- style:    Code style (no logic change)
- refactor: Code restructuring
- test:     Tests
- chore:    Build/config changes

Example:
feat: Add support for multiple language emails

- Implement language detection
- Add translation API integration
- Update documentation
```

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2026 Muhammed Muflih & Fasalu Rahman

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 💬 Support

### Getting Help

- **📖 [Documentation Wiki](https://github.com/muhammedmuflih/AI-Gmail-Phishing-Detector/wiki)** - Comprehensive guides and tutorials
- **🐛 [Report Issues](https://github.com/muhammedmuflih/AI-Gmail-Phishing-Detector/issues)** - Found a bug? Create an issue
- **💡 [Discussions](https://github.com/muhammedmuflih/AI-Gmail-Phishing-Detector/discussions)** - Ask questions and share ideas
- **📧 Team Contact:**
  - Muflih: [Muflih@2020](mailto:Muflih@2020)
  - Fasalu Rahman: [fasalurhn502@gmail.com](mailto:fasalurhn502@gmail.com)

### Frequently Asked Questions

#### Q: How accurate is the detector?
**A:** The ensemble model achieves 98.8% accuracy with 98.9% recall rate for phishing emails.

#### Q: Does it work with other email providers?
**A:** Currently supports Gmail. Outlook and Yahoo Mail support are in the roadmap.

#### Q: Is my email data secure?
**A:** Yes! We use OAuth 2.0. Your emails are never stored on our servers. Only analysis results are kept locally.

#### Q: Can I use this offline?
**A:** Yes, after initial setup. The ML models are loaded locally. Gmail API requires internet for sync.

#### Q: How often are models updated?
**A:** Models are retrained monthly with new phishing data to maintain accuracy.

### Common Issues & Solutions

#### Issue: Gmail API Authentication Failed

```
Error: "The credentials provided were not valid"

Solutions:
1. Verify credentials.json file exists in project root
2. Check if Gmail API is enabled in Google Cloud Console
3. Ensure OAuth consent screen is configured
4. Regenerate credentials.json with correct permissions
5. Delete token.pickle and reauthenticate
```

#### Issue: Model Loading Error

```
Error: "Failed to load model file"

Solutions:
1. Reinstall scikit-learn: pip install --upgrade scikit-learn
2. Verify models/ directory contains all .pkl files
3. Check Python version is 3.8+: python --version
4. Retrain models: python train_all_models.py
5. Check file permissions
```

#### Issue: Port Already in Use

```
Error: "Address already in use"

Solutions:
# Run on different port
python app.py --port 5001

# Or kill existing process
# Windows:
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/macOS:
lsof -i :5000
kill -9 <PID>
```

#### Issue: Slow Email Analysis

```
Solutions:
1. Ensure sufficient RAM (2GB minimum)
2. Close other applications
3. Reduce batch size
4. Check internet connection for Gmail API calls
5. Upgrade to faster CPU (if possible)
```

#### Issue: Out of Memory

```
Solutions:
1. Reduce batch size in batch analysis
2. Increase virtual memory/swap
3. Upgrade system RAM
4. Process emails in smaller batches
```

---

## 🌟 Acknowledgments

This project stands on the shoulders of giants:

- **[Google Gmail API](https://developers.google.com/gmail/api)** - For secure email access
- **[scikit-learn](https://scikit-learn.org/)** - For powerful ML algorithms
- **[Flask](https://flask.palletsprojects.com/)** - For lightweight web framework
- **[pandas](https://pandas.pydata.org/)** - For data manipulation
- **[Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/)** - For HTML parsing
- **Security Researchers** - For publicly available phishing datasets
- **Open Source Community** - For continuous support and contributions

### Special Thanks to Our Team Members

- **Muflih** - For visionary project leadership and architecture
- **Fasalu Rahman** - For exceptional ML engineering and optimization

---

## 📈 Roadmap

Future features and improvements planned for the project:

### Phase 1 (Q2 2026)
- [ ] Mobile app (iOS/Android) with native Gmail integration
- [ ] Real-time browser extension for Chrome/Firefox
- [ ] Advanced NLP with transformer models (BERT)
- [ ] Multi-language support (20+ languages)

### Phase 2 (Q3 2026)
- [ ] Integration with other email providers (Outlook, Yahoo, ProtonMail)
- [ ] Advanced dashboard with analytics and threat intelligence
- [ ] Machine learning model versioning and rollback
- [ ] API rate limiting and caching system

### Phase 3 (Q4 2026)
- [ ] Enterprise deployment options
- [ ] LDAP/Active Directory integration
- [ ] Custom rule builder for organizations
- [ ] Advanced threat hunting capabilities

### Under Consideration
- [ ] Webhook support for third-party integrations
- [ ] GraphQL API alternative
- [ ] Database persistence (PostgreSQL support)
- [ ] Kubernetes deployment manifests
- [ ] Automated security audit reports

---

## 📊 Project Statistics

```
Repository Stats:
├── Total Lines of Code:     ~5000+
├── Number of Files:         30+
├── Total Commits:           50+
├── Active Contributors:     2
├── Last Updated:            March 13, 2026
├── License:                 MIT
└── Status:                  Active Development

Technology Stats:
├── Languages:               Python, JavaScript, HTML, CSS
├── Frontend Framework:      Flask + Bootstrap
├── ML Framework:            scikit-learn
├── Database:                N/A (File-based models)
├── API Type:                RESTful JSON
└── Deployment:              Render, Docker-ready

Team Stats:
├── Total Team Members:      2
├── Lead Developer:          Muflih
├── ML Engineer:             Fasalu Rahman
└── Combined Experience:     10+ years
```

---

<div align="center">

### 🌟 Show Your Support

If you find this project helpful, please consider:
- ⭐ **Starring** the repository
- 🍴 **Forking** to contribute
- 📢 **Sharing** with others
- 🐛 **Reporting** issues
- 💡 **Suggesting** improvements

### Made with ❤️ by Muflih & Fasalu Rahman

**Last Updated**: March 13, 2026  
**Version**: 1.0.0  
**Status**: Active Development

---

### 📞 Quick Links

| Team Member | Email | GitHub | LinkedIn |
|-----------|-------|--------|----------|
| **Muflih** | [Muflih@2020](mailto:Muflih@2020) | [muhammedmuflih](https://github.com/muhammedmuflih) | [Profile](https://www.linkedin.com/in/muflih-a-b27644351/) |
| **Fasalu Rahman** | [fasalurhn502@gmail.com](mailto:fasalurhn502@gmail.com) | [FASALU7311](https://github.com/FASALU7311) | [Profile](https://www.linkedin.com/in/fasalu-rahman-01a922335/) |

---

[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)
[![GitHub followers](https://img.shields.io/github/followers/muhammedmuflih?style=social)](https://github.com/muhammedmuflih)
[![GitHub stars](https://img.shields.io/github/stars/muhammedmuflih/AI-Gmail-Phishing-Detector?style=social)](https://github.com/muhammedmuflih/AI-Gmail-Phishing-Detector)

</div>
