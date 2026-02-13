import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const StockDetail = () => {
  const { ticker } = useParams();
  const navigate = useNavigate();
  const [historicalData, setHistoricalData] = useState([]);
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(true);
  const [analyzing, setAnalyzing] = useState(false);
  const [error, setError] = useState(null);
  const [companyName, setCompanyName] = useState('');

  useEffect(() => {
    fetchStockData();
  }, [ticker]);

  const fetchStockData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Fetch historical data
      const historyResponse = await axios.get(`${API_BASE_URL}/api/stocks/${ticker}/history`);
      setHistoricalData(historyResponse.data.historical_data);
      setCompanyName(historyResponse.data.company_name);
      
      // Automatically trigger analysis
      analyzeStock();
    } catch (err) {
      setError('Failed to fetch stock data. Please try again.');
      console.error('Error fetching stock data:', err);
    } finally {
      setLoading(false);
    }
  };

  const analyzeStock = async () => {
    try {
      setAnalyzing(true);
      const response = await axios.post(`${API_BASE_URL}/api/stocks/${ticker}/analyze`);
      setAnalysis(response.data);
    } catch (err) {
      console.error('Error analyzing stock:', err);
      setError('Failed to generate AI analysis. Please try again.');
    } finally {
      setAnalyzing(false);
    }
  };

  const getTrendColor = (trend) => {
    if (trend.toLowerCase().includes('upward')) return 'text-green-600';
    if (trend.toLowerCase().includes('downward')) return 'text-red-600';
    return 'text-yellow-600';
  };

  const getRiskColor = (risk) => {
    if (risk.toLowerCase().includes('low')) return 'bg-green-100 text-green-800';
    if (risk.toLowerCase().includes('high')) return 'bg-red-100 text-red-800';
    return 'bg-yellow-100 text-yellow-800';
  };

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="bg-white rounded-lg shadow-md p-8">
          <div className="flex items-center justify-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-700"></div>
            <span className="ml-4 text-gray-600">Loading stock details...</span>
          </div>
        </div>
      </div>
    );
  }

  if (error && !historicalData.length) {
    return (
      <div className="container mx-auto px-4 py-8">
        <button 
          onClick={() => navigate('/')}
          className="mb-4 text-blue-700 hover:text-blue-900 flex items-center"
        >
          <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          Back to Home
        </button>
        <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded">
          <p className="text-red-700">{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Back Button */}
      <button 
        onClick={() => navigate('/')}
        className="mb-6 text-blue-700 hover:text-blue-900 flex items-center font-medium"
      >
        <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
        </svg>
        Back to Top 10
      </button>

      {/* Stock Header */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-4xl font-bold text-gray-900">{ticker}</h1>
            <p className="text-xl text-gray-600 mt-1">{companyName}</p>
          </div>
          <div className="text-right">
            {historicalData.length > 0 && (
              <>
                <div className="text-3xl font-bold text-gray-900">
                  ${historicalData[historicalData.length - 1].close}
                </div>
                <div className="text-sm text-gray-500 mt-1">
                  Last Updated: {historicalData[historicalData.length - 1].date}
                </div>
              </>
            )}
          </div>
        </div>
      </div>

      {/* Price Chart */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">6-Month Price History</h2>
        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={historicalData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey="date" 
              tick={{ fontSize: 12 }}
              angle={-45}
              textAnchor="end"
              height={80}
            />
            <YAxis 
              tick={{ fontSize: 12 }}
              domain={['auto', 'auto']}
            />
            <Tooltip />
            <Legend />
            <Line 
              type="monotone" 
              dataKey="close" 
              stroke="#1e40af" 
              strokeWidth={2}
              dot={false}
              name="Close Price"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* AI Analysis Section */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-2xl font-bold text-gray-900">AI-Powered Analysis</h2>
          {!analyzing && (
            <button
              onClick={analyzeStock}
              className="bg-blue-700 hover:bg-blue-800 text-white px-4 py-2 rounded-lg font-medium transition-colors"
            >
              Refresh Analysis
            </button>
          )}
        </div>

        {analyzing ? (
          <div className="flex items-center justify-center py-8">
            <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-700"></div>
            <span className="ml-4 text-gray-600">Analyzing with AI...</span>
          </div>
        ) : analysis ? (
          <div className="space-y-6">
            {/* Analysis Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {/* Trend */}
              <div className="bg-gray-50 rounded-lg p-4">
                <h3 className="text-sm font-medium text-gray-500 mb-2">Trend</h3>
                <p className={`text-2xl font-bold ${getTrendColor(analysis.analysis.trend)}`}>
                  {analysis.analysis.trend}
                </p>
              </div>

              {/* Risk Level */}
              <div className="bg-gray-50 rounded-lg p-4">
                <h3 className="text-sm font-medium text-gray-500 mb-2">Risk Level</h3>
                <span className={`inline-block px-3 py-1 rounded-full text-lg font-bold ${getRiskColor(analysis.analysis.risk_level)}`}>
                  {analysis.analysis.risk_level}
                </span>
              </div>

              {/* 6M Growth */}
              <div className="bg-gray-50 rounded-lg p-4">
                <h3 className="text-sm font-medium text-gray-500 mb-2">6-Month Growth</h3>
                <p className={`text-2xl font-bold ${analysis.analysis.price_change_6m >= 0 ? 'text-green-600' : 'text-red-600'}`}>
                  {analysis.analysis.price_change_6m >= 0 ? '+' : ''}{analysis.analysis.price_change_6m}%
                </p>
              </div>
            </div>

            {/* Suggested Action */}
            <div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded">
              <h3 className="text-lg font-bold text-gray-900 mb-2">Suggested Action</h3>
              <p className="text-gray-800">{analysis.analysis.suggested_action}</p>
            </div>

            {/* Reasoning */}
            <div className="bg-gray-50 rounded-lg p-4">
              <h3 className="text-lg font-bold text-gray-900 mb-2">Analysis Reasoning</h3>
              <p className="text-gray-700 leading-relaxed">{analysis.analysis.reasoning}</p>
            </div>

            {/* Volatility */}
            <div className="bg-gray-50 rounded-lg p-4">
              <h3 className="text-sm font-medium text-gray-500 mb-2">Volatility Index</h3>
              <p className="text-xl font-bold text-gray-900">{analysis.analysis.volatility}%</p>
            </div>

            {/* Disclaimer */}
            <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 rounded">
              <div className="flex">
                <div className="flex-shrink-0">
                  <svg className="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                  </svg>
                </div>
                <div className="ml-3">
                  <p className="text-sm text-yellow-700 font-medium">{analysis.disclaimer}</p>
                </div>
              </div>
            </div>
          </div>
        ) : (
          <div className="text-center py-8">
            <p className="text-gray-600">Click "Refresh Analysis" to generate AI insights</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default StockDetail;
