The `graphics.py` file in the `events` module provides graphical interfaces (TUI - Text User Interface) for managing in-game events. It integrates with the `GameEvent` system to display interactive elements, notifications, and dialogues in the game's text-based user interface.

---

### **Responsibilities**
1. **Event-Based TUIs**
   - Defines `GameEventTUI` and its subclasses to provide specific interfaces for different event types.
   - Handles event interactions, including notifications, menu selection, and conversations.

2. **Dynamic TUI Integration**
   - TUIs are dynamically associated with events using the `RegisterEventTUIMeta` metaclass.
   - Event-specific TUIs are registered and instantiated as needed.

3. **Graphical User Feedback**
   - Displays graphical notifications for events like damage or level changes.
   - Presents menus and dialogues for player interaction.

---

### **Key Components**

#### **Metaclass: `RegisterEventTUIMeta`**
- Automatically registers subclasses of `GameEventTUI` in the global `eventTUIs` dictionary.
- Facilitates dynamic mapping of events to their corresponding TUI classes.

#### **Base Class: `GameEventTUI`**
- Serves as the base for all event-specific TUIs.
- Manages event lifecycle (`__enter__` and `__exit__`) and interaction with the TUI framework (`tui_main`).

#### **Subclasses**
1. **`notifyEventTUI`**
   - Displays a simple notification message.
   - Used for events like `DamageEvent` and `changeLevelEvent`.

2. **`DamageEventTUI`**
   - Inherits from `notifyEventTUI` to display damage notifications.
   - Message: `"You have been dealt {damage} damage!"`

3. **`changeLevelEventTUI`**
   - Inherits from `notifyEventTUI` to display level transition notifications.
   - Message: `"You have found a passage to {nextLevel}"`

4. **`menuEventTUI`**
   - Displays a menu for player choice.
   - Uses `entryList` from the `menuEvent` to populate menu options.
   - Handles menu interactions and triggers the selected action.

5. **`ConversationEventTUI`**
   - Manages dialogue events with a character and text.
   - Provides a "Next" button for progressing through dialogue lines.
   - Uses `ConversationEvent` to fetch and display the current and next dialogue lines.

---

### **Key Functionalities**

#### **Dynamic Widget Creation**
- Each TUI subclass creates its interface dynamically using `urwid` widgets (e.g., `Text`, `Button`, `Pile`).

#### **Event Integration**
- TUIs are linked to `GameEvent` instances and triggered during the event lifecycle.
- Events requiring user input (`uiEvent=True`) are paused until the TUI completes (e.g., menu selection).

#### **Notifications and Interactions**
- Notifications are displayed temporarily and cleared automatically.
- Menus and dialogues involve user input, with results affecting subsequent events.

---

### **Example Usage**

1. **Displaying a Damage Notification**
   ```python
   damage_event = DamageEvent("damage_1", {"hp": 10})
   damage_tui = DamageEventTUI(damage_event)
   with damage_tui:
       asyncio.run(damage_event())
   ```

2. **Showing a Menu**
   ```python
   menu_event = menuEvent("menu_1", {"entryList": ["Attack", "Defend"], "eventList": ["attack_event", "defend_event"]})
   menu_tui = menuEventTUI(menu_event)
   with menu_tui:
       asyncio.run(menu_event())
   ```

3. **Running a Conversation**
   ```python
   conversation_event = ConversationEvent(
       "dialogue_1",
       {"dialogue": [("NPC", "Hello, adventurer!"), ("NPC", "Good luck!")]}
   )
   conversation_tui = ConversationEventTUI(conversation_event)
   with conversation_tui:
       asyncio.run(conversation_event())
   ```
