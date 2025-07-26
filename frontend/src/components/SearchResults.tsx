/**
 * SearchResults Component
 * 
 * Displays search results with AI enhancements, relevance scoring, and rich metadata
 */

import React from 'react';
import { ExternalLink, Sparkles } from 'lucide-react';
import type { AIEnhancedResult } from '../types/search';

interface SearchResultsProps {
  enhancedResults: AIEnhancedResult[];
  isLoading: boolean;
}

const SearchResults: React.FC<SearchResultsProps> = ({ enhancedResults, isLoading }) => {
  const getDomain = (url: string): string => {
    try {
      return new URL(url).hostname.replace('www.', '');
    } catch {
      return "Invalid URL";
    }
  };

  if (isLoading) {
    return (
      <div className="search-results">
        {Array.from({ length: 3 }).map((_, index) => (
          <div key={index} className="result-card loading-skeleton">
            <div className="skeleton-item skeleton-title"></div>
            <div className="skeleton-item skeleton-text"></div>
            <div className="skeleton-item skeleton-text skeleton-text-short"></div>
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="search-results">
      {enhancedResults.map((enhanced, index) => (
        <article key={`${enhanced.originalResult.url}-${index}`} className="result-card">
          <a
            href={enhanced.originalResult.url}
            target="_blank"
            rel="noopener noreferrer"
          >
            <h3>{enhanced.originalResult.title}</h3>
            <p className="domain">{getDomain(enhanced.originalResult.url)}</p>
          </a>
          <div className="summary">
            <Sparkles size={20} className="sparkle-icon" />
            <p>{enhanced.aiSummary}</p>
          </div>
          <div className="source-link">
            <a href={enhanced.originalResult.url} target="_blank" rel="noopener noreferrer">
              Visit Source <ExternalLink size={16} />
            </a>
          </div>
        </article>
      ))}
    </div>
  );
};

export default SearchResults; 