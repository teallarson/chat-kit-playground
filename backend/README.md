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

4. Add your Anthropic API key to `.env`:
```
ANTHROPIC_API_KEY=your_api_key_here
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

## Next Steps

- [ ] Integrate Anthropic Claude for AI responses
- [ ] Add proper session management
- [ ] Implement database storage (replace in-memory storage)
- [ ] Add authentication
- [ ] Implement proper ChatKit API specification
- [ ] Add error handling and logging

## Tech Stack

- FastAPI - Modern Python web framework
- Anthropic SDK - Claude AI integration
- Uvicorn - ASGI server
- Pydantic - Data validation
