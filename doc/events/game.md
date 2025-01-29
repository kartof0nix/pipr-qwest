The `events/game.py` file defines the framework for managing and executing various game events. It is designed to facilitate a modular, dynamic, and extensible event-driven system that handles player interactions, condition checks, damage calculations, and more.

### **Functionality**
1. **Base Event Class**
   - `GameEvent` is the base class for all events, providing common functionality such as:
     - Storing event-specific configurations.
     - Handling the lifecycle of an event (start, execution, and completion).
     - Assigning values to game state variables after the event finishes.

2. **Meta-Class for Registration**
   - `RegisterEventMeta` dynamically tracks all event subclasses and registers them in a global `eventTypes` dictionary. This enables event creation using their class names.

3. **Custom Event Types**
   - The module provides several specialized event classes:
     - **`IfEvent`**: Executes different events based on a condition.
     - **`DamageEvent`**: Reduces the player’s health and triggers a `gameover` event if health drops to zero.
     - **`menuEvent`**: Represents a menu with selectable entries, triggering the corresponding event for the chosen entry.
     - **`ConversationEvent`**: Manages dialogue sequences with multiple lines.
     - **`changeLevelEvent`**: Prepares for level changes by specifying the next level and field.

4. **Event Factory**
   - `eventFromDict(type, eventId, config)`:
     - Dynamically creates an event instance from a dictionary, based on the specified type and configuration.

5. **Event Lifecycle**
   - Events are asynchronous and can be awaited. They push `event_start` and `event_end` messages to the central event queue for other modules to act on.

---

### **Usage**
1. **Registering and Handling Events**
   - Event classes are automatically registered using the `RegisterEventMeta` metaclass.
   - To create a new event, define a subclass of `GameEvent` and specify the desired behavior.

2. **Creating Events Dynamically**
   - Use `eventFromDict` to create events based on configuration dictionaries:
     ```python
     event = eventFromDict("DamageEvent", "event1", {"hp": 10})
     ```

3. **Executing Events**
   - Events can be executed asynchronously by awaiting them:
     ```python
     result = await event()
     ```

4. **Custom Event Logic**
   - Developers can define new event types by subclassing `GameEvent` and implementing their specific functionality.

---

### **Examples**
1. **Damage Event**
   - Decreases player health by 10 and triggers `gameover` if health is zero:
     ```python
     damage_event = DamageEvent("damage1", {"hp": 10})
     await damage_event()
     ```

2. **Conditional Event**
   - Executes `eventA` if a condition is true, otherwise `eventB`:
     ```python
     if_event = IfEvent("conditional", {"condition": "player.health > 50", "eventIdTrue": "eventA", "eventIdFalse": "eventB"})
     next_event = await if_event()
     ```

3. **Menu Event**
   - Displays a menu and triggers the corresponding event for the selected entry:
     ```python
     menu = menuEvent("menu1", {"entryList": ["Option1", "Option2"], "eventList": ["event1", "event2"]})
     next_event = await menu()
     ```

