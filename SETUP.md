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

# Add your Anthropic API key to .env (optional for now)
# ANTHROPIC_API_KEY=your_key_here

# Start the backend server
python -m uvicorn app.main:app --reload --port 8000
```

The backend will be running at `http://localhost:8000`

### 2. Frontend Setup

In a new terminal:

```bash
# Navigate to project root (where package.json is)
cd chat-ui

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
- ✅ Echo responses (placeholder)
- ⏳ AI integration (coming next)

## Next Steps

To integrate AI responses:

1. Get an Anthropic API key from https://console.anthropic.com/
2. Add it to `backend/.env`:
   ```
   ANTHROPIC_API_KEY=sk-ant-...
   ```
3. Update `backend/app/main.py` to use Claude instead of echo responses

## Project Structure

```
chat-ui/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── main.py      # Main server file
│   │   └── config.py    # Configuration
│   ├── requirements.txt
│   └── .env.example
├── src/                  # React frontend
│   ├── Chat.tsx         # Main chat component
│   ├── Chat.css         # Styling
│   └── App.tsx          # App entry
├── vite.config.ts       # Vite config with proxy
└── package.json
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
