# Chat UI - Setup Guide

A full-stack chat application with React frontend and FastAPI backend.

## Quick Start

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Add your OpenAI API key to .env (required)
# OPENAI_API_KEY=sk-...

# Start the backend server
python -m uvicorn app.main:app --reload --port 8000
```

The backend will be running at `http://localhost:8000`

### 2. Frontend Setup (React)

In a new terminal (from project root):

```bash
# Navigate to react folder
cd react

# Install dependencies
npm install

# Start the development server
npm run dev
```

The frontend will be running at `http://localhost:5173`

## How It Works

1. **Frontend** (React + ChatKit) runs on port 5173
2. **Backend** (FastAPI) runs on port 8000
3. **Vite proxy** forwards `/api/chatkit/*` requests from frontend to backend
4. Backend handles chat logic and (eventually) AI responses

## Current Features

- ✅ Basic chat interface
- ✅ Session management
- ✅ Thread creation
- ✅ Message sending
- ✅ OpenAI agent integration (GPT-3.5-turbo)
- ✅ Streaming responses
- ✅ In-memory storage
- ⏳ Database storage (coming next)
- ⏳ Authentication (coming next)

## Next Steps

The backend is already integrated with OpenAI agents. To customize:

1. Get an OpenAI API key from https://platform.openai.com/api-keys
2. Add it to `backend/.env`:
   ```
   OPENAI_API_KEY=sk-...
   ```
3. Customize the agent in `backend/app/chatkit_server.py` (model, instructions, etc.)

## Project Structure

```
chat-ui/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── main.py      # FastAPI app and routes
│   │   ├── chatkit_server.py  # ChatKit server implementation
│   │   ├── memory_store.py    # In-memory storage
│   │   └── config.py    # Configuration
│   ├── dev.sh           # Development script
│   ├── requirements.txt
│   └── .env.example
├── react/                # React frontend
│   ├── src/
│   │   ├── Chat.tsx     # Main chat component
│   │   ├── Chat.css     # Styling
│   │   └── App.tsx      # App entry
│   ├── vite.config.ts   # Vite config with proxy
│   └── package.json
└── vue/                  # Vue frontend (coming soon)
```

## Troubleshooting

**Backend won't start:**
- Make sure virtual environment is activated
- Check Python version (3.10+)
- Verify all dependencies installed

**Frontend can't connect:**
- Ensure backend is running on port 8000
- Check browser console for errors
- Verify Vite proxy configuration

**CORS errors:**
- Backend is configured to allow localhost:5173
- Check CORS middleware in `backend/app/main.py`
