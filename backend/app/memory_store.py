"""In-memory implementation of ChatKit Store."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from chatkit.store import NotFoundError, Store
from chatkit.types import (
    Attachment,
    Page,
    ThreadItem,
    ThreadMetadata,
    UserMessageItem,
    UserMessageTextContent,
)


class MemoryStore(Store[dict[str, Any]]):
    """Simple in-memory store for development."""

    def __init__(self) -> None:
        self.threads: dict[str, ThreadMetadata] = {}
        self.thread_items: dict[str, list[ThreadItem]] = {}

    def generate_item_id(
        self,
        type: str,
        thread: ThreadMetadata,
        context: dict[str, Any],
    ) -> str:
        """Generate a unique item ID."""
        return f"{type}_{uuid.uuid4().hex[:8]}"

    async def load_thread(
        self,
        thread_id: str,
        context: dict[str, Any],
    ) -> ThreadMetadata:
        """Load a thread by ID."""
        thread = self.threads.get(thread_id)
        if thread is None:
            raise NotFoundError(f"Thread {thread_id} not found")
        return thread

    async def save_thread(
        self,
        thread: ThreadMetadata,
        context: dict[str, Any],
    ) -> None:
        """Save or update a thread."""
        self.threads[thread.id] = thread
        if thread.id not in self.thread_items:
            self.thread_items[thread.id] = []

    async def load_thread_items(
        self,
        thread_id: str,
        after: str | None,
        limit: int,
        order: str,
        context: dict[str, Any],
    ) -> Page[ThreadItem]:
        """Load thread items."""
        items = self.thread_items.get(thread_id, [])

        # Simple pagination (not production-ready)
        if order == "desc":
            items = list(reversed(items))

        return Page(
            data=items[:limit],
            has_more=len(items) > limit,
        )

    async def add_thread_item(
        self,
        thread_id: str,
        item: ThreadItem,
        context: dict[str, Any],
    ) -> None:
        """Add an item to a thread."""
        if thread_id not in self.thread_items:
            self.thread_items[thread_id] = []
        self.thread_items[thread_id].append(item)
        
        # Auto-generate thread title from first user message if thread doesn't have one
        thread = self.threads.get(thread_id)
        if thread and not thread.title:
            # Check if this is a user message
            if isinstance(item, UserMessageItem) and item.content:
                # Extract text from first content item
                first_content = item.content[0] if item.content else None
                if isinstance(first_content, UserMessageTextContent):
                    # Use first 50 characters as title
                    title = first_content.text[:50].strip()
                    if title:
                        # Update thread with title
                        thread.title = title if len(first_content.text) <= 50 else title + "..."
                        self.threads[thread_id] = thread

    async def update_thread_item(
        self,
        thread_id: str,
        item: ThreadItem,
        context: dict[str, Any],
    ) -> None:
        """Update a thread item."""
        items = self.thread_items.get(thread_id, [])
        for i, existing_item in enumerate(items):
            if existing_item.id == item.id:
                items[i] = item
                break

    async def delete_thread_item(
        self,
        thread_id: str,
        item_id: str,
        context: dict[str, Any],
    ) -> None:
        """Delete a thread item."""
        items = self.thread_items.get(thread_id, [])
        self.thread_items[thread_id] = [
            item for item in items if item.id != item_id
        ]

    async def delete_thread(
        self,
        thread_id: str,
        context: dict[str, Any],
    ) -> None:
        """Delete a thread."""
        self.threads.pop(thread_id, None)
        self.thread_items.pop(thread_id, None)

    async def load_threads(
        self,
        after: str | None,
        limit: int,
        order: str,
        context: dict[str, Any],
    ) -> Page[ThreadMetadata]:
        """Load all threads."""
        threads = list(self.threads.values())
        
        # Sort by created_at (newest first for desc, oldest first for asc)
        threads.sort(key=lambda t: t.created_at, reverse=(order == "desc"))
        
        # Handle pagination with 'after' cursor (simple implementation)
        if after:
            # Find the thread with the 'after' ID and start from the next one
            try:
                after_index = next(i for i, t in enumerate(threads) if t.id == after)
                threads = threads[after_index + 1:]
            except StopIteration:
                # If 'after' thread not found, return empty
                threads = []
        
        return Page(
            data=threads[:limit],
            has_more=len(threads) > limit,
            after=threads[limit - 1].id if len(threads) > limit else None,
        )

    async def load_item(
        self,
        thread_id: str,
        item_id: str,
        context: dict[str, Any],
    ) -> ThreadItem | None:
        """Load a specific thread item."""
        items = self.thread_items.get(thread_id, [])
        for item in items:
            if item.id == item_id:
                return item
        return None

    async def save_item(
        self,
        thread_id: str,
        item: ThreadItem,
        context: dict[str, Any],
    ) -> None:
        """Save a thread item (add or update)."""
        items = self.thread_items.get(thread_id, [])
        
        # Check if item exists
        for i, existing_item in enumerate(items):
            if existing_item.id == item.id:
                items[i] = item
                return
        
        # If not found, add it
        items.append(item)

    async def save_attachment(
        self,
        thread_id: str,
        attachment_id: str,
        data: bytes,
        context: dict[str, Any],
    ) -> None:
        """Save an attachment (not implemented for in-memory store)."""
        # For a simple in-memory store, we'll skip attachment storage
        pass

    async def load_attachment(
        self,
        attachment_id: str,
        context: dict[str, Any],
    ) -> Attachment:
        """Load an attachment (not implemented for in-memory store)."""
        # For a simple in-memory store, attachments are not supported
        raise NotFoundError(f"Attachment {attachment_id} not found (attachments not supported in memory store)")

    async def delete_attachment(
        self,
        thread_id: str,
        attachment_id: str,
        context: dict[str, Any],
    ) -> None:
        """Delete an attachment (not implemented for in-memory store)."""
        # For a simple in-memory store, we'll skip attachment deletion
        pass
