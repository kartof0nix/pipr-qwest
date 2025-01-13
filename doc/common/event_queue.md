### **Responsibility and Usage**

The `event_queue.py` file provides a centralized event queue system for managing and handling game events. It allows modules to:
1. **Push Events**: Modules can enqueue events using `pushEvent()`.
2. **Register Handlers**: Modules can register callback functions to handle specific events via `registerHandler()`.
3. **Unregister Handlers**: Modules can remove event listeners using `unregisterHandler()`.
4. **Event Processing**: The `loop()` function processes events asynchronously, invoking all registered handlers for a given event type.

This system facilitates decoupled communication between game modules, ensuring that events can trigger actions across different parts of the game.

