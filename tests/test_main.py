import pytest
import asyncio
from httpx import AsyncClient
from fastapi.testclient import TestClient
from app.main import app


def test_health_check():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_async_health_check():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# Example test for the full flow (requires database setup)
# @pytest.mark.asyncio
# async def test_question_flow():
#     async with AsyncClient(app=app, base_url="http://test") as client:
#         # Create document
#         doc_response = await client.post("/documents/", json={
#             "title": "Test Document",
#             "content": "This is test content"
#         })
#         assert doc_response.status_code == 201
#         doc_id = doc_response.json()["id"]
#         
#         # Ask question
#         question_response = await client.post(f"/documents/{doc_id}/question", json={
#             "question": "What is this about?"
#         })
#         assert question_response.status_code == 202
#         question_id = question_response.json()["question_id"]
#         
#         # Check question status
#         status_response = await client.get(f"/questions/{question_id}")
#         assert status_response.status_code == 200
#         assert status_response.json()["status"] in ["pending", "answered"]
