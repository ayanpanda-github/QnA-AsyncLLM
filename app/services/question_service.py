from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Question
from app.schemas import QuestionCreate


async def create_question(db: AsyncSession, doc_id: int, data: QuestionCreate) -> Question:
    question = Question(document_id=doc_id, **data.model_dump())
    db.add(question)
    await db.commit()
    await db.refresh(question)
    return question


async def get_question(db: AsyncSession, question_id: int) -> Question | None:
    result = await db.execute(select(Question).where(Question.id == question_id))
    return result.scalar_one_or_none()


async def update_question_answer(db: AsyncSession, question_id: int, answer: str) -> Question | None:
    question = await get_question(db, question_id)
    if question:
        question.answer = answer
        question.status = "answered"
        await db.commit()
        await db.refresh(question)
    return question
