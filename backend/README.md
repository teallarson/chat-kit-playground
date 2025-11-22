# Chat UI Backend

FastAPI backend for the Chat UI, implementing a custom ChatKit-compatible API.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file:
```bash
cp .env.example .env
```

4. Add your OpenAI API key to `.env` (required):
```
OPENAI_API_KEY=sk-your_api_key_here
```

## Running

### Quick Start (recommended)
```bash
./dev.sh
```

### Or manually
```bash
source venv/bin/activate
python -m uvicorn app.main:app --reload --port 8000
```

### Using uv (optional - faster alternative)
If you have `uv` installed:
```bash
uv sync
uv run uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

## API Endpoints

- `POST /api/chatkit/sessions` - Create a new session
- `POST /api/chatkit/threads` - Create a new thread
- `GET /api/chatkit/threads` - List all threads
- `GET /api/chatkit/threads/{thread_id}` - Get thread details
- `POST /api/chatkit/threads/{thread_id}/messages` - Send a message (streaming response)

## Current Implementation

- ✅ OpenAI agent integration (GPT-3.5-turbo)
- ✅ ChatKit server implementation
- ✅ Session and thread management
- ✅ Streaming responses
- ✅ In-memory storage (MemoryStore)

## Next Steps

- [ ] Implement database storage (replace in-memory storage)
- [ ] Add authentication
- [ ] Add error handling and logging improvements
- [ ] Add more agent customization options

## Tech Stack

- FastAPI - Modern Python web framework
- OpenAI Agents SDK - AI agent integration
- ChatKit Server SDK - ChatKit API implementation
- Uvicorn - ASGI server
- Pydantic - Data validation
