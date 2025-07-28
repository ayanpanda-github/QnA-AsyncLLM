import asyncio
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db, AsyncSessionLocal
from app.schemas import QuestionCreate, QuestionOut, QuestionResponse
from app.services import document_service, question_service, llm_service
from app.models import Question

router = APIRouter()

# Keep references to background tasks to avoid garbage collection
tasks = set()


@router.post("/{doc_id}/question", response_model=QuestionResponse, status_code=202)
async def ask_question(doc_id: int, q: QuestionCreate, db: AsyncSession = Depends(get_db)):
    # Check if document exists
    doc = await document_service.get_document(db, doc_id)
    if not doc:
        raise HTTPException(404, "Document not found")
    
    # Create question
    question = await question_service.create_question(db, doc_id, q)
    
    # Fire-and-forget task
    task = asyncio.create_task(_process_question(question.id, q.question))
    tasks.add(task)  # keep ref to avoid GC
    task.add_done_callback(tasks.discard)  # cleanup when done
    
    return {"question_id": question.id, "status": question.status}


@router.get("/{question_id}", response_model=QuestionOut)
async def get_question(question_id: int, db: AsyncSession = Depends(get_db)):
    question = await question_service.get_question(db, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question


async def _process_question(q_id: int, text: str):
    """Background task to process question with LLM"""
    try:
        # Generate answer using mock LLM
        answer = await llm_service.generate_answer(text)
        
        # Update question with answer in a new session
        async with AsyncSessionLocal() as db:
            await question_service.update_question_answer(db, q_id, answer)
    except Exception as e:
        # In production, you'd want proper logging here
        print(f"Error processing question {q_id}: {e}")
