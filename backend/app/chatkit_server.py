from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, AsyncIterator

from agents import Agent, Runner
from chatkit.agents import stream_agent_response, AgentContext
from chatkit.errors import ErrorCode
from chatkit.server import ChatKitServer
from chatkit.actions import ActionConfig
from chatkit.types import (
    Action,
    AssistantMessageContent,
    AssistantMessageItem,
    ErrorEvent,
    ThreadMetadata,
    ThreadStreamEvent,
    ThreadItemDoneEvent,
    UserMessageItem,
    UserMessageTextContent,
    WidgetItem,
)
from chatkit.widgets import Button, Card, Col, Text
from openai import APIError
from openai.types.responses import ResponseInputContentParam

from .config import get_settings
from .memory_store import MemoryStore

logging.basicConfig(level=logging.INFO)
settings = get_settings()


class SimpleChatServer(ChatKitServer[dict[str, Any]]):
    """Simple ChatKit server with basic echo functionality."""

    def __init__(self) -> None:
        self.store: MemoryStore = MemoryStore()
        super().__init__(self.store)

        # Create a simple agent
        # Using gpt-3.5-turbo for cost savings (cheaper than gpt-4o-mini)
        # Other cheap options: "gpt-3.5-turbo", "gpt-4o-mini" (current cheapest GPT-4 variant)
        self.agent = Agent(
            model="gpt-3.5-turbo",
            name="Assistant",
            instructions="You are a helpful assistant. Keep responses concise and friendly.",
        )

    async def _build_user_message_item(
        self, input, thread: ThreadMetadata, context: dict[str, Any]
    ) -> UserMessageItem:
        """Override to handle Thread objects (which extend ThreadMetadata)."""
        # Ensure thread has an id (handle both Thread and ThreadMetadata)
        if thread is None:
            raise ValueError("Thread cannot be None when building user message item")
        
        # Thread extends ThreadMetadata, so we can use it directly
        return UserMessageItem(
            id=self.store.generate_item_id("message", thread, context),
            content=input.content,
            thread_id=thread.id,
            attachments=[
                await self.store.load_attachment(attachment_id, context)
                for attachment_id in input.attachments
            ],
            quoted_text=input.quoted_text,
            inference_options=input.inference_options,
            created_at=datetime.now(),
        )

    async def respond(
        self,
        thread: ThreadMetadata,
        item: UserMessageItem | None,
        context: dict[str, Any],
    ) -> AsyncIterator[ThreadStreamEvent]:
        """Respond to user messages."""

        try:
            # Create agent context
            agent_context = AgentContext(
                thread=thread,
                store=self.store,
                request_context=context,
            )

            # Load recent thread items for context
            items_page = await self.store.load_thread_items(
                thread.id,
                after=None,
                limit=20,
                order="desc",
                context=context,
            )

            # Runner expects most recent message last
            items = list(reversed(items_page.data))

            # Convert to agent input format
            input_items = []
            for thread_item in items:
                if hasattr(thread_item, 'content'):
                    if isinstance(thread_item, UserMessageItem):
                        # Extract text from UserMessageItem content array
                        # content is a list of UserMessageTextContent or UserMessageTagContent
                        text_parts = []
                        for content_part in thread_item.content:
                            if isinstance(content_part, UserMessageTextContent):
                                text_parts.append(content_part.text)
                            # Skip UserMessageTagContent for now (could handle @mentions later)
                        if text_parts:
                            # Join all text parts into a single string
                            text = "".join(text_parts)
                            input_items.append({"role": "user", "content": text})
                    elif isinstance(thread_item, AssistantMessageItem):
                        # Get text from content array
                        text = ""
                        for content in thread_item.content:
                            if hasattr(content, 'text'):
                                text += content.text
                        if text:
                            input_items.append({"role": "assistant", "content": text})

            # Run the agent
            result = Runner.run_streamed(
                self.agent,
                input_items,
                context=agent_context,
            )

            # Stream the response
            async for event in stream_agent_response(agent_context, result):
                yield event
        except APIError as e:
            # Handle OpenAI API errors (e.g., quota exceeded, rate limits)
            error_message = str(e)
            if "quota" in error_message.lower() or "billing" in error_message.lower():
                error_message = "OpenAI API quota exceeded. Please check your billing and plan details."
            elif "rate limit" in error_message.lower():
                error_message = "OpenAI API rate limit exceeded. Please try again later."
            
            logging.error(f"OpenAI API error: {e}")
            yield ErrorEvent(
                code=ErrorCode.STREAM_ERROR,
                message=error_message,
                allow_retry=True,
            )
        except Exception as e:
            # Handle other errors
            error_message = f"An error occurred: {str(e)}"
            logging.exception("Error in respond method")
            yield ErrorEvent(
                code=ErrorCode.STREAM_ERROR,
                message=error_message,
                allow_retry=True,
            )

    async def action(
        self,
        thread: ThreadMetadata,
        action: Action[str, Any],
        sender: WidgetItem | None,
        context: dict[str, Any],
    ) -> AsyncIterator[ThreadStreamEvent]:
        """Handle custom actions like sharing threads."""
        
        if action.type == "share_thread":
            # Generate shareable URL for the thread
            thread_url = f"{context.get('base_url', 'http://localhost:5173')}/thread/{thread.id}"
            
            # Create a widget with the share link and copy button
            share_widget = WidgetItem(
                id=self.store.generate_item_id("widget", thread, context),
                thread_id=thread.id,
                created_at=datetime.now(),
                widget=Card(
                    children=[
                        Col(
                            children=[
                                Text(
                                    text="Share this conversation",
                                    size="lg",
                                    weight="bold",
                                ),
                                Text(
                                    text=f"Thread ID: {thread.id}",
                                    size="sm",
                                    color="secondary",
                                ),
                                Button(
                                    label="Copy Link",
                                    onClickAction=ActionConfig(
                                        type="copy_to_clipboard",
                                        payload={"text": thread_url},
                                        handler="client",  # Handle on client side
                                    ),
                                    style="primary",
                                ),
                                Text(
                                    text=thread_url,
                                    size="sm",
                                    color="secondary",
                                ),
                            ],
                            gap="md",
                        ),
                    ],
                ),
            )
            
            yield ThreadItemDoneEvent(item=share_widget)
        else:
            # Unknown action
            yield ErrorEvent(
                code=ErrorCode.STREAM_ERROR,
                message=f"Unknown action type: {action.type}",
                allow_retry=False,
            )


def create_chatkit_server() -> SimpleChatServer:
    """Create and return a configured ChatKit server instance."""
    return SimpleChatServer()


# Singleton instance
chatkit_server = create_chatkit_server()
