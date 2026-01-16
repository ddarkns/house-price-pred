# 🏠 House Price Prediction - ML Full Stack Application

[![Live Demo](https://img.shields.io/badge/Live-Demo-green)](your-live-link)
[![Python](https://img.shields.io/badge/Python-3.9+-blue)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-blue)](https://fastapi.tiangolo.com)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.3+-green)](https://vuejs.org)
[![License](https://img.shields.io/badge/License-MIT-red)](LICENSE)

A  machine learning application that predicts house prices in Bangalore based on location, area(sqft), bedrooms, and bathrooms.

## ✨ Features
### **DataSet Used**
- [ model trained on Bangalore house price data](https://www.kaggle.com/code/mfaisalqureshi/banglore-house-price-prediction)

### 🤖 **Machine Learning Backend**
- **Scikit-learn** model trained on Bangalore house price data
- **Linear Regression** for accurate price predictions
- **Feature engineering** for location-based pricing
- **FastAPI** REST API with automatic documentation

### 🎨 **Modern Frontend**
- **Vue.js 3** with Composition API
- **Professional search** with fuzzy matching
- **Indian price formatting** (Lakhs/Crores)
- **Real-time predictions** with instant results
- **Responsive design** for all devices

### 🔍 **Smart Location Search**
- YouTube-style searchable dropdown
- Fuzzy matching with abbreviations
- Recent searches memory
- Keyboard navigation support
- Highlighted search results

## 📸 Screenshots

### 🏠 Prediction Interface
![Prediction Form](screenshots/form.png)

### 📊 Results Display
![Results](screenshots/results.png)

### 🔍 Smart Search
![Smart Search](screenshots/search.png)

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- Git

### Backend Setup
```bash
# Clone repository
git clone https://github.com/yourusername/house-price-predictor.git
cd house-price-predictor/backend

# Install dependencies
pip install -r requirements.txt

# Run backend
python app.py
# Server runs at http://localhost:8000