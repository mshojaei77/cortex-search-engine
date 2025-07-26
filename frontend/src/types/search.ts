/**
 * Search result interfaces for the AI-powered search engine
 */

export interface SearchResult {
  title: string;
  url: string;
  content: string;
  engine: string;
  score?: number;
  category?: string;
}

export interface AIEnhancedResult {
  originalResult: SearchResult;
  aiSummary: string;
  relevanceScore: number;
  keyPoints: string[];
  sentiment?: 'positive' | 'neutral' | 'negative';
}

export interface SearchResponse {
  query: string;
  results: SearchResult[];
  suggestions?: string[];
  infoboxes?: Infobox[];
  answers?: Answer[];
  query_time?: number;
  number_of_results?: number;
}

export interface Infobox {
  engine: string;
  content: string;
  urls?: InfoboxUrl[];
  img_src?: string;
}

export interface InfoboxUrl {
  title: string;
  url: string;
}

export interface Answer {
  answer: string;
  url: string;
}

export interface SearchIntent {
  query: string;
  intentType: 'informational' | 'navigational' | 'transactional' | 'commercial';
  category: string;
  urgency: 'low' | 'medium' | 'high';
  confidence: number;
}

export interface QuerySuggestion {
  text: string;
  type: 'autocomplete' | 'related' | 'correction';
  confidence?: number;
}

export interface SearchFilters {
  engines?: string[];
  categories?: string[];
  language?: string;
  timeRange?: 'hour' | 'day' | 'week' | 'month' | 'year';
  safeSearch?: 0 | 1 | 2; // 0=off, 1=moderate, 2=strict
}

export interface SearchState {
  query: string;
  results: SearchResult[];
  enhancedResults: AIEnhancedResult[];
  isLoading: boolean;
  isEnhancing: boolean;
  error: string | null;
  suggestions: QuerySuggestion[];
  intent: SearchIntent | null;
  filters: SearchFilters;
  hasSearched: boolean;
}

export interface SearchMetrics {
  totalResults: number;
  queryTime: number;
  engines: string[];
  enhancementTime?: number;
}

export type SearchCategory = 
  | 'general' 
  | 'images' 
  | 'videos' 
  | 'news' 
  | 'music' 
  | 'it' 
  | 'science' 
  | 'files' 
  | 'social media';

export type SearchEngine = 
  | 'google' 
  | 'bing' 
  | 'duckduckgo' 
  | 'startpage' 
  | 'qwant' 
  | 'wikipedia' 
  | 'github' 
  | 'stackoverflow'; 