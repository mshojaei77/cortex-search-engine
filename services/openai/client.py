"""
OpenAI Client Service for AI-Powered Search Enhancement

This service provides intelligent search result processing using OpenAI's function calling capabilities.
It enhances search results with AI-powered analysis, summarization, and context.
"""

import os
import json
import asyncio
import aiohttp
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from openai import AsyncOpenAI
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SearchResult:
    """Represents a search result from SearXNG"""
    title: str
    url: str
    content: str
    engine: str
    score: float = 0.0
    category: str = "general"

@dataclass
class AIEnhancedResult:
    """Represents an AI-enhanced search result"""
    original_result: SearchResult
    ai_summary: str
    relevance_score: float
    key_points: List[str]
    sentiment: str = "neutral"

class OpenAISearchService:
    """
    AI-powered search enhancement service using OpenAI function calling.
    
    This service provides:
    - Search result analysis and summarization
    - Relevance scoring
    - Key point extraction
    - Query enhancement suggestions
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the OpenAI service"""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
        
        self.client = AsyncOpenAI(api_key=self.api_key)
        self.model = "gpt-4o-mini"  # Using cost-effective model for search enhancement
        
        # Function definitions for OpenAI function calling
        self.search_functions = [
            {
                "type": "function",
                "function": {
                    "name": "analyze_search_results",
                    "description": "Analyze and enhance search results with AI insights",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The original search query"
                            },
                            "results": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "title": {"type": "string"},
                                        "content": {"type": "string"},
                                        "url": {"type": "string"}
                                    }
                                },
                                "description": "Array of search results to analyze"
                            },
                            "enhancement_type": {
                                "type": "string",
                                "enum": ["summarize", "extract_key_points", "score_relevance", "all"],
                                "description": "Type of enhancement to apply"
                            }
                        },
                        "required": ["query", "results", "enhancement_type"],
                        "additionalProperties": False
                    },
                    "strict": True
                }
            },
            {
                "type": "function", 
                "function": {
                    "name": "suggest_query_improvements",
                    "description": "Suggest improvements to search queries for better results",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "original_query": {
                                "type": "string",
                                "description": "The original search query"
                            },
                            "context": {
                                "type": "string", 
                                "description": "Additional context about what the user is looking for"
                            }
                        },
                        "required": ["original_query"],
                        "additionalProperties": False
                    },
                    "strict": True
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "extract_search_intent",
                    "description": "Extract and classify search intent from user queries",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "The search query to analyze"
                            }
                        },
                        "required": ["query"],
                        "additionalProperties": False
                    },
                    "strict": True
                }
            }
        ]

    async def enhance_search_results(
        self, 
        query: str, 
        results: List[SearchResult],
        enhancement_type: str = "all"
    ) -> List[AIEnhancedResult]:
        """
        Enhance search results using OpenAI function calling
        
        Args:
            query: The original search query
            results: List of search results from SearXNG
            enhancement_type: Type of enhancement to apply
            
        Returns:
            List of AI-enhanced search results
        """
        try:
            # Prepare results data for AI analysis
            results_data = [
                {
                    "title": result.title,
                    "content": result.content[:500],  # Limit content for API efficiency
                    "url": result.url
                }
                for result in results[:5]  # Limit to top 5 results for cost efficiency
            ]
            
            # Create the AI conversation
            messages = [
                {
                    "role": "developer",
                    "content": (
                        "You are an AI assistant that enhances search results. "
                        "Analyze the provided search results and provide intelligent insights. "
                        "Focus on relevance, accuracy, and usefulness to the user's query. "
                        "Always use the provided functions to structure your analysis."
                    )
                },
                {
                    "role": "user", 
                    "content": f"Please analyze these search results for the query: '{query}'"
                }
            ]
            
            # Call OpenAI with function calling
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.search_functions,
                tool_choice="auto",
                temperature=0.3  # Lower temperature for more consistent analysis
            )
            
            enhanced_results = []
            
            # Process function calls if any
            if response.choices[0].message.tool_calls:
                for tool_call in response.choices[0].message.tool_calls:
                    if tool_call.function.name == "analyze_search_results":
                        # Execute the search results analysis
                        enhanced_results = await self._process_search_analysis(
                            query, results, json.loads(tool_call.function.arguments)
                        )
            else:
                # Fallback: create basic enhanced results
                enhanced_results = await self._create_basic_enhanced_results(query, results)
            
            return enhanced_results
            
        except Exception as e:
            logger.error(f"Error enhancing search results: {e}")
            # Return basic enhanced results as fallback
            return await self._create_basic_enhanced_results(query, results)

    async def suggest_query_improvements(self, query: str, context: str = "") -> List[str]:
        """
        Suggest improvements to search queries
        
        Args:
            query: Original search query
            context: Additional context
            
        Returns:
            List of suggested improved queries
        """
        try:
            messages = [
                {
                    "role": "developer",
                    "content": (
                        "You are a search query optimization expert. "
                        "Suggest better search queries that would yield more relevant results. "
                        "Focus on adding relevant keywords, fixing typos, and improving specificity."
                    )
                },
                {
                    "role": "user",
                    "content": f"Improve this search query: '{query}'" + (f" Context: {context}" if context else "")
                }
            ]
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.search_functions,
                tool_choice={"type": "function", "function": {"name": "suggest_query_improvements"}},
                temperature=0.7
            )
            
            # Process the suggestions
            suggestions = []
            if response.choices[0].message.tool_calls:
                for tool_call in response.choices[0].message.tool_calls:
                    if tool_call.function.name == "suggest_query_improvements":
                        # Extract suggestions from the function call
                        args = json.loads(tool_call.function.arguments)
                        suggestions = await self._generate_query_suggestions(args.get("original_query", query))
            
            return suggestions or [query]  # Return original query if no suggestions
            
        except Exception as e:
            logger.error(f"Error suggesting query improvements: {e}")
            return [query]

    async def extract_search_intent(self, query: str) -> Dict[str, Any]:
        """
        Extract search intent from user query
        
        Args:
            query: Search query to analyze
            
        Returns:
            Dictionary containing intent classification and metadata
        """
        try:
            messages = [
                {
                    "role": "developer", 
                    "content": (
                        "You are a search intent classifier. "
                        "Analyze user queries to determine their intent: "
                        "informational, navigational, transactional, or commercial. "
                        "Also identify the topic category and urgency level."
                    )
                },
                {
                    "role": "user",
                    "content": f"Analyze the search intent for: '{query}'"
                }
            ]
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.search_functions,
                tool_choice={"type": "function", "function": {"name": "extract_search_intent"}},
                temperature=0.2
            )
            
            intent_data = {
                "query": query,
                "intent_type": "informational",
                "category": "general",
                "urgency": "medium",
                "confidence": 0.8
            }
            
            if response.choices[0].message.tool_calls:
                for tool_call in response.choices[0].message.tool_calls:
                    if tool_call.function.name == "extract_search_intent":
                        # Process intent extraction results
                        intent_data = await self._process_intent_extraction(
                            json.loads(tool_call.function.arguments)
                        )
            
            return intent_data
            
        except Exception as e:
            logger.error(f"Error extracting search intent: {e}")
            return {
                "query": query,
                "intent_type": "informational", 
                "category": "general",
                "urgency": "medium",
                "confidence": 0.5
            }

    async def _process_search_analysis(
        self, 
        query: str, 
        results: List[SearchResult], 
        analysis_args: Dict[str, Any]
    ) -> List[AIEnhancedResult]:
        """Process the search analysis function call results"""
        enhanced_results = []
        
        for i, result in enumerate(results[:5]):  # Limit to 5 results
            # Generate AI summary and insights
            ai_summary = await self._generate_summary(result.content, query)
            key_points = await self._extract_key_points(result.content)
            relevance_score = await self._calculate_relevance_score(result, query)
            
            enhanced_result = AIEnhancedResult(
                original_result=result,
                ai_summary=ai_summary,
                relevance_score=relevance_score,
                key_points=key_points,
                sentiment="neutral"
            )
            enhanced_results.append(enhanced_result)
        
        return enhanced_results

    async def _create_basic_enhanced_results(
        self, 
        query: str, 
        results: List[SearchResult]
    ) -> List[AIEnhancedResult]:
        """Create basic enhanced results as fallback"""
        enhanced_results = []
        
        for result in results:
            enhanced_result = AIEnhancedResult(
                original_result=result,
                ai_summary=result.content[:200] + "..." if len(result.content) > 200 else result.content,
                relevance_score=0.5,  # Default score
                key_points=[result.title],
                sentiment="neutral"
            )
            enhanced_results.append(enhanced_result)
        
        return enhanced_results

    async def _generate_summary(self, content: str, query: str) -> str:
        """Generate AI summary of content"""
        try:
            prompt = f"Summarize this content in relation to the query '{query}': {content[:300]}"
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"Error generating summary: {e}")
            return content[:100] + "..."

    async def _extract_key_points(self, content: str) -> List[str]:
        """Extract key points from content"""
        try:
            prompt = f"Extract 3 key points from this content: {content[:300]}"
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=80,
                temperature=0.3
            )
            
            points = response.choices[0].message.content.strip().split('\n')
            return [point.strip('- ').strip() for point in points if point.strip()][:3]
        except Exception as e:
            logger.error(f"Error extracting key points: {e}")
            return [content[:50] + "..."]

    async def _calculate_relevance_score(self, result: SearchResult, query: str) -> float:
        """Calculate relevance score using simple heuristics"""
        try:
            query_words = query.lower().split()
            title_lower = result.title.lower()
            content_lower = result.content.lower()
            
            # Count query word matches
            title_matches = sum(1 for word in query_words if word in title_lower)
            content_matches = sum(1 for word in query_words if word in content_lower)
            
            # Calculate score (0.0 to 1.0)
            title_score = title_matches / len(query_words) * 0.6
            content_score = content_matches / len(query_words) * 0.4
            
            return min(1.0, title_score + content_score)
        except Exception:
            return 0.5

    async def _generate_query_suggestions(self, query: str) -> List[str]:
        """Generate query suggestions"""
        # Simple query improvement suggestions
        suggestions = [query]
        
        # Add quotes for exact phrases
        if ' ' in query and '"' not in query:
            suggestions.append(f'"{query}"')
        
        # Add common modifiers
        suggestions.extend([
            f"{query} tutorial",
            f"{query} guide", 
            f"{query} 2025",
            f"how to {query}",
            f"{query} best practices"
        ])
        
        return suggestions[:5]

    async def _process_intent_extraction(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Process intent extraction results"""
        query = args.get("query", "")
        
        # Simple intent classification
        intent_type = "informational"
        category = "general"
        urgency = "medium"
        
        # Basic keyword-based classification
        if any(word in query.lower() for word in ['buy', 'purchase', 'price', 'cost']):
            intent_type = "transactional"
        elif any(word in query.lower() for word in ['how to', 'tutorial', 'guide']):
            intent_type = "informational"
        elif any(word in query.lower() for word in ['login', 'website', 'official']):
            intent_type = "navigational"
        
        # Category classification
        if any(word in query.lower() for word in ['tech', 'programming', 'software']):
            category = "technology"
        elif any(word in query.lower() for word in ['health', 'medical', 'doctor']):
            category = "health"
        elif any(word in query.lower() for word in ['news', 'current', 'latest']):
            category = "news"
        
        return {
            "query": query,
            "intent_type": intent_type,
            "category": category, 
            "urgency": urgency,
            "confidence": 0.8
        }


if __name__ == "__main__":
    # Example usage and testing
    async def test_openai_service():
        """Test the OpenAI service"""
        try:
            service = OpenAISearchService()
            
            # Test search results
            test_results = [
                SearchResult(
                    title="Python Programming Guide",
                    url="https://example.com/python-guide",
                    content="Learn Python programming with this comprehensive guide. Covers basics to advanced topics.",
                    engine="test"
                ),
                SearchResult(
                    title="JavaScript Tutorial",
                    url="https://example.com/js-tutorial", 
                    content="Modern JavaScript tutorial covering ES6+ features and best practices.",
                    engine="test"
                )
            ]
            
            # Test enhancement
            enhanced = await service.enhance_search_results("python programming", test_results)
            print("Enhanced Results:", len(enhanced))
            
            # Test query suggestions
            suggestions = await service.suggest_query_improvements("python programming")
            print("Query Suggestions:", suggestions)
            
            # Test intent extraction
            intent = await service.extract_search_intent("how to learn python programming")
            print("Search Intent:", intent)
            
        except Exception as e:
            print(f"Test error: {e}")

    # Run tests if executed directly
    asyncio.run(test_openai_service()) 