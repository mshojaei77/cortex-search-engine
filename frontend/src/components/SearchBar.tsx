/**
 * SearchBar Component
 * 
 * A modern search interface with autocomplete, suggestions, and AI-powered enhancements
 */

import React, { useState } from 'react';
import { Search } from 'lucide-react';

interface SearchBarProps {
  onSearch: (query: string) => void;
  isLoading: boolean;
}

const SearchBar: React.FC<SearchBarProps> = ({ onSearch, isLoading }) => {
  const [query, setQuery] = useState('');

  const handleSearch = () => {
    if (query.trim()) {
      onSearch(query.trim());
    }
  };

  return (
    <div className="search-bar">
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
        placeholder="Ask me anything..."
        className="search-input"
        disabled={isLoading}
      />
      <button
        onClick={handleSearch}
        disabled={isLoading}
        className="search-button"
      >
        {isLoading ? (
          <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
        ) : (
          <Search size={20} />
        )}
      </button>
    </div>
  );
};

export default SearchBar; 