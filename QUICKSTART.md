# 🚀 QUICK START GUIDE

## Get RealTicker Running in 5 Minutes!

---

## ⚡ Super Fast Setup

### Step 1: Backend (2 minutes)

```bash
cd backend
python -m venv venv
```

**Windows:**
```bash
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

**Mac/Linux:**
```bash
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

✅ **Backend ready:** http://localhost:8000

---

### Step 2: Frontend (2 minutes)

Open a **NEW terminal window:**

```bash
cd frontend
npm install
npm start
```

✅ **Frontend ready:** http://localhost:3000

---

### Step 3: Test (1 minute)

Open browser to: **http://localhost:3000**

You should see:
- ✅ 10 stocks appear instantly
- ✅ Click NVDA → See price chart
- ✅ AI analysis shows up

**Done! 🎉**

---

## 🎯 What You'll See

### Home Page
- Top 10 stocks ranked by growth
- NVDA at #1 with +156.78% growth
- Beautiful table with all details

### Stock Detail Page
- 6-month price chart
- AI Analysis:
  - Trend: Upward/Downward/Sideways
  - Risk Level: Low/Medium/High
  - Suggested Action with reasoning

---

## 💡 Quick Tips

**No API Keys Needed!**
- Uses mock data (no external APIs)
- Instant loading, no rate limits
- Perfect for demos

**Want AI Analysis?**
- Get free key: https://huggingface.co/settings/tokens
- Add to `backend/.env`:
  ```
  HUGGINGFACE_API_KEY=hf_your_key_here
  ```
- Restart backend

**Without API key:**
- Smart fallback analysis still works!

---

## 🐛 Problems?

### Backend not starting?
```bash
# Make sure you're in the virtual environment
# You should see (venv) in your terminal
```

### Frontend not loading?
```bash
# Check if backend is running first
# Visit: http://localhost:8000
```

### Stocks not showing?
```bash
# Press F12 in browser
# Check console for errors
# Make sure both servers are running
```

---

## 📁 File Structure Quick Reference

```
realticker-updated/
├── backend/
│   ├── main.py          ← Start here: python main.py
│   └── requirements.txt
│
└── frontend/
    ├── src/
    │   ├── App.jsx
    │   ├── components/
    │   └── pages/
    └── package.json     ← Start here: npm install
```

---

## ✅ Verification Checklist

Before testing, make sure:
- [ ] Backend terminal shows "Uvicorn running on http://0.0.0.0:8000"
- [ ] Frontend terminal shows "Compiled successfully!"
- [ ] Browser opened to http://localhost:3000
- [ ] No red errors in either terminal

---

## 🎊 You're All Set!

Your RealTicker app is now running with:
- ✅ Top 10 stocks
- ✅ 6-month charts
- ✅ AI analysis
- ✅ Beautiful UI

**Ready for your hackathon submission!** 🏆

---

## 🔄 To Run Again Later

```bash
# Terminal 1 - Backend
cd backend
venv\Scripts\activate    # Windows
# source venv/bin/activate  # Mac/Linux
python main.py

# Terminal 2 - Frontend
cd frontend
npm start
```

That's it! 🚀
