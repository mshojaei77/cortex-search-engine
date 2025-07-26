/**
 * Search API Service
 * 
 * Handles communication with SearXNG backend and AI enhancement services
 */

import axios, { type AxiosInstance, AxiosError } from 'axios';
import type { 
  SearchResult, 
  SearchResponse, 
  AIEnhancedResult, 
  SearchIntent, 
  QuerySuggestion,
  SearchFilters,
  SearchMetrics 
} from '../types/search';

export class SearchApiError extends Error {
  public statusCode?: number;
  public originalError?: Error;
  
  constructor(
    message: string,
    statusCode?: number,
    originalError?: Error
  ) {
    super(message);
    this.name = 'SearchApiError';
    this.statusCode = statusCode;
    this.originalError = originalError;
  }
}

class SearchApiService {
  private api: AxiosInstance;
  private baseUrl: string;

  constructor() {
    this.baseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8080';
    
    this.api = axios.create({
      baseURL: this.baseUrl,
      timeout: 30000, // 30 seconds timeout
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
    });

    // Add request interceptor for logging
    this.api.interceptors.request.use((config) => {
      console.log(`🔍 Search API Request: ${config.method?.toUpperCase()} ${config.url}`);
      return config;
    });

    // Add response interceptor for error handling
    this.api.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        const message = this.getErrorMessage(error);
        throw new SearchApiError(message, error.response?.status, error);
      }
    );
  }

  /**
   * Perform a search using SearXNG
   */
  async search(
    query: string, 
    filters: SearchFilters = {}
  ): Promise<{ results: SearchResult[], metrics: SearchMetrics }> {
    try {
      const startTime = Date.now();

      const params = {
        q: query,
        format: 'json',
        ...this.buildSearchParams(filters)
      };

      const response = await this.api.get<SearchResponse>('/search', { params });
      
      const queryTime = Date.now() - startTime;
      
      // Transform SearXNG response to our format
      const results = this.transformSearchResults(response.data.results || []);
      
      const metrics: SearchMetrics = {
        totalResults: results.length,
        queryTime,
        engines: [...new Set(results.map(r => r.engine))],
      };

      return { results, metrics };
    } catch (error) {
      console.error('Search failed:', error);
      if (error instanceof SearchApiError) {
        throw error;
      }
      throw new SearchApiError('Search request failed', undefined, error as Error);
    }
  }

  /**
   * Get search suggestions/autocomplete
   */
  async getSuggestions(query: string): Promise<QuerySuggestion[]> {
    try {
      // SearXNG autocomplete endpoint
      const response = await this.api.get('/autocompleter', {
        params: { q: query }
      });

      return (response.data || []).map((suggestion: string) => ({
        text: suggestion,
        type: 'autocomplete' as const,
        confidence: 0.8
      }));
    } catch (error) {
      console.warn('Failed to get suggestions:', error);
      return [];
    }
  }

  /**
   * Enhance search results with AI (if OpenAI is enabled)
   */
  async enhanceResults(
    query: string, 
    results: SearchResult[]
  ): Promise<AIEnhancedResult[]> {
    // Check if AI enhancement is enabled
    const aiEnabled = import.meta.env.VITE_OPENAI_ENABLED === 'true';
    if (!aiEnabled) {
      return this.createBasicEnhancedResults(results);
    }

    try {
      const startTime = Date.now();

      // For now, create mock enhanced results
      // In a real implementation, this would call your Python OpenAI service
      const enhancedResults = await this.mockAIEnhancement(query, results);
      
      const enhancementTime = Date.now() - startTime;
      console.log(`✨ AI Enhancement completed in ${enhancementTime}ms`);
      
      return enhancedResults;
    } catch (error) {
      console.warn('AI enhancement failed, falling back to basic results:', error);
      return this.createBasicEnhancedResults(results);
    }
  }

  /**
   * Extract search intent (mock implementation)
   */
  async extractIntent(query: string): Promise<SearchIntent> {
    // Mock intent extraction - in production, this would call your OpenAI service
    return {
      query,
      intentType: this.classifyIntent(query),
      category: this.classifyCategory(query),
      urgency: 'medium',
      confidence: 0.8
    };
  }

  /**
   * Get related search suggestions
   */
  async getRelatedQueries(query: string): Promise<string[]> {
    // Mock related queries - in production, this could use OpenAI or SearXNG data
    const relatedQueries = [
      `${query} tutorial`,
      `${query} guide`,
      `how to ${query}`,
      `${query} best practices`,
      `${query} 2025`
    ];

    return relatedQueries.slice(0, 3);
  }

  /**
   * Build search parameters from filters
   */
  private buildSearchParams(filters: SearchFilters): Record<string, any> {
    const params: Record<string, any> = {};

    if (filters.categories?.length) {
      params.categories = filters.categories.join(',');
    }

    if (filters.engines?.length) {
      params.engines = filters.engines.join(',');
    }

    if (filters.language) {
      params.language = filters.language;
    }

    if (filters.timeRange) {
      params.time_range = filters.timeRange;
    }

    if (filters.safeSearch !== undefined) {
      params.safesearch = filters.safeSearch;
    }

    return params;
  }

  /**
   * Transform SearXNG results to our format
   */
  private transformSearchResults(results: any[]): SearchResult[] {
    return results.map((result, index) => ({
      title: result.title || 'Untitled',
      url: result.url || '',
      content: result.content || result.snippet || '',
      engine: result.engine || 'unknown',
      score: result.score || (1 - index * 0.1), // Decrease score by position
      category: result.category || 'general'
    }));
  }

  /**
   * Create basic enhanced results as fallback
   */
  private createBasicEnhancedResults(results: SearchResult[]): AIEnhancedResult[] {
    return results.map(result => ({
      originalResult: result,
      aiSummary: this.extractSummary(result.content),
      relevanceScore: result.score || 0.5,
      keyPoints: this.extractKeyPoints(result.content),
      sentiment: 'neutral' as const
    }));
  }

  /**
   * Mock AI enhancement for demonstration
   */
  private async mockAIEnhancement(
    query: string, 
    results: SearchResult[]
  ): Promise<AIEnhancedResult[]> {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 1000));

    return results.map(result => ({
      originalResult: result,
      aiSummary: `AI-enhanced summary: ${this.extractSummary(result.content)} This content is highly relevant to "${query}".`,
      relevanceScore: Math.min(1, (result.score || 0.5) + 0.2), // Boost score slightly
      keyPoints: [
        ...this.extractKeyPoints(result.content),
        `Relates to: ${query}`,
        'AI-verified content'
      ],
      sentiment: this.analyzeSentiment(result.content)
    }));
  }

  /**
   * Extract summary from content
   */
  private extractSummary(content: string): string {
    const maxLength = 150;
    if (content.length <= maxLength) return content;
    
    const truncated = content.substring(0, maxLength);
    const lastSpace = truncated.lastIndexOf(' ');
    return lastSpace > 0 ? truncated.substring(0, lastSpace) + '...' : truncated + '...';
  }

  /**
   * Extract key points from content
   */
  private extractKeyPoints(content: string): string[] {
    const sentences = content.split(/[.!?]+/).filter(s => s.trim().length > 20);
    return sentences.slice(0, 3).map(s => s.trim());
  }

  /**
   * Simple intent classification
   */
  private classifyIntent(query: string): SearchIntent['intentType'] {
    const lowerQuery = query.toLowerCase();
    
    if (lowerQuery.includes('buy') || lowerQuery.includes('purchase') || lowerQuery.includes('price')) {
      return 'transactional';
    }
    if (lowerQuery.includes('how to') || lowerQuery.includes('tutorial') || lowerQuery.includes('guide')) {
      return 'informational';
    }
    if (lowerQuery.includes('login') || lowerQuery.includes('website') || lowerQuery.includes('official')) {
      return 'navigational';
    }
    return 'informational';
  }

  /**
   * Simple category classification
   */
  private classifyCategory(query: string): string {
    const lowerQuery = query.toLowerCase();
    
    if (lowerQuery.match(/(tech|programming|software|code)/)) return 'technology';
    if (lowerQuery.match(/(health|medical|doctor)/)) return 'health';
    if (lowerQuery.match(/(news|current|latest)/)) return 'news';
    if (lowerQuery.match(/(recipe|cooking|food)/)) return 'lifestyle';
    
    return 'general';
  }

  /**
   * Simple sentiment analysis
   */
  private analyzeSentiment(content: string): 'positive' | 'neutral' | 'negative' {
    const lowerContent = content.toLowerCase();
    const positiveWords = ['great', 'excellent', 'good', 'amazing', 'wonderful', 'best'];
    const negativeWords = ['bad', 'terrible', 'awful', 'worst', 'horrible', 'poor'];
    
    const positiveCount = positiveWords.filter(word => lowerContent.includes(word)).length;
    const negativeCount = negativeWords.filter(word => lowerContent.includes(word)).length;
    
    if (positiveCount > negativeCount) return 'positive';
    if (negativeCount > positiveCount) return 'negative';
    return 'neutral';
  }

  /**
   * Get error message from axios error
   */
  private getErrorMessage(error: AxiosError): string {
    if (error.response?.status === 404) {
      return 'Search service not available. Please check if SearXNG is running.';
    }
    if (error.response && error.response.status >= 500) {
      return 'Search service is experiencing issues. Please try again later.';
    }
    if (error.code === 'ECONNREFUSED') {
      return 'Cannot connect to search service. Please check your configuration.';
    }
    if (error.code === 'ECONNABORTED') {
      return 'Search request timed out. Please try again.';
    }
    return error.message || 'An unexpected error occurred during search.';
  }
}

// Export singleton instance
export const searchApi = new SearchApiService();
export default searchApi; 