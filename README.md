# Async Document Q&A Microservice

This project is a FastAPI-based microservice that allows storing documents, processing questions asynchronously with a mock LLM, and saving data using PostgreSQL. It is designed to be scalable and easily extendable with real LLM integrations.

## Setup Instructions

### Prerequisites
- Python 3.11+
- PostgreSQL
- Docker (optional, for containerized deployment)

### Local Development Setup
1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd async-doc-qa
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv venv
   . venv/Scripts/Activate.ps1  # On Windows
   # source venv/bin/activate  # On Unix or MacOS
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   - Copy `.env.example` to `.env` and configure database connection settings.

5. **Run database migrations**:
   ```bash
   alembic upgrade head
   ```

6. **Start the application**:
   ```bash
   python run_local.py
   ```
   The API will be available at `http://127.0.0.1:8000`.

### Docker Setup
1. **Build and run with Docker**:
   ```bash
   docker-compose up --build
   ```
   The API will be available at `http://localhost:8000`.

## How to Test the Endpoints

### Automated Tests
- Run tests using pytest:
  ```bash
  pytest tests/ -v
  ```

### Manual Testing
- Use tools like [HTTPie](https://httpie.io/) or [Postman](https://www.postman.com/) to test endpoints.

#### Available Endpoints
- **Document Endpoints**:
  - `POST /documents/`: Upload a new document.
  - `GET /documents/{doc_id}`: Retrieve a document by ID.
  - `GET /documents/`: List all documents.

- **Question Endpoints**:
  - `POST /documents/{doc_id}/question`: Ask a question about a document. Processes asynchronously.
  - `GET /questions/{question_id}`: Retrieve the status and answer of a question.

- **Health Check**:
  - `GET /health`: Check the health/status of the API.

### Example API Usage

#### 1. Upload a Document
```bash
# Using curl
curl -X POST "http://127.0.0.1:8000/documents/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Sample Document",
    "content": "This is a sample document about machine learning and AI."
  }'

# Response
{
  "id": 1,
  "title": "Sample Document",
  "content": "This is a sample document about machine learning and AI.",
  "created_at": "2025-01-28T09:00:00"
}
```

#### 2. Ask a Question (Async Processing)
```bash
# Using curl
curl -X POST "http://127.0.0.1:8000/documents/1/question" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is this document about?"
  }'

# Response (immediate)
{
  "question_id": 1,
  "status": "pending"
}
```

#### 3. Check Question Status and Answer
```bash
# Using curl
curl "http://127.0.0.1:8000/questions/1"

# Response (after processing)
{
  "id": 1,
  "document_id": 1,
  "question": "What is this document about?",
  "answer": "This is a generated answer to your question: What is this document about?",
  "status": "answered",
  "created_at": "2025-01-28T09:01:00"
}
```

#### 4. Get All Documents
```bash
# Using curl
curl "http://127.0.0.1:8000/documents/"

# Response
[
  {
    "id": 1,
    "title": "Sample Document",
    "content": "This is a sample document about machine learning and AI.",
    "created_at": "2025-01-28T09:00:00"
  }
]
```

#### 5. Health Check
```bash
# Using curl
curl "http://127.0.0.1:8000/health"

# Response
{
  "status": "ok"
}
```

### Swagger UI
Access the interactive API documentation at `http://127.0.0.1:8000/docs` once the server is running.

## Configuration

### Environment Variables
The application uses the following environment variables (configure in `.env` file):

- `DB_URL`: PostgreSQL connection string (default: `postgresql+asyncpg://user:password@localhost/docqa`)
- `LLM_DELAY`: Simulated LLM processing delay in seconds (default: `5`)

### Database Configuration
For local development, ensure PostgreSQL is running and create a database:
```sql
CREATE DATABASE docqa;
CREATE USER user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE docqa TO user;
```

## Architecture Overview

### Key Features
- **Async Processing**: Questions are processed in the background using `asyncio.create_task()`
- **Database**: PostgreSQL with async SQLAlchemy 2.0
- **Validation**: Pydantic schemas for request/response validation
- **Testing**: Comprehensive test suite with pytest
- **Documentation**: Auto-generated OpenAPI/Swagger documentation
- **Containerization**: Docker and Docker Compose support

### Project Structure
```
app/
├── core/           # Configuration and database setup
├── models/         # SQLAlchemy database models
├── schemas/        # Pydantic validation schemas
├── services/       # Business logic layer
└── api/            # FastAPI route handlers
```

## Development

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_main.py -v
```

### Database Migrations
```bash
# Create a new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## Extending the Service

### Adding Real LLM Integration
To replace the mock LLM with a real one (e.g., OpenAI):

1. Install the OpenAI SDK: `pip install openai`
2. Update `app/services/llm_service.py`:
```python
import openai
from app.core.config import settings

async def generate_answer(question: str) -> str:
    client = openai.AsyncOpenAI(api_key=settings.openai_api_key)
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": question}]
    )
    return response.choices[0].message.content
```
3. Add `OPENAI_API_KEY` to your environment variables

### Adding Authentication
Consider using `fastapi-users` or implementing JWT authentication for production use.

### Adding Caching
Implement Redis caching for frequently asked questions to improve performance.

## Troubleshooting

### Common Issues
1. **Database Connection Error**: Ensure PostgreSQL is running and connection string is correct
2. **Migration Errors**: Check that all models are imported in `alembic/env.py`
3. **Port Already in Use**: Change the port in `run_local.py` or kill the process using the port

### Logs
The application logs are available in the console when running locally. For production, consider using structured logging with tools like `structlog`.
