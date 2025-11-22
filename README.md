# Chat UI

A full-stack chat application with React frontend and FastAPI backend, built with OpenAI's ChatKit framework.

## Features

- Modern chat interface using ChatKit-React
- FastAPI backend with ChatKit SDK integration
- OpenAI agent integration (GPT-3.5-turbo)
- Session and thread management
- Streaming responses
- Responsive design
- TypeScript support

## Quick Start

See [SETUP.md](./SETUP.md) for detailed setup instructions.

### Frontend (React)
```bash
cd react
npm install
npm run dev
```

### Backend
```bash
cd backend
./dev.sh
# Or manually:
source venv/bin/activate
python -m uvicorn app.main:app --reload --port 8000
```

## Configuration

The chat interface is configured in `src/Chat.tsx` and connects to the backend via `/api/chatkit` (proxied through Vite).

Backend configuration is in `backend/app/config.py` and uses environment variables from `backend/.env`:
- `OPENAI_API_KEY` - Your OpenAI API key (required)
- `HOST` - Backend host (default: 0.0.0.0)
- `PORT` - Backend port (default: 8000)
- `FRONTEND_URL` - Frontend URL for CORS (default: http://localhost:5173)

## Tech Stack

**Frontend:**
- React 19
- TypeScript
- Vite
- ChatKit-React

**Backend:**
- FastAPI
- Python 3.10+
- OpenAI Agents SDK
- ChatKit Server SDK
- Uvicorn

## Development

**Frontend (React):**
- `cd react && npm run dev` - Start development server (http://localhost:5173)
- `cd react && npm run build` - Build for production
- `cd react && npm run preview` - Preview production build

**Backend:**
- `cd backend && ./dev.sh` - Start backend server (http://localhost:8000)
- Or manually: `python -m uvicorn app.main:app --reload --port 8000`

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
