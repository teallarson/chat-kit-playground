# Chat UI

A React-based chat interface built with OpenAI's ChatKit framework, configured to work with a custom backend endpoint.

## Features

- Modern chat interface using ChatKit-JS
- Custom backend integration support
- Responsive design
- TypeScript support

## Setup

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

## Configuration

The chat interface is configured in `src/Chat.tsx`. Key configuration points:

- **Custom Backend URL**: Set in `api.url` (currently `/api/chatkit`)
- **Domain Key**: Replace `your-domain-key` with your actual domain key
- **Custom Headers**: Add authentication or other headers in the `fetch` function

## Next Steps

To make this chat interface fully functional, you'll need to:

1. **Set up a backend server** that implements the ChatKit API specification
2. **Configure the domain key** for your deployment
3. **Implement authentication** if needed
4. **Connect to your AI agent** or LLM endpoint

## Backend Requirements

Your backend must implement the ChatKit API specification, handling:
- Session management
- Thread management
- Message handling
- Streaming responses

See [ChatKit Custom Backends Guide](https://openai.github.io/chatkit-js/guides/custom-backends/) for details.

## Tech Stack

- React 18
- TypeScript
- Vite
- ChatKit-JS
- ChatKit-React

## Development

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
