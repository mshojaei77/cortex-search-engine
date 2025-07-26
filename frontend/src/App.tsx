/**
 * Main App Component
 * 
 * AI-Powered Personal Search Engine
 * Combines SearXNG backend with OpenAI enhancements and modern React UI
 */

import React, { useState } from 'react';
import { Toaster, toast } from 'react-hot-toast';
import SearchBar from './components/SearchBar';
import SearchResults from './components/SearchResults';
import { searchApi, SearchApiError } from './services/searchApi';
import type { AIEnhancedResult } from './types/search';
import { Brain } from 'lucide-react';

const App: React.FC = () => {
  const [enhancedResults, setEnhancedResults] = useState<AIEnhancedResult[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);

  const handleSearch = async (query: string) => {
    setIsLoading(true);
    setHasSearched(true);
    setEnhancedResults([]);

    try {
      const { results } = await searchApi.search(query);
      if (results.length > 0) {
        const enhanced = await searchApi.enhanceResults(query, results);
        setEnhancedResults(enhanced);
      }
    } catch (error) {
      const errorMessage = error instanceof SearchApiError ? error.message : 'An unexpected error occurred.';
      toast.error(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      <main className="main-content">
        <header>
          <div className="logo">
            <Brain size={40} className="text-primary" />
            <h1>Cortex</h1>
          </div>
          <p>Your private, AI-powered answer engine.</p>
        </header>

        <SearchBar onSearch={handleSearch} isLoading={isLoading} />

        {hasSearched && (
          <section className="results-section">
            <SearchResults
              enhancedResults={enhancedResults}
              isLoading={isLoading}
            />
          </section>
        )}
      </main>
      <Toaster position="bottom-center" />
    </div>
  );
};

export default App;
