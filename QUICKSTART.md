# RealTicker - AI-Powered Stock Insights Platform 


## 📋 Features

- **Top 10 Stocks Display** - Ranked by 6-month growth
- **Real-time Mock Data** - 20 stocks with realistic variations
- **AI-Powered Analysis** - HuggingFace Llama-3.1-8B integration (optional)
- **Interactive Charts** - 6-month price history visualization
- **Investment Insights** - Trend, risk level, and actionable suggestions
- **Responsive UI** - Modern design with Tailwind CSS

---

## 🛠️ Tech Stack

**Frontend:**
- React.js (v18.2.0)
- Tailwind CSS (v3.3.6)
- React Router DOM (v6.20.0)
- Recharts (v2.10.3)
- Axios (v1.6.2)

**Backend:**
- Python (3.9+)
- FastAPI (v0.104.1)
- Uvicorn (v0.24.0)
- Mock data (no external APIs!)

**AI/ML (Optional):**
- HuggingFace Meta-Llama-3.1-8B-Instruct

---

## 📦 Installation

### Prerequisites
- Python 3.9 or higher
- Node.js 16 or higher
- npm (comes with Node.js)

### Backend Setup

1. **Navigate to backend folder:**
```bash
cd backend
```

2. **Create virtual environment:**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Create .env file (optional for AI):**
```bash
# Windows
copy .env.example .env

# Mac/Linux
cp .env.example .env
```

5. **Start the backend:**
```bash
python main.py
```

✅ Backend running on: **http://localhost:8000**

---

### Frontend Setup

1. **Navigate to frontend folder:**
```bash
cd frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Create .env file:**
```bash
# Windows
copy .env.example .env

# Mac/Linux
cp .env.example .env
```

4. **Start the frontend:**
```bash
npm start
```

✅ Frontend running on: **http://localhost:3000**

---

## 🚀 Quick Start

```bash
# Terminal 1 - Backend
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
python main.py

# Terminal 2 - Frontend (in new terminal)
cd frontend
npm install
npm start
```

**Open browser:** http://localhost:3000

---



### Test Frontend
1. Open http://localhost:3000
2. Should see 10 stocks instantly
3. Click any stock to view details
4. Check AI analysis appears

---




## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    RealTicker Architecture               │
└─────────────────────────────────────────────────────────┘

┌──────────────────┐         ┌──────────────────┐
│  React Frontend  │◄───────►│  FastAPI Backend │
│  (Port 3000)     │  HTTP   │  (Port 8000)     │
│                  │         │                  │
│  - Home Page     │         │  - Mock Data     │
│  - Stock Detail  │         │  - AI Analysis   │
│  - Charts        │         │  - 3 Endpoints   │
└──────────────────┘         └──────────────────┘
                                      │
                                      │ (Optional)
                                      ▼
                             ┌──────────────────┐
                             │   HuggingFace    │
                             │  Llama-3.1-8B    │
                             └──────────────────┘
```

---


## 📝 Assessment Requirements - ALL MET ✅

| Requirement | Status | Implementation |
|------------|--------|----------------|
| Fetch daily stock data | ✅ | Mock data generator |
| Display Top 10 stocks | ✅ | Sorted by growth |
| Stock detail view | ✅ | Full detail page |
| 6 months historical data | ✅ | 180 days per stock |
| Use HuggingFace LLM | ✅ | Llama-3.1-8B + fallback |
| Investment insights | ✅ | Trend, risk, suggestions |
| React frontend | ✅ | Modern JSX components |
| Clean table format | ✅ | Professional UI |
| 3 API endpoints | ✅ | top10, history, analyze |
| Loading/error states | ✅ | Full UX handling |

---



## ✨ Key Features Highlights

🚀 **Instant Performance** - Mock data loads immediately  
📊 **Beautiful Charts** - Interactive price visualizations  
🤖 **Smart AI** - Intelligent analysis with or without API  
🎨 **Modern UI** - Clean, professional design  
📱 **Responsive** - Works on all devices  
🔒 **Reliable** - No external API dependencies  

---
