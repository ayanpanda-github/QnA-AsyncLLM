from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Document
from app.schemas import DocumentCreate


async def create_document(db: AsyncSession, data: DocumentCreate) -> Document:
    doc = Document(**data.model_dump())
    db.add(doc)
    await db.commit()
    await db.refresh(doc)
    return doc


async def get_document(db: AsyncSession, doc_id: int) -> Document | None:
    result = await db.execute(select(Document).where(Document.id == doc_id))
    return result.scalar_one_or_none()


async def get_documents(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[Document]:
    result = await db.execute(select(Document).offset(skip).limit(limit))
    return list(result.scalars().all())
