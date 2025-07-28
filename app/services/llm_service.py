import asyncio
from app.core.config import settings


async def generate_answer(question: str) -> str:
    await asyncio.sleep(settings.llm_delay)  # simulate latency
    return f"This is a generated answer to your question: {question}"
