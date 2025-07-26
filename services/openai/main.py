"""
FastAPI server for OpenAI Search Enhancement Service

Provides HTTP endpoints for AI-powered search result enhancement using OpenAI function calling.
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import asyncio
import logging
import os
from datetime import datetime

from client import OpenAISearchService, SearchResult, AIEnhancedResult

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Search Enhancement Service",
    description="OpenAI-powered search result enhancement using function calling",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI service
openai_service = None

@app.on_event("startup")
async def startup_event():
    """Initialize the OpenAI service on startup"""
    global openai_service
    try:
        openai_service = OpenAISearchService()
        logger.info("✅ OpenAI Search Service initialized successfully")
    except Exception as e:
        logger.error(f"❌ Failed to initialize OpenAI service: {e}")
        # Continue without OpenAI service (graceful degradation)

# Request/Response models
class SearchResultRequest(BaseModel):
    title: str
    url: str
    content: str
    engine: str
    score: Optional[float] = 0.0
    category: Optional[str] = "general"

class EnhanceResultsRequest(BaseModel):
    query: str
    results: List[SearchResultRequest]
    enhancement_type: Optional[str] = "all"

class EnhancedResultResponse(BaseModel):
    original_result: SearchResultRequest
    ai_summary: str
    relevance_score: float
    key_points: List[str]
    sentiment: Optional[str] = "neutral"

class QuerySuggestionsRequest(BaseModel):
    query: str
    context: Optional[str] = ""

class SearchIntentRequest(BaseModel):
    query: str

class SearchIntentResponse(BaseModel):
    query: str
    intent_type: str
    category: str
    urgency: str
    confidence: float

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "ai-search-enhancement",
        "openai_available": openai_service is not None
    }

# Enhanced search results endpoint
@app.post("/enhance-results", response_model=List[EnhancedResultResponse])
async def enhance_search_results(request: EnhanceResultsRequest):
    """
    Enhance search results with AI insights
    """
    if not openai_service:
        raise HTTPException(
            status_code=503, 
            detail="OpenAI service not available. Please check your API key configuration."
        )
    
    try:
        # Convert request models to domain models
        search_results = [
            SearchResult(
                title=result.title,
                url=result.url,
                content=result.content,
                engine=result.engine,
                score=result.score or 0.0,
                category=result.category or "general"
            )
            for result in request.results
        ]
        
        # Enhance results using OpenAI
        enhanced_results = await openai_service.enhance_search_results(
            query=request.query,
            results=search_results,
            enhancement_type=request.enhancement_type
        )
        
        # Convert back to response models
        response_data = [
            EnhancedResultResponse(
                original_result=SearchResultRequest(
                    title=enhanced.original_result.title,
                    url=enhanced.original_result.url,
                    content=enhanced.original_result.content,
                    engine=enhanced.original_result.engine,
                    score=enhanced.original_result.score,
                    category=enhanced.original_result.category
                ),
                ai_summary=enhanced.ai_summary,
                relevance_score=enhanced.relevance_score,
                key_points=enhanced.key_points,
                sentiment=enhanced.sentiment
            )
            for enhanced in enhanced_results
        ]
        
        logger.info(f"✨ Enhanced {len(enhanced_results)} results for query: '{request.query}'")
        return response_data
        
    except Exception as e:
        logger.error(f"❌ Error enhancing results: {e}")
        raise HTTPException(status_code=500, detail=f"Enhancement failed: {str(e)}")

# Query suggestions endpoint
@app.post("/suggest-queries")
async def suggest_query_improvements(request: QuerySuggestionsRequest):
    """
    Get improved query suggestions
    """
    if not openai_service:
        raise HTTPException(
            status_code=503,
            detail="OpenAI service not available"
        )
    
    try:
        suggestions = await openai_service.suggest_query_improvements(
            query=request.query,
            context=request.context
        )
        
        return {
            "original_query": request.query,
            "suggestions": suggestions,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Error generating suggestions: {e}")
        raise HTTPException(status_code=500, detail=f"Suggestion generation failed: {str(e)}")

# Search intent extraction endpoint
@app.post("/extract-intent", response_model=SearchIntentResponse)
async def extract_search_intent(request: SearchIntentRequest):
    """
    Extract and classify search intent
    """
    if not openai_service:
        raise HTTPException(
            status_code=503,
            detail="OpenAI service not available"
        )
    
    try:
        intent_data = await openai_service.extract_search_intent(request.query)
        
        return SearchIntentResponse(
            query=intent_data["query"],
            intent_type=intent_data["intent_type"],
            category=intent_data["category"],
            urgency=intent_data["urgency"],
            confidence=intent_data["confidence"]
        )
        
    except Exception as e:
        logger.error(f"❌ Error extracting intent: {e}")
        raise HTTPException(status_code=500, detail=f"Intent extraction failed: {str(e)}")

# Service information endpoint
@app.get("/info")
async def service_info():
    """
    Get service information and status
    """
    return {
        "service": "AI Search Enhancement Service",
        "version": "1.0.0",
        "description": "OpenAI-powered search result enhancement using function calling",
        "endpoints": {
            "health": "/health",
            "enhance": "/enhance-results",
            "suggestions": "/suggest-queries", 
            "intent": "/extract-intent",
            "info": "/info"
        },
        "openai_available": openai_service is not None,
        "model": getattr(openai_service, 'model', 'N/A') if openai_service else 'N/A',
        "timestamp": datetime.utcnow().isoformat()
    }

# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint with basic service information
    """
    return {
        "message": "AI Search Enhancement Service",
        "status": "running",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    
    # Configuration from environment
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8001"))
    
    # Run the server
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=False,  # Set to True for development
        log_level="info"
    ) 