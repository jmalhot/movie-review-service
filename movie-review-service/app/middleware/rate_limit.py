from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import time
from collections import defaultdict
from app.core.config import settings

# Simple in-memory store for rate limiting
# In production, you'd want to use Redis for this
request_counts = defaultdict(list)

async def rate_limit_middleware(request: Request, call_next):
    # Get client IP
    client_ip = request.client.host
    
    # Get current timestamp
    now = time.time()
    
    # Clean old requests
    request_counts[client_ip] = [
        timestamp for timestamp in request_counts[client_ip]
        if timestamp > now - 60
    ]
    
    # Check if rate limit is exceeded
    if len(request_counts[client_ip]) >= settings.RATE_LIMIT_PER_MINUTE:
        return JSONResponse(
            status_code=429,
            content={"detail": "Too many requests"}
        )
    
    # Add current request timestamp
    request_counts[client_ip].append(now)
    
    # Process the request
    response = await call_next(request)
    return response 