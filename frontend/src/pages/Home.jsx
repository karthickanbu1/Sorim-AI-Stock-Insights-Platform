import React, { useState, useEffect } from 'react';
import axios from 'axios';
import StockTable from '../components/StockTable';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const Home = () => {
  const [stocks, setStocks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [sortBy, setSortBy] = useState('growth');

  useEffect(() => {
    fetchTopStocks();
  }, [sortBy]);

  const fetchTopStocks = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await axios.get(`${API_BASE_URL}/api/stocks/top10?sort_by=${sortBy}`);
      setStocks(response.data.stocks);
    } catch (err) {
      setError('Failed to fetch stock data. Please try again later.');
      console.error('Error fetching stocks:', err);
    } finally {
      setLoading(false);
    }
  };

  const getSortLabel = () => {
    switch(sortBy) {
      case 'volume': return 'Highest Volume';
      case 'market_cap': return 'Market Cap';
      default: return '6-Month Growth';
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <h2 className="text-3xl font-bold text-gray-900 mb-2">
          Top 10 Stocks by {getSortLabel()}
        </h2>
        <p className="text-gray-600">
        </p>
        
        {/* Sorting Options */}
        <div className="mt-4 flex flex-wrap gap-2">
          <button
            onClick={() => setSortBy('growth')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              sortBy === 'growth'
                ? 'bg-blue-700 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            📈 Highest Growth
          </button>
          <button
            onClick={() => setSortBy('volume')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              sortBy === 'volume'
                ? 'bg-blue-700 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            📊 Highest Volume
          </button>
          <button
            onClick={() => setSortBy('market_cap')}
            className={`px-4 py-2 rounded-lg font-medium transition-colors ${
              sortBy === 'market_cap'
                ? 'bg-blue-700 text-white'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            💰 Market Cap
          </button>
        </div>
      </div>

      {error && (
        <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-6 rounded">
          <div className="flex">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-3">
              <p className="text-sm text-red-700">{error}</p>
            </div>
            <button 
              onClick={fetchTopStocks}
              className="ml-auto bg-red-100 hover:bg-red-200 text-red-800 px-3 py-1 rounded text-sm"
            >
              Retry
            </button>
          </div>
        </div>
      )}

      <StockTable stocks={stocks} loading={loading} sortBy={sortBy} />

      
    </div>
  );
};

export default Home;
