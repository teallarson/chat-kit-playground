import { ChatKit, useChatKit } from '@openai/chatkit-react';
import { useEffect } from 'react';
import './Chat.css';

export function Chat() {
  useEffect(() => {
    console.log('Chat component mounted');
    console.log('ChatKit web component defined?', customElements.get('openai-chatkit'));
    
    // Listen for custom actions from ChatKit widgets
    const handleAction = (event: CustomEvent) => {
      const { type, payload } = event.detail || {};
      
      if (type === 'copy_to_clipboard' && payload?.text) {
        // Copy text to clipboard
        navigator.clipboard.writeText(payload.text).then(() => {
          console.log('Copied to clipboard:', payload.text);
          // You could show a toast notification here
        }).catch((err) => {
          console.error('Failed to copy to clipboard:', err);
        });
      }
    };
    
    // Listen for action events from the ChatKit component
    const chatKitElement = document.querySelector('openai-chatkit');
    if (chatKitElement) {
      chatKitElement.addEventListener('chatkit.action', handleAction as EventListener);
    }
    
    return () => {
      if (chatKitElement) {
        chatKitElement.removeEventListener('chatkit.action', handleAction as EventListener);
      }
    };
  }, []);

  const { control } = useChatKit({
    api: {
      // Points to our FastAPI backend (proxied through Vite)
      url: '/api/chatkit',
      domainKey: 'local-dev', // Dev domain key
      fetch: async (url, options) => {
        const response = await fetch(url, {
          ...options,
          headers: {
            ...options?.headers,
            'Content-Type': 'application/json',
          },
        });
        
        // Check for HTTP errors
        if (!response.ok) {
          let errorMessage = `HTTP ${response.status}: ${response.statusText}`;
          try {
            const errorData = await response.json();
            errorMessage = errorData.error || errorMessage;
          } catch {
            // If response isn't JSON, use the status text
            const text = await response.text();
            if (text) {
              errorMessage = text;
            }
          }
          throw new Error(errorMessage);
        }
        
        return response;
      },
    },
    startScreen: {
      greeting: 'Hey there! 👋 I\'m your AI assistant. What would you like to chat about?',
      prompts: [
        {
          label: '💡 Get creative',
          prompt: 'Help me brainstorm ideas for a new project',
          icon: 'sparkle',
        },
        {
          label: '📚 Learn something',
          prompt: 'Explain a concept I\'m curious about',
          icon: 'circle-question',
        },
        {
          label: '✍️ Write something',
          prompt: 'Help me write or edit some content',
          icon: 'sparkle',
        },
        {
          label: '🤔 Ask anything',
          prompt: 'Answer a question I have',
          icon: 'circle-question',
        },
      ],
    },
    theme: {
      colorScheme: 'light',
      radius: 'round',
      color: {
        accent: {
          primary: '#6366f1', // Indigo to match your design
          level: 2,
        },
      },
      density: 'normal',
      typography: {
        fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", "Oxygen", "Ubuntu", "Cantarell", "Fira Sans", "Droid Sans", "Helvetica Neue", sans-serif',
      },
    },
    composer: {
      placeholder: 'Type your message...',
    },
  });

  return (
    <div className="chat-container">
      <ChatKit control={control} className="chat-interface" />
    </div>
  );
}
