import pytest
import asyncio
from src.common.event_queue import pushEvent, registerHandler, unregisterHandler, loop

@pytest.mark.asyncio
async def test_event_queue():
    results = []

    async def test_handler(params):
        """Sample event handler."""
        results.append(params["value"])

    # Register the event handler
    registerHandler("test_event", test_handler)

    # Push events into the queue
    pushEvent("test_event", {"value": 1})
    pushEvent("test_event", {"value": 2})
    pushEvent("test_event", {"value": 3})

    # Start the event loop in a limited capacity
    task = asyncio.create_task(loop())
    await asyncio.sleep(0.3)  # Allow time for events to process

    # Validate that the handler was called with the correct parameters
    assert results == [1, 2, 3]

    # Unregister the handler
    unregisterHandler("test_event", test_handler)

    # Push another event and ensure it does not get processed
    results.clear()
    pushEvent("test_event", {"value": 4})
    await asyncio.sleep(0.1)

    assert results == []
    task.cancel()  # Cancel the loop after testing
