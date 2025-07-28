from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.schemas import DocumentCreate, DocumentOut
from app.services import document_service

router = APIRouter()


@router.post("/", response_model=DocumentOut, status_code=201)
async def upload_doc(data: DocumentCreate, db: AsyncSession = Depends(get_db)):
    return await document_service.create_document(db, data)


@router.get("/{doc_id}", response_model=DocumentOut)
async def get_document(doc_id: int, db: AsyncSession = Depends(get_db)):
    doc = await document_service.get_document(db, doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc


@router.get("/", response_model=list[DocumentOut])
async def list_documents(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    return await document_service.get_documents(db, skip=skip, limit=limit)
