from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import requests
import os
from pydantic import BaseModel
import random
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="RealTicker API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# HuggingFace API configuration
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")
HUGGINGFACE_API_URL = os.getenv("HUGGINGFACE_API_URL", "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3.1-8B-Instruct")

# Mock stock data - Top 20 stocks
MOCK_STOCKS = [
    {"ticker": "NVDA", "company": "NVIDIA Corporation", "base_price": 875.40, "growth": 156.78, "volatility": 12.5, "base_volume": 95000000, "market_cap": 2158000000000},
    {"ticker": "META", "company": "Meta Platforms Inc", "base_price": 492.50, "growth": 89.45, "volatility": 15.2, "base_volume": 42000000, "market_cap": 1245000000000},
    {"ticker": "TSLA", "company": "Tesla, Inc.", "base_price": 248.50, "growth": 67.23, "volatility": 22.8, "base_volume": 125000000, "market_cap": 789000000000},
    {"ticker": "AMZN", "company": "Amazon.com Inc", "base_price": 178.30, "growth": 52.15, "volatility": 10.5, "base_volume": 68000000, "market_cap": 1856000000000},
    {"ticker": "GOOGL", "company": "Alphabet Inc Class A", "base_price": 142.80, "growth": 45.67, "volatility": 8.9, "base_volume": 35000000, "market_cap": 1789000000000},
    {"ticker": "MSFT", "company": "Microsoft Corporation", "base_price": 412.30, "growth": 38.92, "volatility": 7.2, "base_volume": 45000000, "market_cap": 3078000000000},
    {"ticker": "AAPL", "company": "Apple Inc.", "base_price": 185.40, "growth": 25.50, "volatility": 8.2, "base_volume": 78000000, "market_cap": 2891000000000},
    {"ticker": "AMD", "company": "Advanced Micro Devices", "base_price": 165.20, "growth": 78.34, "volatility": 18.5, "base_volume": 82000000, "market_cap": 267000000000},
    {"ticker": "NFLX", "company": "Netflix Inc", "base_price": 598.75, "growth": 42.18, "volatility": 16.3, "base_volume": 38000000, "market_cap": 259000000000},
    {"ticker": "V", "company": "Visa Inc", "base_price": 272.60, "growth": 18.45, "volatility": 6.8, "base_volume": 28000000, "market_cap": 567000000000},
    {"ticker": "MA", "company": "Mastercard Inc", "base_price": 458.90, "growth": 22.33, "volatility": 7.1, "base_volume": 25000000, "market_cap": 445000000000},
    {"ticker": "JPM", "company": "JPMorgan Chase & Co", "base_price": 198.45, "growth": 15.67, "volatility": 9.2, "base_volume": 32000000, "market_cap": 589000000000},
    {"ticker": "WMT", "company": "Walmart Inc", "base_price": 168.20, "growth": 12.89, "volatility": 5.4, "base_volume": 48000000, "market_cap": 478000000000},
    {"ticker": "JNJ", "company": "Johnson & Johnson", "base_price": 156.78, "growth": 8.23, "volatility": 4.8, "base_volume": 22000000, "market_cap": 389000000000},
    {"ticker": "PG", "company": "Procter & Gamble Co", "base_price": 164.55, "growth": 10.45, "volatility": 5.1, "base_volume": 26000000, "market_cap": 398000000000},
    {"ticker": "XOM", "company": "Exxon Mobil Corporation", "base_price": 112.34, "growth": -5.67, "volatility": 14.2, "base_volume": 55000000, "market_cap": 456000000000},
    {"ticker": "CVX", "company": "Chevron Corporation", "base_price": 156.89, "growth": -3.24, "volatility": 12.8, "base_volume": 42000000, "market_cap": 289000000000},
    {"ticker": "KO", "company": "The Coca-Cola Company", "base_price": 62.45, "growth": 6.78, "volatility": 4.2, "base_volume": 52000000, "market_cap": 268000000000},
    {"ticker": "BAC", "company": "Bank of America Corp", "base_price": 38.92, "growth": 14.56, "volatility": 11.3, "base_volume": 98000000, "market_cap": 312000000000},
    {"ticker": "HD", "company": "The Home Depot Inc", "base_price": 382.75, "growth": 19.88, "volatility": 8.7, "base_volume": 36000000, "market_cap": 389000000000},
]

class AnalyzeRequest(BaseModel):
    ticker: str

def generate_mock_current_data(stock_info):
    """Generate current price with small daily variation"""
    base_price = stock_info["base_price"]
    daily_change = random.uniform(-3.0, 3.0)  # Random daily change between -3% and +3%
    current_price = base_price * (1 + daily_change / 100)
    
    # Add realistic volume variation
    volume = int(stock_info["base_volume"] * random.uniform(0.8, 1.2))
    
    return {
        "ticker": stock_info["ticker"],
        "company_name": stock_info["company"],
        "current_price": round(current_price, 2),
        "daily_change": round(daily_change, 2),
        "volume": volume,
        "market_cap": stock_info["market_cap"],
        "growth_6m": stock_info["growth"]
    }

def generate_mock_historical_data(ticker: str, base_price: float, growth: float, volatility: float, months: int = 6):
    """Generate 6 months of realistic historical stock data"""
    days = months * 30
    historical_data = []
    
    # Calculate starting price based on growth
    end_price = base_price
    start_price = end_price / (1 + growth / 100)
    
    # Generate daily prices with realistic trends
    for i in range(days):
        date = datetime.now() - timedelta(days=days-i)
        
        # Calculate progress through the period (0 to 1)
        progress = i / days
        
        # Base price follows the growth trend
        trend_price = start_price + (end_price - start_price) * progress
        
        # Add volatility
        daily_volatility = random.gauss(0, volatility / 10)
        price = trend_price * (1 + daily_volatility / 100)
        
        # Generate OHLC data
        open_price = price * random.uniform(0.98, 1.02)
        high_price = max(open_price, price) * random.uniform(1.0, 1.02)
        low_price = min(open_price, price) * random.uniform(0.98, 1.0)
        close_price = price
        volume = random.randint(10000000, 150000000)
        
        historical_data.append({
            "date": date.strftime("%Y-%m-%d"),
            "open": round(open_price, 2),
            "high": round(high_price, 2),
            "low": round(low_price, 2),
            "close": round(close_price, 2),
            "volume": volume
        })
    
    return historical_data

def get_stock_by_ticker(ticker: str):
    """Get stock info by ticker"""
    for stock in MOCK_STOCKS:
        if stock["ticker"] == ticker.upper():
            return stock
    return None

@app.get("/")
def read_root():
    return {"message": "RealTicker API is running with mock data"}

@app.get("/api/stocks/top10")
def get_top10_stocks(sort_by: Optional[str] = Query("growth", description="Sort by: growth, volume, or market_cap")):
    """
    Get top 10 stocks based on sorting criteria
    
    Parameters:
    - sort_by: 'growth' (default), 'volume', or 'market_cap'
    """
    print(f"Generating top 10 stocks sorted by {sort_by}...")
    
    # Generate current data for all stocks
    stocks_data = []
    for stock in MOCK_STOCKS:
        stock_data = generate_mock_current_data(stock)
        stocks_data.append(stock_data)
    
    # Sort based on criteria
    if sort_by == "volume":
        stocks_data.sort(key=lambda x: x['volume'], reverse=True)
    elif sort_by == "market_cap":
        stocks_data.sort(key=lambda x: x['market_cap'], reverse=True)
    else:  # default to growth
        stocks_data.sort(key=lambda x: x['growth_6m'], reverse=True)
    
    # Return top 10
    return {
        "stocks": stocks_data[:10],
        "sorted_by": sort_by
    }

@app.get("/api/stocks/{ticker}/history")
def get_stock_history(ticker: str):
    """Get 6 months historical data for a stock"""
    ticker = ticker.upper()
    
    # Find stock info
    stock_info = get_stock_by_ticker(ticker)
    
    if not stock_info:
        raise HTTPException(status_code=404, detail=f"Stock {ticker} not found")
    
    print(f"Generating historical data for {ticker}...")
    
    # Generate historical data
    historical_data = generate_mock_historical_data(
        ticker,
        stock_info["base_price"],
        stock_info["growth"],
        stock_info["volatility"],
        6
    )
    
    return {
        "ticker": ticker,
        "company_name": stock_info["company"],
        "historical_data": historical_data
    }

@app.post("/api/stocks/{ticker}/analyze")
def analyze_stock(ticker: str):
    """Analyze stock using HuggingFace LLM or fallback"""
    ticker = ticker.upper()
    
    # Find stock info
    stock_info = get_stock_by_ticker(ticker)
    
    if not stock_info:
        raise HTTPException(status_code=404, detail=f"Stock {ticker} not found")
    
    print(f"Generating analysis for {ticker}...")
    
    # Get historical data
    historical_data = generate_mock_historical_data(
        ticker,
        stock_info["base_price"],
        stock_info["growth"],
        stock_info["volatility"],
        6
    )
    
    # Prepare price data for LLM
    prices = [item['close'] for item in historical_data]
    dates = [item['date'] for item in historical_data]
    
    # Calculate basic statistics
    start_price = prices[0]
    end_price = prices[-1]
    max_price = max(prices)
    min_price = min(prices)
    avg_price = sum(prices) / len(prices)
    price_change = stock_info["growth"]
    volatility_percent = stock_info["volatility"]
    
    # Create prompt for LLM
    prompt = f"""Analyze the following 6-month stock price data for {ticker}:

Start Date: {dates[0]}
End Date: {dates[-1]}
Starting Price: ${start_price:.2f}
Ending Price: ${end_price:.2f}
Highest Price: ${max_price:.2f}
Lowest Price: ${min_price:.2f}
Average Price: ${avg_price:.2f}
Price Change: {price_change:.2f}%
Volatility: {volatility_percent:.2f}%

Based on this data, provide:
1. Trend (Upward/Downward/Sideways)
2. Risk Level (Low/Medium/High)
3. Suggested Action (Long-term investment/Short-term watch/Avoid with reason)

Format your response as:
Trend: [your answer]
Risk Level: [your answer]
Suggested Action: [your answer]
Reasoning: [brief explanation]"""

    result = None
    
    try:
        # Call HuggingFace API only if key is provided
        if HUGGINGFACE_API_KEY and HUGGINGFACE_API_KEY != "your_huggingface_api_key_here":
            headers = {
                "Authorization": f"Bearer {HUGGINGFACE_API_KEY}"
            }
            
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 300,
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "return_full_text": False
                }
            }
            
            response = requests.post(
                HUGGINGFACE_API_URL,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                response_data = response.json()
                
                if isinstance(response_data, list) and len(response_data) > 0:
                    analysis_text = response_data[0].get('generated_text', '')
                else:
                    analysis_text = response_data.get('generated_text', '')
                
                # Parse the response
                lines = analysis_text.strip().split('\n')
                trend = "Sideways"
                risk_level = "Medium"
                suggested_action = "Short-term watch"
                reasoning = "Analysis based on historical data."
                
                for line in lines:
                    if 'Trend:' in line:
                        trend = line.split('Trend:')[1].strip()
                    elif 'Risk Level:' in line:
                        risk_level = line.split('Risk Level:')[1].strip()
                    elif 'Suggested Action:' in line:
                        suggested_action = line.split('Suggested Action:')[1].strip()
                    elif 'Reasoning:' in line:
                        reasoning = line.split('Reasoning:')[1].strip()
                
                result = {
                    "ticker": ticker,
                    "analysis": {
                        "trend": trend,
                        "risk_level": risk_level,
                        "suggested_action": suggested_action,
                        "reasoning": reasoning,
                        "price_change_6m": round(price_change, 2),
                        "volatility": round(volatility_percent, 2)
                    },
                    "disclaimer": "This is AI-generated analysis and not financial advice."
                }
        
    except Exception as e:
        print(f"Error calling HuggingFace API: {str(e)}")
    
    # Use fallback if LLM failed or no API key
    if not result:
        result = generate_fallback_analysis(ticker, price_change, volatility_percent)
    
    return result

def generate_fallback_analysis(ticker: str, price_change: float, volatility: float):
    """Generate basic analysis when LLM is unavailable"""
    
    # Determine trend
    if price_change > 10:
        trend = "Upward"
    elif price_change < -10:
        trend = "Downward"
    else:
        trend = "Sideways"
    
    # Determine risk level
    if volatility < 5:
        risk_level = "Low"
    elif volatility < 15:
        risk_level = "Medium"
    else:
        risk_level = "High"
    
    # Determine suggested action
    if price_change > 15 and volatility < 10:
        suggested_action = "Long-term investment - Strong upward trend with stable volatility"
    elif price_change > 0 and volatility < 15:
        suggested_action = "Long-term investment - Positive growth with manageable risk"
    elif price_change < -15:
        suggested_action = "Avoid - Significant downward trend indicates potential further losses"
    elif volatility > 20:
        suggested_action = "Short-term watch - High volatility suggests increased risk"
    else:
        suggested_action = "Short-term watch - Monitor for clearer trend signals"
    
    reasoning = f"Based on {price_change:.2f}% price change and {volatility:.2f}% volatility over 6 months. "
    
    if trend == "Upward":
        reasoning += "The stock shows positive momentum. "
    elif trend == "Downward":
        reasoning += "The stock shows negative momentum. "
    else:
        reasoning += "The stock shows mixed signals. "
    
    if risk_level == "High":
        reasoning += "High volatility indicates increased risk exposure."
    elif risk_level == "Low":
        reasoning += "Low volatility suggests stable performance."
    else:
        reasoning += "Moderate volatility suggests balanced risk-reward."
    
    return {
        "ticker": ticker,
        "analysis": {
            "trend": trend,
            "risk_level": risk_level,
            "suggested_action": suggested_action,
            "reasoning": reasoning,
            "price_change_6m": round(price_change, 2),
            "volatility": round(volatility, 2)
        },
        "disclaimer": "This is AI-generated analysis and not financial advice."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)