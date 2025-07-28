from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.database import engine
from app.api.v1 import documents, questions


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup - resources are ready
    yield
    # Graceful shutdown
    await engine.dispose()


app = FastAPI(title="Document Q&A", lifespan=lifespan)

# Include routers
app.include_router(documents.router, prefix="/documents", tags=["documents"])
app.include_router(questions.router, prefix="/questions", tags=["questions"])

# Health check
@app.get("/health")
async def health_check():
    return {"status": "ok"}
