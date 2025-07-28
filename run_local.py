#!/usr/bin/env python3
"""
Simple script to run the application locally with development settings
"""

import uvicorn
import os

if __name__ == "__main__":
    # Set environment variables for local development
    os.environ.setdefault("DB_URL", "postgresql+asyncpg://user:password@localhost/docqa")
    os.environ.setdefault("LLM_DELAY", "2")  # Shorter delay for development
    
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
