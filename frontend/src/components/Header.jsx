import React from 'react';
import { Link } from 'react-router-dom';

const Header = () => {
  return (
    <header className="bg-blue-700 text-white shadow-lg">
      <div className="container mx-auto px-4 py-6">
        <Link to="/" className="flex items-center space-x-2">
          <div className="flex items-center">
            <svg 
              className="w-8 h-8" 
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path 
                strokeLinecap="round" 
                strokeLinejoin="round" 
                strokeWidth={2} 
                d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" 
              />
            </svg>
            <h1 className="text-3xl font-bold ml-2">RealTicker</h1>
          </div>
        </Link>
      </div>
    </header>
  );
};

export default Header;
